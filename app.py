import secrets
import os
#jesonify help here with jwd token error handling
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

from flask_migrate import Migrate

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

from db import db
import models

#factory pattern -> so we won't need to make app.py for each flask app
def create_app(db_url =None):
    app = Flask(__name__)

    #configurations
    #"PROPAGATE_EXCEPTIONS" -> flask config , if the is exceptions that happens in flask extension we would it to move to main app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    #flask_smorest configurations 
    #Version and title of the apies
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"]  = "v1"
    #to tell flask smorest with version of api to use.
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"]  = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
   
    #db configurations.
    #config for our db. os.getenv->will try to access DATABASE_URL enviromnent var, and if not found will use sqlite.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    db.init_app(app) # this line connects betwenn flask and sqlalchemy.
    migrate = Migrate(app,db)
    #Api -> connects the flask smorest extension to our flask app.
    api = Api(app) 
    

    #JWT CONFIGURARTIONS
    app.config["JWT_SECRET_KEY"] = "95171970091299291929580618563867485451" #used secrets.SystemRandom().getrandbits(128)
    
    #app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128)) # making a secret key. this key is used to signing the JWTS.
    #JWT uses the secret key so that when a user sends us JWT to tell us who he is 
    # the app can use it to verify that the app made that JWT hence if the app did, 
    # then JWT IS VALID
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
        #if we return true , then the token is revoked.

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )
    
    @jwt.additional_claims_loader
    #we can added more information to the token themself, for example if the user is an admin or not.
    def add_claims_to_jwt(identity):
        # this is an example , in reality we should make sure that the id matchs the database,to make sure that 1 is for admin.
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


    # @decrpted => using flask migrate.
    #with app.app_context():
       # db.create_all() #creating the table, before all the requests.(runs if there is zero tables)

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)




    return app


