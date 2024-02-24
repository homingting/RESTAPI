import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores",__name__,description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError: #假如store_id  not exit 
            abort(404,message = "Store not found") 
    
    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message":"delete store sucessfully"},201
        except KeyError:
            abort(404,message = "item not found.")
            
@blp.route("/store")
class storeslist(MethodView):
    @blp.response(201,StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):   
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404,message = "The store already exists.",)

        store_id = uuid.uuid4().hex #自動編碼16進位函數
        store = {**store_data,"id": store_id}
        stores[store_id] = store
        
        return store