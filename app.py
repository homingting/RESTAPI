from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

#獲得所有store的資訊
@app.get("/store") #以get方式requst => http://127.0.0.1:5000\store
def get_stores():
    return {"stores": stores},201 #回傳stores裡面所有東西

#創造一個store
@app.post("/store") #以post方式requst=> http://127.0.0.1:5000\store 
def create_store():
    request_data = request.get_json() #以json的方式接收
    new_store = {"name": request_data["name"], "items": []} #以new_store存取輸入
    stores.append(new_store) #將new_store值放入stores裡面
    return new_store, 201 #回傳new_store的值，並且回傳201表示成功了!

#建立stores裡面的items
@app.post("/store/<string:name>/item") #以post方式requst => http://127.0.0.1:5000\store/<string:name>/item
def creat_item(name):
    request_data = request.get_json() #以json的方式接收
    for store in stores:
        if store["name"] == name: #確認是否有這個store
            new_item = {"name":request_data["name"],"price":request_data["price"]} #將相對應值放入
            store["items"].append(new_item) #將new_items存入store
            return new_item, 201 #回傳new_item 和 201 並且結束
    return {"message":"Store not found"}, 404 #若迴圈都跑完了還沒結束，則回傳{"message":"Store not found"} 這個json

#獲得指定商店的資訊
@app.get("/store/<string:name>") #以get方式進入 http://127.0.0.1:5000\store/<string:name>
def get_store(name):
    for store in stores: #把所有store跑過一次
        if store["name"] == name : #若跟 <string:name> 一樣就回傳store的值
            return {"all store imformation": store},201
    return {"message":"Store not found"}, 404 #跑完沒找到就回傳

#獲得指定商店的品項(和上面差不多只差有沒有顯示出store名稱)
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"all items": store["items"]},201
    return {"message":"Store is not found"}, 404