from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# 創建一個陣列(創一個名為apple物品當測試)，存放品項
items = [
    {
        "name": "apple",
        "price": 10
    },
    {
        "name": "banana",
        "price": 20
    }
]

class Item(Resource):

    #get查詢已有資料
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}

    #post未有選項
    def post(self, name):
        #若已存在就回傳
        if next(filter(lambda x: x['name'] == name, items), None): 
            return {'meg': f'{name} 已存在'}
        #若不存在則新增
        data = request.get_json() #取得用戶回饋數據
        item = {'name': name, 'price': data['price']}
        items.append(item)
        y=sorted(items,key=lambda x:x["name"]) #把name降冪排列
        return y

    #put更新資料
    def put(self,name):
        #判斷是否已存在
        if next(filter(lambda x: x['name'] == name, items), None):
            data = request.get_json()
            item = data['price'] #取得新price

            find = [it for it in items if it['name'] == name]#找到位置
            find[0]["price"]=item #變更價錢
            items[items.index(next(filter(lambda x: x['name'] == name, items), None))]=find[0] #用index找到要更新的目標後更新items
            y=sorted(items,key=lambda x:x["name"]) 
            return y


    def delete(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            find = [it for it in  items if it['name'] == name]
            items.pop(items.index(find[0]))
            
            return items
            


class ItemsList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemsList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)