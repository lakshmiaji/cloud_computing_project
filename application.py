from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

application = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
application.config['MYSQL_HOST'] = db['mysql_host']
application.config['MYSQL_USER'] = db['mysql_user']
application.config['MYSQL_PASSWORD'] = db['mysql_password']
application.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(application)
@application.route('/')
def form1():
    return render_template('registration_form.html')

@application.route('/search',methods=['GET', 'POST'])
def search():
    title="Search"
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        field=request.form.get("field")
        search =request.form.get("value1")
        value = "%" + f"%{search}%".lower() + "%"
        if field=="first_name":
            cur.execute("SELECT * FROM students where first_name LIKE %(value)s ", {"value": value})
        elif field=="college":
            cur.execute("SELECT * FROM students where college LIKE %(value)s ", {"value": value})
        elif field=="course":
            cur.execute("SELECT * FROM students where course LIKE %(value)s ", {"value": value})
        # cur.execute("SELECT * FROM students where first_name LIKE %(value)s ", {"value":value})

        studentDetails = cur.fetchall()
        return render_template('search.html', studentDetails=studentDetails)

    return render_template('search.html',title=title)

@application.route('/form', methods=['POST'])
def form():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Fetch form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        college = request.form["college"]
        course = request.form["course"]
        email = request.form["email"]
        gender = request.form["gender"]
        state = request.form["state"]
        city = request.form["city"]

        if gender=="Male":
            g="Male"
        else:
            g="Female"
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO students(first_name,last_name,college,course,email,gender,state,city) VALUES(%s, %s,%s, %s,%s, %s,%s, %s)",
                    (first_name,last_name,college,course,email,g,state,city))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('registration_form.html')


if __name__ == '__main__':
    application.run(debug=True)