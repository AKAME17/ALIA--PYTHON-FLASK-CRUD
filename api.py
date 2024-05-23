from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" 

if __name__== "__main__":
    app.run(debug= True)  


# from flask import Flask, make_response, jsonify, request
# from flask_mysqldb import MySQL
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

