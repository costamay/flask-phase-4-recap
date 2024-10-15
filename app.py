from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recap.db"

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        response=  [user.to_dict() for user in User.query.all() ]
        
        return make_response(response, 200)
    
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        
        return make_response({"message" : "Success"}, 200)
    
    
@app.route('/users/<int:id>/', methods=['DELETE', 'PATCH', 'GET'])
def user(id):
    if request.method == 'GET':
        user  = User.query.get(id)
        return make_response(user.to_dict(), 200)

@app.route('/posts', methods=['POST', 'GET'])
def posts():
    response = [post.to_dict() for post in Post.query.all()]
    return make_response(response, 200)




@app.route('/')
def index():
    return "Welcome to Flask"








if __name__ == '__main__':
    app.run(port=8080, debug=True)