from db import db

#this class is mapping between a row in a a table to a python class
class ItemModel(db.Model):
    __tablename__ ="items" #creating a table for this class.

    id = db.Column(db.Integer,primary_key = True) # defining the columns

    name = db.Column(db.String(80),unique = True,nullable = False) # unique items + no null items.

    description = db.Column(db.String)

    price = db.Column(db.Float(precision =2),unique = False,nullable =False)

    #db.ForignKEY-> tells that this column is maps to stores.id
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"),unique = False,nullable = False)
    #relationshoips ->connects the item to the store id we want.
    #back_pop -> will help us to see what items are connect to the store(confi ->store_model)
    store =db.relationship("StoreModel",back_populates="items")
    tags = db.relationship("TagModel",back_populates = "items",secondary = "items_tags")