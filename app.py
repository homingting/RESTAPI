
from flask import Flask, request
from flask_smorest import abort
from db import items,stores
import uuid

app = Flask(__name__)



#獲得所有store的資訊
@app.get("/store") #以get方式requst => http://127.0.0.1:5000\store
def get_stores():
    return{"stores":list(stores.values())}

#創造一個store
@app.post("/store") #以post方式requst=> http://127.0.0.1:5000\store 
def create_store():
    store_data = request.get_json() #以json的方式接收
    if "name"  not in store_data :
        abort(404,messsage ="Bad request.Ensure 'name' is include in the Jsin payload",)    
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(404,message = "The store already exists.",)

    store_id = uuid.uuid4().hex #自動編碼16進位函數
    store = {**store_data,"id": store_id}
    stores[store_id] = store
    return store,201

#建立stores裡面的items
@app.post("/item") #以post方式requst => http://127.0.0.1:5000/item
def creat_item():
    item_data = request.get_json() #以json的方式接收
    
    #錯誤處理 有值沒輸入到
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400,message ="Bad request.Ensure 'price','store_id' and 'name' are include in the Jsin payload")
    
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


#獲得指定商店的資訊
@app.get("/store/<string:store_id>") #以get方式進入 http://127.0.0.1:5000\store/<string:store_id>
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError: #假如store_id  not exit 
        abort(404,message = "Store not found") #跑完沒找到就回傳

#獲得所有ITEM
@app.get("/item")
def get_all_items():
    return {"items":list(items.values())} 

#獲得特定ITEM
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message = "Item not found")

#刪除ITEM
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"item deleted sucessfully"},201
    except KeyError:
        abort(404,message = "item not found.")

#更新item(這裡比較不懂，需注意!!!!)
@app.put("/item/<string:item_id>")
def update_item(item_id):
    items_data = request.get_json()
    
    if("price" not in items_data or "name" not in items_data):
        abort(404,messgae ="Bad request.Ensure 'price'and 'name' are include in the Json payload")
    
    try:
        item = items[item_id]
        item |= items_data #將值合併
        return item
    except KeyError:
         abort(404,message="Item not found")
         
#delete store
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"delete store sucessfully"},201
    except KeyError:
        abort(404,message = "item not found.")