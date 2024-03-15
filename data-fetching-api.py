from flask import Flask, jsonify
import parser


app = Flask(__name__)

@app.route('/get-parsed-data')
def get_parse_data():
    dict = parser.get_parsed_data()
    return dict


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')