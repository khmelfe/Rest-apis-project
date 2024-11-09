import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models.store import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from schemas import StoreSchema

#blueprint-> diving the api to multiple segments.
blp = Blueprint("stores",__name__ , description = "Operations on Stores")

# the @blp.route -> connects flask smorest with methodview ,
# so we could access these function when we run request(here is delete and get).
#we put in each class the methods that are associated with the excet url 
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    blp.response(200,StoreSchema)
    def get(self,store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store  deleted."}
#different bip.
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)#schema pass the value as the first parameter
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message ="A store with that name is already exists.")
        except SQLAlchemyError:
            abort(500,message= "An error ocurred creating the store .")
        return store
    