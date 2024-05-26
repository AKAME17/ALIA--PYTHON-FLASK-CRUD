FLASK API IT STUDENT MANAGEMENT This Flask application provides a simple API for managing IT students information and their courses.

Installation
~ Clone the repository git clone (git link) 
~ Navigate to the project directory: cd flask-itstudent-api 
~ Install the required dependencies: pip install flask flask-MySQLdb
~Set up the SQL database: Ensure MYSQL is installed and running on your computer Create a new data name sitedata or download and import the sql file provided in the repository.

Usage
~ Start Flask server: run the python file on the visual studio or on the command line [python api.py] 
~Access the API using the following endpoints: "/itstudent": Get list of all IT students using the GET method. "/itstudent": Add new student record using the POST method. "/itstudent/int:id": GET, UPDATE or DELETE a specific student using their student number (Primary key) using the [GET, PUT, DELETE] method
"/itstudent/int:id/courses": Get a list of all courses enrolled by a specific student using the GET method.

NOTE: I use postman application to access, but similar application might run the code as well
