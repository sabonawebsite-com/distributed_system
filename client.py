from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
client = None

class FlaskRPCClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def echo(self, message):
        url = f"{self.base_url}/echo"
        payload = {"message": message}
        response = requests.post(url, json=payload)
        return self._handle_response(response)
    
    def add(self, a, b):
        url = f"{self.base_url}/add"
        payload = {"a": a, "b": b}
        response = requests.post(url, json=payload)
        return self._handle_response(response)
    
    def subtract(self, a, b):
        url = f"{self.base_url}/subtract"
        payload = {"a": a, "b": b}
        response = requests.post(url, json=payload)
        return self._handle_response(response)
    
    def multiply(self, a, b):
        url = f"{self.base_url}/multiply"
        payload = {"a": a, "b": b}
        response = requests.post(url, json=payload)
        return self._handle_response(response)
    
    def divide(self, a, b):
        url = f"{self.base_url}/divide"
        payload = {"a": a, "b": b}
        response = requests.post(url, json=payload)
        return self._handle_response(response)
    
    def info(self):
        url = f"{self.base_url}/info"
        response = requests.get(url)
        return self._handle_response(response)
    
    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            try:
                return response.json()
            except:
                return {"error": str(err)}
        except requests.exceptions.RequestException as err:
            return {"error": str(err)}

@app.before_request
def initialize_client():
    global client
    client = FlaskRPCClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/echo', methods=['GET', 'POST'])
def echo():
    if request.method == 'POST':
        message = request.form['message']
        result = client.echo(message)
        return render_template('echo.html', result=result, message=message)
    return render_template('echo.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        operation = request.form['operation']
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            
            if operation == 'add':
                result = client.add(a, b)
            elif operation == 'subtract':
                result = client.subtract(a, b)
            elif operation == 'multiply':
                result = client.multiply(a, b)
            elif operation == 'divide':
                result = client.divide(a, b)
            
            return render_template('calculator.html', 
                                 result=result.get('result', 'Error'),
                                 a=a, b=b, operation=operation)
        except ValueError:
            return render_template('calculator.html', 
                                 error="Please enter valid numbers")
        except Exception as e:
            return render_template('calculator.html', 
                                 error=str(e))
    
    return render_template('calculator.html')

@app.route('/info')
def info():
    server_info = client.info()
    return render_template('info.html', info=server_info)

if __name__ == '__main__':
    app.run(port=5000, debug=True)