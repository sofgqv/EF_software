from flask import Flask, request, jsonify
from datetime import datetime
from models import *

app = Flask(__name__)

if __name__ == "__main__":
    app.run()
