from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel,StoreModel,ItemModel
from schemas import TagSchema,TagAndItemSchema


blp = Blueprint("Tags","tags",description = "Opreations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        tag = TagModel(**tag_data,store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message = str(e))

        return tag
    

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        else:
            item.tags.append(tag) #treating the tags as list automatically the ItemModel will take care of changes that it needs.
        try:
            db.session.add(item)
            db.session.commit()
        except:
            abort(500,message = "An error ocurred while inserting the tag.")
        return tag
    
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        else:
            item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message= "Aa error occurred while deleting the tag")
        return item


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.alt_response(404,description="Tag not found. " )
    def delete(self,tag_id ):
        tag  = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"Message" : "Tag Deleted."}
        abort(400,message= "Could not delete tag. Make sure tag is not associated with any items first.")