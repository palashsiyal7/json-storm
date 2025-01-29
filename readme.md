How to use:

    Run the script

    Enter the API endpoint URL when prompted

    Enter the number of iterations you want

    Enter your JSON template with placeholders (see below)

    Press Enter twice to finish JSON input


Example JSON template:

{
    "user": "{{random_string}}",
    "age": {{random_int}},
    "active": {{boolean}},
    "uuid": "{{uuid}}",
    "score": {{random_float}}
}


Placeholder options:

    {{random_int}}: Random integer between 1-100

    {{random_float}}: Random float between 0-1

    {{random_string}}: 10-character random string

    {{uuid}}: UUID v4 string

    {{boolean}}: Random boolean (true/false)

Features:

    Validates JSON before sending

    Shows status code and response for each request

    Handles network errors gracefully

    Preserves unknown placeholders in the template

Note: Make sure your JSON template is valid except for the placeholders. The script will automatically convert placeholders to appropriate values based on the placeholder name.
