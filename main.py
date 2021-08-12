from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello World, This is a test of the web browser."

app.run()