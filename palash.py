import requests
import json
import random
import string
import re

def generate_phone_number():
    return ''.join(random.choices(string.digits, k=10))

def main():
    generators = {
        'random_int': lambda: str(random.randint(1, 100)),
        'random_float': lambda: f"{random.random():.4f}",
        'random_string': lambda: ''.join(random.choices(string.ascii_letters, k=10)),
        'phone_number': generate_phone_number,
        'contact_number': generate_phone_number
    }

    endpoint = input("Enter the API endpoint: ").strip()
    if not endpoint.startswith(('http://', 'https://')):
        endpoint = f'http://{endpoint}'
    
    iterations = int(input("Enter the number of iterations: "))
    
    print("\nEnter your JSON template (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "" and (not lines or lines[-1] == ""):
            break
        lines.append(line)
    json_template = '\n'.join(lines)

    pattern = re.compile(r'\{\{(\w+)\}\}')

    for i in range(iterations):
        def replacer(match):
            key = match.group(1)
            return generators.get(key, lambda: match.group(0))()

        try:
            new_body = pattern.sub(replacer, json_template)
            parsed_json = json.loads(new_body)
            
            # Validate phone numbers
            for key in ['phoneNumber', 'refrenceContactFirst', 
                       'refrenceContactSecond', 'refrenceContactThird']:
                if not parsed_json[key].isdigit() or len(parsed_json[key]) != 10:
                    raise ValueError(f"Invalid phone number format in {key}")

            response = requests.post(endpoint, json=parsed_json, timeout=5)
            print(f"\nIteration {i+1}:")
            print(f"Status Code: {response.status_code}")
            try:
                print("Response:", response.json())
            except:
                print("Response:", response.text)
            
        except Exception as e:
            print(f"\nIteration {i+1}: Error - {str(e)}")

if __name__ == "__main__":
    main()
