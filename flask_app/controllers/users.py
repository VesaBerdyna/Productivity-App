from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def show_register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/register')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register_user(data)
    session['user_id'] = id
    flash('Registration was successful!')
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_user_by_email(request.form)

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
        
    session['user_id'] = user.id
    flash('Login was successful!')
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')