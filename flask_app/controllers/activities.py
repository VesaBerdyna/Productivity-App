from cmath import log
from flask import render_template,redirect,session,request, flash   
from flask_app import app
from flask_app.models.activity import Activity
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    activities = Activity.get_all()
    return render_template("dashboard.html",user=user, activities= activities)

@app.route('/activities/new')
def new_activity_form():  
    if 'user_id' not in session:
        return redirect('/logout')
    user_date = {
    'id' : session['user_id']
    }    
    user = User.get_by_id(user_date)
    return render_template("create_activity.html",user=user)

@app.route('/activities/create',methods=['POST'])
def create_activity(): 
    if not Activity.validate_create(request.form):
        return redirect('/dashboard')
    Activity.create(request.form)
    return redirect("/dashboard")

@app.route('/activities/<int:id>')
def show_activity(id): 
    if 'user_id' not in session:
        return redirect('/logout') 
    user_date = {
     'id' : session['user_id']
    }    
    user = User.get_by_id(user_date) 
    activity_data = {
      'id' : id
    }    
    activity = Activity.get_one(activity_data)
    favoritedActivities = Activity.get_all_favorited_activities_by_user(user_date)
    print(favoritedActivities)
    return render_template("show_activity.html",activity=activity,user=user,favoritedActivities =favoritedActivities)  


@app.route('/activities/<int:id>/edit')
def show_edit_form(id):
    user_date = {
      'id' : session['user_id']
    }    
    user = User.get_by_id(user_date) 
    activity_data = {
      'id' : id
    } 
    activity = Activity.get_one(activity_data)
    if activity.user_id != user.id:
      flash(f'Unathorized access to edit activity with id {id}!')
      return redirect("/dashboard")

    return render_template("edit_activity.html",activity=activity,user=user)  

@app.route('/activities/<int:id>/update',methods=['POST'])
def update_activity(id):
    if not Activity.validate_create(request.form):
        return redirect(f'/activities/{id}/edit')
    Activity.update(request.form)
    return redirect("/dashboard")

@app.route('/activities/<int:id>/delete',methods=['POST'])
def delete_activity(id):
    activity_data = {
      'id' : id
    } 
    activity = Activity.get_one(activity_data)
    if activity.user_id != session["user_id"]:
        flash(f'Unathorized access to delete activity with id {id}!')
        return redirect("/dashboard")
    Activity.delete(request.form)
    return redirect("/dashboard")

@app.route('/activities/<int:id>/favorite',methods=['POST'])
def favorite_activity(id):  
    Activity.favorite(request.form)  
    return redirect("/dashboard")

@app.route('/activities/<int:id>/unfavorite',methods=['POST'])
def unfavorite_activity(id):  
    Activity.unfavorite(request.form)  
    return redirect("/dashboard")