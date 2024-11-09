#schemans.py -> A way to valitate what we need from the json files we get.(without using a lot of "if" statments).

from marshmallow import Schema,fields

#these fields works on both ends,so a client will need these fields to achieve sucess,
#The server will have to send back the item with these fields(in both ways it will return on based what we configured.)

#we made a schema that only makes an item(if we want to make an obj without info on the store.)
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) # dump_only means we don't recive from post request => we won't get it from json
    name = fields.Str(required=True) # this field is required in the json file(hences true)
    price = fields.Float(required = True)


class PlainStoreSchema(Schema):
    id= fields.Str(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    #here a user might sent without info and thats fine,therefore there is not required.
    name = fields.Str() 
    price = fields.Float()
    store_id =fields.Int()


#the idea behiend making plain class is to avoid infinite nesting.
#so we made item schema and store that are inherit from the plain counterpart.
#also this reducess duplications.

#item with connection to store.
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required = True,load_only = True)
    #this field is for returning data to the client and not reciving.
    store = fields.Nested(PlainStoreSchema(),dump_only = "True") 
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only =True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only =True)



class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only = True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only= True)
    store = fields.Nested(PlainStoreSchema(),dump_only = "True") 


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

### users!

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username= fields.Str(required=True)
    #load only => making sure that the client won't get the password! 
    # and stoping the password from being send or saved !
    password = fields.Str(required=True,load_only=True)