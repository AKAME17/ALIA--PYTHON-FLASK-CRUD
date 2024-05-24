# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>" 

# if __name__== "__main__":
#     app.run(debug= True)  


from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sitedata"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

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
SELECT course_name.courseid, course_name.coursename 
FROM itstudent
INNER JOIN course_enrollees
ON itstudent.studentnumber = course_enrollees.studentnumber
INNER JOIN course_name
ON course_enrollees.courseid = course_name.courseid
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

if __name__ == "__main__":
    app.run(debug=True) 