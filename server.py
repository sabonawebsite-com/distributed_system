from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Flask-RPC-Server")

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    """Return the same message received"""
    data = request.get_json()
    message = data.get('message', '')
    logger.info(f"Echoing message: {message}")
    return jsonify({'result': message})

@app.route('/add', methods=['POST'])
def add_numbers():
    """Add two numbers and return the result"""
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    result = a + b
    logger.info(f"Adding {a} + {b} = {result}")
    return jsonify({'result': result})

@app.route('/subtract', methods=['POST'])
def subtract_numbers():
    """Subtract two numbers and return the result"""
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    result = a - b
    logger.info(f"Subtracting {a} - {b} = {result}")
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply_numbers():
    """Multiply two numbers and return the result"""
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    result = a * b
    logger.info(f"Multiplying {a} * {b} = {result}")
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide_numbers():
    """Divide two numbers and return the result"""
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 1) 
    
    if b == 0:
        logger.error("Division by zero attempted")
        return jsonify({'error': 'Division by zero is not allowed'}), 400
    
    result = a / b
    logger.info(f"Dividing {a} / {b} = {result}")
    return jsonify({'result': result})

@app.route('/info', methods=['GET'])
def get_server_info():
    """Return server information"""
    info = {
        'status': 'running',
        'methods': [
            '/echo (POST)',
            '/add (POST)',
            '/subtract (POST)',
            '/multiply (POST)',
            '/divide (POST)',
            '/info (GET)'
        ],
        'description': 'Flask RPC Server with Calculator Operations'
    }
    logger.info("Returning server info")
    return jsonify(info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)