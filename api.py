# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>" 

# if __name__== "__main__":
#     app.run(debug= True)  

from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

#flask setup and data base
app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sitedata"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#security function 

@auth.verify_password
def security(username, password):
    return username == "NelyzaAlia"
    return password == "IPT123"

#Security API endpoint 
@app.route("/security")
@auth.login_required
def security_measure():
    return jsonify({"message": "you are authorized to acces this API applocation "})


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#helper funtions 
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

#formatting function 
def dict_to_xml(data):
    xml = ['<root>']
    for item in data:
        xml.append('<item>')
        for key, value in item.items():
            xml.append(f'<{key}>{value}</{key}>')
        xml.append('</item>')
    xml.append('</root>')
    return ''.join(xml)


def output_format(data, format):
    if format == 'xml':
        xml_data = dict_to_xml(data)
        response = make_response(xml_data, 200)
        response.headers["Content-Type"] = "application/xml"
    else:  # Default to JSON
        response = make_response(jsonify(data), 200)
        response.headers["Content-Type"] = "application/json"
    return response
# GET student endpoints

@app.route("/itstudent", methods=["GET"])
@auth.login_required
def get_itstudent():
    format = request.args.get('format', 'json')
    data = data_fetch("""select * from itstudent""")
    return output_format(data, format)

@app.route("/itstudent/<int:id>", methods=["GET"])
@auth.login_required
def get_itstudent_by_(id):
    format = request.args.get('format', 'json')
    data = data_fetch("""select * from itstudent where studentnumber = {}""".format(id))
    return output_format(data, format)



#get courses  y student endpoint 
@app.route("/itstudent/<int:id>/courses", methods=["GET"])
@auth.login_required
def get_course_by_itstudent (id):

    data = data_fetch("""
SELECT courses_name.courseid, courses_name.coursename 
FROM itstudent
INNER JOIN course_enrolled
ON itstudent.studentnumber = course_enrolled.studentnumber
INNER JOIN courses_name
ON course_enrolled.course_id = courses_name.courseid
where itstudent.studentnumber = {}""".format(id))
    return make_response(jsonify({"Student number": id, "count": len(data), "courses": data}), 200)

#post student endpoint 
@app.route("/itstudent", methods=["POST"]) 
@auth.login_required
def add_itstudent():
    cur = mysql.connection.cursor()
    info = request.get_json()
    fullname = info ["fullname"]
    studentnumber = info ["studentnumber"]
    address = info ["address"]
    yearandblock = info ["yearandblock"]
    units = info ["units"]
    cur.execute(
        """ INSERT INTO itstudent (fullname, studentnumber, address, yearandblock, units) VALUE (%s, %s, %s, %s, %s)""", 
        (fullname, studentnumber, address, yearandblock, units),
    )

    mysql.connection.commit()
    print("Row(s) affected: {}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Student added successfully", "rows_affected": rows_affected}), 201)

#put student endpoint 
@app.route("/itstudent/<int:id>", methods=["PUT"])
@auth.login_required
def update_itstudent(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    fullname = info ["fullname"]
    address = info ["address"]
    yearandblock = info ["yearandblock"]
    units = info ["units"]
    cur.execute(
        """ UPDATE itstudent SET fullname =%s, address =  %s, yearandblock =%s, units = %s WHERE studentnumber =%s """, 
        (fullname, address, yearandblock, units, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()


    return make_response(jsonify({"Message": "itstudent added successfully", "rows_affected": rows_affected}), 201)

#Delete student endpoint 
@app.route("/itstudent/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_itstudent(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM itstudent where studentnumber = %s""", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student deleted successfully", "rows_affected": rows_affected}), 200)


#main execution

if __name__ == "__main__":
    app.run(debug=True) 