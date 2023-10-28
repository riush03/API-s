from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

#instance of a flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ == 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)

    def __init__(self):
        return {'id':self.id,
                'username':self.username,
                'email':self.email}

#intialize the database
db.create_all()

#test rour
@app.route('/test',methods=['GET'])
def test():
    return make_response(jsonify({'message':'test route'}),200)

#to create a user we need to make a POST request withe the body
@app.route('/users',methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'],
                        email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message':"User created succeffully!"}),201)
    except e:
        return make_response(jsonify({'message':"Error while creating user!"}),500)
    
#get all users
@app_route('/users',methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if len(users):
            return make_response(jsonify({'users':[user.json() for user in users]}),200)
        #return make_response(jsonify({'message':"No user found!"}),404)
    except e:
        return make_response(jsonify({'message':"Error while getting users!"}),500)
    
#get users by id
@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user':user.json()}),201)
        return make_response(jsonify({'message':"User not found!"}),404)
    except e:
        return make_response(jsonify({'message':"Error getting user!"}),500)
    
#to update the user we will use the PUT request
@app.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message':"User updated successfully!"}),200)
        return make_response(jsonify({'message':"User not found!"}),404)
    except e:
        return make_response(jsonify({'message':"Error while updating user!"}),500)
    
#to delete an user we use the DELETE request
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message':"Use deleted!"}),200)
        return make_response(jsonify({'message':"User not found!"}),404)
    except e:
        return make_response(jsonify({'message':"Error while deleting user!"}),500)