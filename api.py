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

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sitedata"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@auth.verify_password
def security(username, password):
    return username == "NelyzaAlia"
    return password == "IPT123"

@app.route("/security")
@auth.login_required
def security_measure():
    return jsonify({"message": "you are authorized to acces this API applocation "})


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/itstudent", methods=["GET"])
def get_itstudent():
    data = data_fetch("""select * from itstudent""")
    return make_response(jsonify(data), 200)

@app.route("/itstudent/<int:id>", methods=["GET"])
def get_itstudent_by_(id):
    data = data_fetch("""select * from itstudent where studentnumber = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/itstudent/<int:id>/courses", methods=["GET"])
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

@app.route("/itstudent", methods=["POST"]) 
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

@app.route("/itstudent/<int:id>", methods=["PUT"])
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


@app.route("/itstudent/<int:id>", methods=["DELETE"])
def delete_itstudent(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM itstudent where studentnumber = %s""", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "student deleted successfully", "rows_affected": rows_affected}), 200)

@app.route("/itstudent/format", methods= ["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('bbbb')
    return make_response(jsonify({"format": fmt}))
if __name__ == "__main__":
    app.run(debug=True) 