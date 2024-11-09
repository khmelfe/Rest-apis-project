#import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt
from schemas import ItemSchema,ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema) # returing a code when success response. 
    def get(self, item_id):
       item = ItemModel.query.get_or_404(item_id) #getting the item using the id(will abort with 404 if not there.)
       return item
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message = "Admin privilege required")#the idea is now we use the jwt as a way to make sure if the user is an admin.
        
        item = ItemModel.query.get_or_404(item_id) #getting the item using the id(will abort with 404 if not there.)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted."}
    

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema) # the order of the blps, are important!
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id) 
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id = item_id,**item_data) # if the item doesn't exsists then make one.
        db.session.add(item)
        db.session.commit()
        return item



@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))#because we will check more then one item, we using "many" parameter.
    def get(self):
        return  ItemModel.query.all()#because of schema the response will give us a list as a parameter.
    
    @jwt_required(refresh=True)#Making sure that everytime, a user want to use this function we will ask for token.
    @blp.arguments(ItemSchema)
    #schema will get the item and will valitate,if it is correct it will return it to item_data(in this case)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
       #creating item_model.
       item = ItemModel(**item_data)
       try:
            db.session.add(item) # will validate the item(not written to file.)
            db.session.commit()# will save the item to db if passes validation,
            #commit is also useful if a func is doing a few changes at once and with this line we can commit all the changes at once.
       except SQLAlchemyError:        
            abort(500,message = "An error occurred while inserting the Item.")
       return item