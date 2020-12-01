from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(8), unique=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#endpoint to create new user
@app.route('/user', methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_user= User(username, email, password)

    db.session.add(new_user)
    db.session.commit()

    user= User.query.get(new_user.id)

    return user_schema.jsonify(user)


#endpoint to query all user
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


#endpoint to query a single user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


#endpoint for updating a user 
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user.username = username
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)


#endpoint for deleting a single user
@app.route('/user/<id>', methods=['DELETE'])
def deleting_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
        
    return user_schema.jsonify(user)


#should be at the end of page

if __name__ == '__main__':
    app.run(debug=True)