from flask import Flask, jsonify
from utils import get_resources


app = Flask(__name__)


@app.route('/data', methods=['GET'])
def api_get_user():
    return jsonify(get_resources())


if __name__ == '__main__':
    app.run(debug=True, port=8080)
