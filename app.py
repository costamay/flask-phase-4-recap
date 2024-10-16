from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recap.db"

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# @app.route('/users', methods=['POST', 'GET'])
# def users():
#     if request.method == 'GET':
#         response=  [user.to_dict() for user in User.query.all() ]
        
#         return make_response(response, 200)
    
#     if request.method == 'POST':
#         data = request.get_json()
#         new_user = User(username=data['username'], email=data['email'])
#         db.session.add(new_user)
#         db.session.commit()
        
#         return make_response(new_user.to_dict(), 201)
    
    
# @app.route('/users/<int:id>', methods=['DELETE', 'PATCH', 'GET'])
# def user(id):
#     if request.method == 'GET':
#         user  = User.query.get(id)
#         if not user:
#             return make_response({"message": "User not found"}, 404)
#         return make_response(user.to_dict(), 200)
    
#     if request.method == 'DELETE':
#         user  = User.query.get(id)
#         if not user:
#             return make_response({"message": "User not found"}, 404)
#         db.session.delete(user)
#         db.session.commit()
        
#         return make_response({"message": "user deleted successfully"}, 200)
    
#     if request.method == "PATCH":
#         user  = User.query.get(id)
#         if not user:
#             return make_response({"message": "User not found"}, 404)
        
#         data = request.get_json()
#         print(data)
#         for attr in request.get_json():
#             setattr(user, attr, request.get_json().get(attr))
            
#         db.session.add(user)
#         db.session.commit()
            
#         return make_response(user.to_dict(), 200)
    
# RestfulAPI
class UserResouce(Resource):
    def get(self, id=None):
        if id is None:
            response =  [user.to_dict() for user in User.query.all() ]
            return make_response(response, 200)
        
        user  = User.query.get(id)
        if not user:
            return make_response({"message": "User not found"}, 404)
        return make_response(user.to_dict(), 200)  
    
    def post(self): 
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        
        return make_response(new_user.to_dict(), 201) 
    
    def delete(self, id):
        pass
    
    def patch(self, id):
        pass
            
    
api.add_resource(UserResouce, '/users', '/users/<int:id>')
        
        
        
        
     

@app.route('/posts', methods=['POST', 'GET'])
def posts():
    response = [post.to_dict() for post in Post.query.all()]
    return make_response(response, 200)




@app.route('/')
def index():
    return "Welcome to Flask"








if __name__ == '__main__':
    app.run(port=8080, debug=True)