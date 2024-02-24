import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items",__name__,description="Operation on items")

@blp.route("/item/<string:item_id>")
class item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,message = "Item not found")
    
    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message":"item deleted sucessfully"},201
        except KeyError:
            abort(404,message = "item not found.")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data #將值合併

            return item
        except KeyError:
            abort(404,message="Item not found")

@blp.route("/item")
class itemlist(MethodView):
    @blp.response(200, ItemSchema(many = True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema) #由函數來確認輸入值是否正確
    @blp.response(201,ItemSchema)
    def post(self, item_data):
        
        #錯誤處理 品項重複
        for item in items.values():
            if(
                item_data["name"] == item["name"] and
                item_data["store_id"] == item["store_id"]
            ):
                abort(400,message = f"The item already exists")
    
        item_id = uuid.uuid4().hex
        item = {**item_data,"id":item_id}
        items[item_id] = item
        
        return item,201
