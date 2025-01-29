import requests
import json
import random
import string
import uuid
import re

def main():
    # Define generators for different placeholder types
    generators = {
        'random_int': lambda: str(random.randint(1, 100)),
        'random_float': lambda: f"{random.random():.4f}",
        'random_string': lambda: ''.join(random.choices(string.ascii_letters, k=10)),
        'uuid': lambda: str(uuid.uuid4()),
        'boolean': lambda: 'true' if random.choice([True, False]) else 'false'
    }

    # Get user inputs
    endpoint = input("Enter the API endpoint: ").strip()
    iterations = int(input("Enter the number of iterations: "))
    
    print("\nEnter your JSON template (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            if not lines:
                continue  # Skip initial empty lines
            break
        lines.append(line)
    json_template = '\n'.join(lines)

    # Compile regex pattern to find placeholders
    pattern = re.compile(r'\{\{(\w+)\}\}')

    # Process each iteration
    for i in range(iterations):
        # Replace placeholders with generated values
        def replacer(match):
            key = match.group(1)
            return generators.get(key, lambda: match.group(0))()

        try:
            # Generate new JSON body
            new_body = pattern.sub(replacer, json_template)
            parsed_json = json.loads(new_body)
            
            # Send POST request
            response = requests.post(endpoint, json=parsed_json)
            print(f"\nIteration {i+1}:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
        except json.JSONDecodeError as e:
            print(f"\nIteration {i+1}: Invalid JSON generated - {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f"\nIteration {i+1}: Request failed - {str(e)}")

if __name__ == "__main__":
    main()
