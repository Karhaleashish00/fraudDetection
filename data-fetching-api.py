from flask import Flask, jsonify
import parser

app = Flask(__name__)


@app.route("/get-parsed-data")  # This is the API route to extract college name from resume
def get_data():
    dict = parser.get_parsed_data() # get_parsed_data() function is defined in the parser.py
    return dict


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
