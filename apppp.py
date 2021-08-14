# Dependency
from flask import Flask

# Create a new falask instance
# https://www.geeksforgeeks.org/dunder-magic-methods-python/
app = Flask(__name__)

# Define the root
@app.route('/')
def hello_world():
    return 'Hello world'