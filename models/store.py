from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique = True,nullable = False)
    #using back_pop on both side, sql knows that they end to end relationships
    #lazy = dynamic -> means the store won't fetch the items unless we tell it so.(no prefetch)
    # cascade -> will delete all the items that are associated with this store.

    items = db.relationship("ItemModel",back_populates = "store",lazy= "dynamic",cascade = "all,delete")
    tags = db.relationship("TagModel",back_populates = "store",lazy= "dynamic")