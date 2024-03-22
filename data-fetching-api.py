from flask import Flask, jsonify,url_for
import psycopg2

import parser

app = Flask(__name__)

dbname = 'Resume_Fraud_detetction'
user = 'vbos'
password = '9thApr@)@#'
host = 'vinzintranetdb.postgres.database.azure.com'
port = '5432'


# Function to establish a database connection
def get_db():
    db = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return db

@app.route("/get-parsed-data")  # This is the API route to extract college name from resume
def get_data():
    dict = parser.get_parsed_data() # get_parsed_data() function is defined in the parser.py
    return jsonify(dict)

@app.route("/resume-text-insertion")
def parsed_text_insertion():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()[0]

    print(f"Connected to PostgreSQL server. Server version: ",db_version)
    with app.test_client() as c:
        response = c.get('/get-parsed-data')
        data = response.get_json()
        # data = get_data()
        query = 'INSERT INTO public."Resume_Parsed_Data"("Resume_Name","Resume_data") VALUES(%s,%s)'
        query1 = 'INSERT INTO public."Resume_extracted_details"("Resume_name","College_name","Email_Address","mobile_no","Person_name") VALUES(%s,%s,%s,%s,%s)'
        for obj in data:
            filename = obj['filename']
            college = obj['college']
            email = obj['email']
            mobile_no = obj['mobile_number']
            p_name = obj['name']
            text = obj['resume_text']
            cleaned_text = str(text).replace('\n',' ')

            cursor.execute(query,(filename,cleaned_text))
            cursor.execute(query1,(filename,college,email,mobile_no,p_name))
            db.commit()
        return "data inserted"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
