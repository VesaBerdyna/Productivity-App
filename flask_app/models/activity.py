from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Activity:
    db = "productivity_app"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.priority = data['priority']
        self.status = data['status']
        self.date = data['date']
        self.time_est = data['time_est']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.users_who_favorited = []
        self.user_ids_who_favorited = []

    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM activities JOIN users AS creators ON activities.user_id = creators.id
        LEFT JOIN favorites ON activities.id = favorites.activity_id 
        LEFT JOIN  users AS users_who_favorited ON favorites.user_id = users_who_favorited.id;'''
        results = connectToMySQL(cls.db).query_db(query)
        activities = []
        for row in results:
            new_activity = True
            users_who_favorited_data = {
                'id' : row['users_who_favorited.id'],
                'first_name' : row['users_who_favorited.first_name'],
                'last_name' : row['users_who_favorited.last_name'],
                'email' : row['users_who_favorited.email'],
                'password' : row['users_who_favorited.password'],
                'created_at' : row['users_who_favorited.created_at'],
                'updated_at' : row['users_who_favorited.updated_at'],
            }

            number_of_activities = len(activities)

            if number_of_activities > 0:
                last_activity = activities[number_of_activities-1]
                if last_activity.id == row['id']:
                    last_activity.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    last_activity.users_who_favorited.append(User(users_who_favorited_data))
                    new_activity = False

            if new_activity:
                activity = cls(row)
                user_data = {
                    'id' : row['creators.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['creators.created_at'],
                    'updated_at' : row['creators.updated_at'],
                }

                creator = User(user_data)
                activity.creator = creator

                if row['users_who_favorited.id']:
                    activity.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    activity.users_who_favorited.append(User(users_who_favorited_data))

                activities.append(activity)

        return activities


    @classmethod
    def get_one(cls,data):
        query = '''
        SELECT * FROM activities JOIN users AS creators ON activities.user_id = creators.id
        LEFT JOIN favorites ON activities.id = favorites.activity_id 
        LEFT JOIN  users AS users_who_favorited ON favorites.user_id = users_who_favorited.id WHERE activities.id = %(id)s;'''

        results = connectToMySQL(cls.db).query_db(query,data)

        if len(results) < 1:
            return False
        
        new_activity = True
        for row in results:
            if new_activity:
                activity = cls(row)

                user_data = {
                    'id' : row['creators.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['creators.created_at'],
                    'updated_at' : row['creators.updated_at'],
                }
                creator = User(user_data)
                activity.creator = creator
                new_activity = False

            if row['users_who_favorited.id']:
                users_who_favorited_data = {
                    'id' : row['users_who_favorited.id'],
                    'first_name' : row['users_who_favorited.first_name'],
                    'last_name' : row['users_who_favorited.last_name'],
                    'email' : row['users_who_favorited.email'],
                    'password' : row['users_who_favorited.password'],
                    'created_at' : row['users_who_favorited.created_at'],
                    'updated_at' : row['users_who_favorited.updated_at'],
                }
                users_who_favorited = User(users_who_favorited_data)
                activity.users_who_favorited.append(users_who_favorited)
                activity.user_ids_who_favorited.append(row['users_who_favorited.id'])

        return activity

    @classmethod
    def get_all_favorited_activities_by_user(cls,data):
        query = '''SELECT * FROM favorites JOIN users AS creators ON favorites.user_id = creators.id
        LEFT JOIN activities ON activities.id = favorites.activity_id 
        LEFT JOIN  users AS users_who_favorited ON favorites.user_id = users_who_favorited.id WHERE creators.id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query,data)
        activities = []
        for row in results:
            new_activity = True
            users_who_favorited_data = {
                'id' : row['users_who_favorited.id'],
                'first_name' : row['users_who_favorited.first_name'],
                'last_name' : row['users_who_favorited.last_name'],
                'email' : row['users_who_favorited.email'],
                'password' : row['users_who_favorited.password'],
                'created_at' : row['users_who_favorited.created_at'],
                'updated_at' : row['users_who_favorited.updated_at'],
            }

            number_of_activities = len(activities)

            if number_of_activities > 0:
                last_activity = activities[number_of_activities-1]
                if last_activity.id == row['id']:
                    last_activity.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    last_activity.users_who_favorited.append(User(users_who_favorited_data))
                    new_activity = False

            if new_activity:
                activity = cls(row)
                user_data = {
                    'id' : row['creators.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['creators.created_at'],
                    'updated_at' : row['creators.updated_at'],
                }

                creator = User(user_data)
                activity.creator = creator

                if row['users_who_favorited.id']:
                    activity.user_ids_who_favorited.append(row['users_who_favorited.id'])
                    activity.users_who_favorited.append(User(users_who_favorited_data))

                activities.append(activity)

        return activities
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO activities (name,priority, status, date,time_est,user_id) VALUES(%(name)s,%(priority)s,%(status)s,%(date)s,%(time_est)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE activities SET name = %(name)s,priority = %(priority)s ,status = %(status)s,date = %(date)s,time_est = %(time_est)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM activities WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def favorite(cls,data):
        query = "INSERT INTO favorites(user_id,activity_id) VALUES(%(user_id)s,%(id)s);"
        return connectToMySQL(cls.db).query_db(query,data)   

    @classmethod
    def unfavorite(cls,data):
        query = "DELETE FROM favorites WHERE user_id = %(user_id)s AND activity_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)  

    @staticmethod
    def validate_create(activity):
        is_valid = True  
        if len(activity['name']) < 2:
            flash("Activity name must be at least 2 character","error")
            is_valid= False
        if len(activity['priority']) < 2:
            flash("Priority must be at least 2 character","error")
            is_valid= False
        if len(activity['status']) < 2:
            flash("Status must be at least 2 character","error")
            is_valid= False
        if len(activity["date"]) <= 0:
            flash("Date is required.")
            is_valid = False
        if len(activity['time_est']) < 1:
            flash("Time estimation must be at least 1 character","error")
            is_valid= False
        return is_valid


  
   