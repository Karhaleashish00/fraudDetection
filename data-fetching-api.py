import psycopg2
from flask import Flask, jsonify

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

@app.route("/get-parsed-data")  # This is the API route to extract all the details from resume
def get_data():
    dict = parser.get_parsed_data() # get_parsed_data() function is defined in the parser.py
    return jsonify(dict)


@app.route("/fetch-details") # this route fetch users details from database add returns a json object
def fetch_details():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * from "Resume_extracted_details"')
    rows = cursor.fetchall()
    cursor.close()
    data = [{'Id':row[0],'Resume_name':row[1],'College_name':row[2],'Email_address':row[3],'Mobile_no':row[4],'Person_name':row[5]}for row in rows]
    return jsonify(data)


@app.route("/resume-text-insertion") # This route fetch the data from route/get-parsed-data add insert into the database
def parsed_text_insertion():
    db = get_db()
    cursor = db.cursor()
    # {{1st commnent}}
    with app.test_client() as c:
        response = c.get('/get-parsed-data')
        data = response.get_json()
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

            try:
                cursor.execute(query,(filename,cleaned_text))
                cursor.execute(query1,(filename,college,email,mobile_no,p_name))
                db.commit()
            except:
                pass

        return "data inserted"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# 1st comment:
         # cursor.execute("SELECT version();")
            # db_version = cursor.fetchone()[0]
            #
            # print(f"Connected to PostgreSQL server. Server version: ",db_version)