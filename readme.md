# API Testing Tool

## Overview
This project is an API Testing Tool that allows users to configure API requests, generate test data, and validate responses. The tool supports MongoDB integration for storing test data and results. It is built using Flask for the backend and a Bootstrap-based frontend.

## Features
- Generate random test data (integers, floats, strings, phone numbers, etc.)
- Validate and send API requests
- Store API responses in MongoDB
- Simple UI for easy configuration
- Supports multiple test iterations

## Technologies Used
- **Backend:** Flask, Python
- **Frontend:** HTML, Bootstrap, JavaScript
- **Database:** MongoDB (optional)
- **Libraries:**
  - Flask
  - Pymongo
  - Requests
  - Random & String (for test data generation)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- MongoDB (if using database storage)
- Pip (Python package manager)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/palashsiyal7/json-storm.git
   cd json-storm
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open the frontend in a browser:
   ```bash
   http://127.0.0.1:3000
   ```

## Usage
1. Configure MongoDB settings (optional) in the UI.
2. Define test data mappings.
3. Paste a JSON template for API requests.
4. Set API endpoint and iterations.
5. Run tests and view responses.

## Endpoints
- `/` - Serves the frontend UI.
- `/configure_mongodb` - Configures MongoDB settings.
- `/run_test` - Executes API tests.

## Contribution
Feel free to contribute by submitting pull requests or reporting issues on [GitHub](https://github.com/palashsiyal7/json-storm).

## License
MIT License

---
**Author:** Palash

