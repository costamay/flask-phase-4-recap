from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt
# from flaks_cors import CORS
from models import *
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

migrate = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
# CORS(app)
api = Api(app)

# jwt error handling

@jwt.expired_token_loader
def jwt_expired_token(jwt_header, jwt_data):
    return make_response({'message': "Token has expired", "error": "token_expired"}, 401)

@jwt.invalid_token_loader
def jwt_invalid_token(error):
    return make_response({'message': 'Invalid token', "error": "invalid_token"}, 401)

@jwt.unauthorized_loader
def missing_token(error):
    return make_response({'message': 'Missing token', "error": "missing_token"}, 401)

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    
    return token is not None


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

class RegisterUser(Resource):
    def post(self):
        data  = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))
        
        if user is not None:
            return make_response({'error': " Username already in use"})
        
        new_user = User(username=data.get('username'), email=data.get('email'))
        new_user.set_password(data.get('password'))
        db.session.add(new_user)
        db.session.commit()
        
        return make_response({'message': 'User created successfully'}, 201)
    
api.add_resource(RegisterUser, '/register')

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        
        user = User.get_user_by_username(username=data.get('username'))
        
        if user and (user.check_password(password=data.get('password'))):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            return make_response({
                "message": "Login successful",
                "tokens" : {
                    "access" :access_token,
                    "refresh" : refresh_token
                }
                                  }, 200)
            
        return make_response({'error': "Invalid username or password"})
    

api.add_resource(LoginUser, '/login')


class LogoutUser(Resource):
    @jwt_required(verify_type=False)
    def get(self):
        jwt = get_jwt()
        jti = jwt['jti']
        token_type = jwt['type']
        
        new_block_list = TokenBlocklist(jti=jti)
        db.session.add(new_block_list)
        db.session.commit()
        
        return make_response({'message': f'{token_type} token revoked successfully'})

api.add_resource(LogoutUser, '/logout')
    
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
@jwt_required()
def posts():
    response = [post.to_dict() for post in Post.query.all()]
    return make_response(response, 200)




@app.route('/')
def index():
    return "Welcome to Flask"








if __name__ == '__main__':
    app.run(port=8080, debug=True)