from db import db

#making many to many relationships in sqlalchemy.

class ItemTags(db.Model):
    __tablename__= "items_tags"

    id = db.Column(db.Integer,primary_key = True)
    item_id = db.Column(db.Integer,db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"))

    