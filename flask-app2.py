#app.py
from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from datetime import datetime

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan-2020"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '722_Jaisn'
app.config['MYSQL_DB'] = 'netflix_data_inputs'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def main():
    return redirect('/useradmin')

@app.route('/useradmin')
def useradmin():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM netflix_details_1")
    employee = cur.fetchall()
    return render_template('dataframe_example.html', employee=employee)

@app.route('/updateemployee', methods=['POST'])
def updateemployee():
        pk = request.form['director']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if name == 'director':
           cur.execute("UPDATE employee SET name = %s WHERE id = %s ", (value, pk))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})

if __name__ == '__main__':
    app.run(debug=True)
