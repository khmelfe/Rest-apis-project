from flask.views import MethodView
from flask_smorest import Blueprint,abort
 #hash algorthem.
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

#creating an token.
from flask_jwt_extended import create_access_token, get_jwt, jwt_required ,get_jwt_identity,create_refresh_token
#revoking tokens.
from blocklist import BLOCKLIST

blp = Blueprint("Users","users" , description = "Opreations on users")


@blp.route("/register")#creating an account.
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409,message = "A user with that name already exists")
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        
        db.session.add(user)
        db.session.commit()   
        return {"message":"User Created Successfully"},201
    
@blp.route("/login") #authentications
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(identity=user.id) #refresh.
            return {"access_token":access_token,"refresh_token":refresh_token}#if user is valided he will receive a token.
        
        abort(401,message = "Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) #this operations means we need a refresh token not an access one.
    def post(self):
        current_user = get_jwt_identity() 
        new_token = create_access_token(identity=current_user,fresh=False) #fresh =false => because we don't want new refreshed token.
        #here we making sure that the client can ask only once for a refresh token
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return{"access_token":new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out. "}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"},200
    
