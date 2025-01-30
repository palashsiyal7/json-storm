from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json
import random
import string
import re
import requests
import os
from serverless_wsgi import handle_request

app = Flask(__name__)

# MongoDB configuration
mongo_client = None
db = None

class DataGenerator:
    @staticmethod
    def generate_phone_number():
        return ''.join(random.choices(string.digits, k=10))

    @staticmethod
    def random_int():
        return str(random.randint(1, 100))

    @staticmethod
    def random_float():
        return f"{random.random():.4f}"

    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))

generators = {
    'random_int': DataGenerator.random_int,
    'random_float': DataGenerator.random_float,
    'random_string': DataGenerator.random_string,
    'phone_number': DataGenerator.generate_phone_number,
    'contact_number': DataGenerator.generate_phone_number
}

def validate_and_generate_data(template, iterations, mongo_config=None):
    pattern = re.compile(r'\{\{(\w+)\}\}')
    results = []
    
    for i in range(iterations):
        try:
            def replacer(match):
                key = match.group(1)
                return generators.get(key, lambda: match.group(0))()
            
            new_body = pattern.sub(replacer, template)
            parsed_json = json.loads(new_body)
            
            # Validate phone numbers
            for key in ['phoneNumber', 'refrenceContactFirst', 
                       'refrenceContactSecond', 'refrenceContactThird']:
                if key in parsed_json and \
                (not parsed_json[key].isdigit() or len(parsed_json[key]) != 10):
                    raise ValueError(f"Invalid phone number format in {key}")

            # Store in MongoDB if configured
            if mongo_client and mongo_config.get('enabled', False):
                collection = db[mongo_config['collection']]
                doc = {
                    'iteration': i+1,
                    'data': parsed_json,
                    'status': 'generated'
                }
                collection.insert_one(doc)

            results.append({
                'iteration': i+1,
                'data': parsed_json,
                'status': 'generated'
            })
        except Exception as e:
            results.append({
                'iteration': i+1,
                'error': str(e),
                'status': 'failed'
            })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_mongodb', methods=['POST'])
def configure_mongodb():
    global mongo_client, db
    config = request.json
    try:
        mongo_client = MongoClient(config['connection_string'])
        db = mongo_client[config['database']]
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/run_test', methods=['POST'])
def run_test():
    data = request.json
    config = {
        'endpoint': data['endpoint'],
        'iterations': data['iterations'],
        'template': data['template'],
        'mongo': {
            'enabled': data['mongo_enabled'],
            'collection': data['mongo_collection']
        }
    }
    
    # Generate test data
    test_data = validate_and_generate_data(
        config['template'],
        config['iterations'],
        config['mongo']
    )
    
    # Execute API tests
    results = []
    for item in test_data:
        if item['status'] == 'failed':
            results.append(item)
            continue
            
        try:
            response = requests.post(
                config['endpoint'],
                json=item['data'],
                timeout=5
            )
            
            # Update MongoDB status
            if mongo_client and config['mongo']['enabled']:
                collection = db[config['mongo']['collection']]
                collection.update_one(
                    {'iteration': item['iteration']},
                    {'$set': {
                        'response_status': response.status_code,
                        'response_body': response.text,
                        'status': 'completed'
                    }}
                )
            
            results.append({
                'iteration': item['iteration'],
                'status_code': response.status_code,
                'response': response.text,
                'status': 'completed'
            })
        except Exception as e:
            results.append({
                'iteration': item['iteration'],
                'error': str(e),
                'status': 'failed'
            })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

def vercel_handler(event, context):
    return handle_request(app, event, context)