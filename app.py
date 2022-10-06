

from flask import Flask, request, render_template, redirect
import gunicorn
import mysql.connector

app = Flask(__name__)

# Production Database connection
my_db = mysql.connector.connect(
  host="containers-us-west-73.railway.app",
  user="root",
  password="TwZIkrviFo7Jvajm1eIh",
  database="railway"
)
mycursor = my_db.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS mytodos (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), dueDate VARCHAR(255), status VARCHAR(255))")


@app.route('/')
def home():
    sql = "SELECT id,name,dueDate,status FROM mytodos"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        list =""
    else:
        list=myresult

    return render_template("home.html", user='', list=list)

@app.route("/add", methods=['POST', 'GET'])
def add():
  if request.method == 'POST':
    name = request.form.get('name')
    dueDate = request.form.get('duedate')
    status = "Not Done"
    
    sql = "INSERT INTO mytodos(name,dueDate,status) VALUES (%s, %s, %s)"
    values =[name,dueDate,status]
    mycursor.execute(sql, values)

    my_db.commit()

    return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    
    sql = "DELETE FROM mytodos WHERE id= %s"
    value = (id,)

    mycursor.execute(sql, value)
    my_db.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  
  if request.method == 'POST':
    name = request.form.get('name')
    dueDate = request.form.get('duedate')
    status = request.form.get('status')
    
    sql = "UPDATE mytodos SET name= %s, dueDate= %s, status= %s WHERE id= %s"
    values = (name, dueDate, status, id)
    mycursor.execute(sql, values)

    my_db.commit()

    return redirect("/")
  else:
    sql = "SELECT id,name,dueDate,status FROM mytodos WHERE id= %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchone()

    return render_template('edit.html', user='', task=myresult)

if __name__ == '__main__':
    app.run()


