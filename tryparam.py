from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sitedata"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['JWT_Secret_KEY'] = 'your_jwt_secret_key'

mysql = MySQL(app)

def data_fetch(query, params=()):
    # Replace with your actual database connection and fetching logic
    try:
        connection = mysql.connect('sitedata.db')
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route("/itstudent/<string:id>", methods=["GET"])
def get_itstudent_by_id(id):
    data = data_fetch("SELECT * FROM itstudent WHERE studentnumber = ?", (id,))
    if data:
        return make_response(jsonify(data), 200)
    else:
        abort(404, description="Student not found")

if __name__ == "__main__":
    app.run(debug=True)