from flask import Flask,request,render_template,redirect,url_for,flash
from flask_login import LoginManager,UserMixin
import pymysql


app=Flask(__name__)



db = pymysql.connect(host = "localhost" ,user = "root",password = "vikas",database = "db")


login_manage=LoginManager()
login_manage.init_app(app)

@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self,user_id,name,email):
        self.id=user_id
        self.name=name
        self.email=email
       


    @staticmethod
    def get(user_id):
        db = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "vikas",
        database = "db")

        cursor=db.cursor()
        cursor.execute('SELECT name,email from mypage where id=%s',(user_id))
        result=cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return User(user_id,result[0],result[1])
        

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method==('POST'):
       email= request.form['email']
       password= request.form['password']

       db = pymysql.connect(
       host = "localhost",
       user = "root",
       password = "vikas",
       database = "db")

       cursor=db.cursor()
       cursor.execute('select * from mypage where email = %s AND password = %s',(email,password))
       user_data = cursor.fetchone()
       if user_data:
           return  redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
      name= request.form['name']
      email= request.form['email']
      password= request.form['password']
        
      db = pymysql.connect(
      host = "localhost",
      user = "root",
       password = "vikas",
      database = "db")

    
      cursor=db.cursor()
      cursor.execute('INSERT INTO mypage(name,email,password) values(%s,%s,%s)',(name,email,password))
      db.commit()
      cursor.close()
      db.close()
      return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')

@app.route('/foodblog')
def food():
    return render_template('food_blog.html')

@app.route('/travelblog')
def travel():
    return render_template('travel_blog.html')

@app.route('/personalblog')
def personal():
    return render_template('personal_blog.html')

@app.route('/blogging')
def blogging():
    return render_template('blogging.html')

@app.route('/about')
def about():
    return render_template('about.html')


db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'vikas',
    database = 'db' 
)


@app.route("/adminLogin",methods = ['GET','POST'])
def admin_login():
    if request.method == 'POST':
      username = request.form.get('us')
      password = request.form.get('ps')
      if username == 'dp1234' and password == 'dp2005':
          return  redirect(url_for('admin'))
      
      
      
    
    return render_template("adminlogin.html")
@app.route("/admin")
def admin():
    db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'vikas',
    database = 'db'
)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM mypage")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("admin.html",rows = rows)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db = pymysql.connect(
host = 'localhost',
user = 'root',
password = 'vikas',
database = 'db'
)
    cursor = db.cursor()
    cursor.execute("DELETE FROM mypage WHERE id = %s",(id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/admin')
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    db = pymysql.connect(
host = 'localhost',
user = 'root',
password = 'vikas',
database = 'db'
)
    cur = db.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
         
        name = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('ps')
        

         
        if not all([email, password,  name]):
            return "All fields are required", 400

       
        cur.execute(
           "UPDATE mypage SET name = %s, email= %s, password = %s  WHERE id = %s" , (name,email, password,  id))
        db.commit()

        cur.close()
        db.close()

        return redirect('/admin')
    
    else:
         
        cur.execute('SELECT * FROM mypage WHERE id = %s', (id,))
        user_data = cur.fetchone()

        cur.close()
        db.close()
        
    return render_template("update.html",row = user_data)
@app.route('/add',methods = ['GET','POST'])
def add():
   conn = pymysql.connect(
host = 'localhost',
user = 'root',
password = 'vikas',
database = 'db'
)
   cur = conn.cursor(pymysql.cursors.DictCursor)
   if request.method == 'POST':
         
        name = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('ps')
        

        
        if not all([email, password, name]):
         return "All fields are required", 400

        
        cur.execute("""
            INSERT INTO mypage (email, password, name)
            VALUES (%s, %s, %s)
        """, (email, password,name))
        conn.commit() 

        cur.close()
        conn.close()

        return redirect('/admin')
    
   else: 
        cur.close()
        conn.close() 

        return render_template('add.html')
    



if __name__=='__main__':
    app.run(debug=True)