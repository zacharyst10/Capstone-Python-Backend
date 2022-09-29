from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import os

app = Flask(__name__)
CORS(app)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://gvonrcurugclxl:e0372921977ec611807c8fd971e1ebbab11b497afe14c1e09021702094ca02e8@ec2-54-91-223-99.compute-1.amazonaws.com:5432/df7snlolbiee27"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    item_img = db.Column(db.String, unique=True)

    def __init__(self, title, item_img):
        self.title = title
        self.item_img = item_img

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'item_img')

item_schema = ItemSchema()
multi_item_schema = ItemSchema(many=True)



# GET ALL

@app.route('/item/get', methods=["GET"])
def get_all_items():
    all_records = db.session.query(Item).all()
    return jsonify(multi_item_schema.dump(all_records))



#GET BY ID

@app.route('/item/get/<id>', methods=["GET"])
def get_item_id(id):
    one_item = db.session.query(Item).filter(Item.id == id).first()
    return jsonify(item_schema.dump(one_item))



#ADD TO DATABASE

@app.route('/item/add', methods=["POST"])
def add_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Please send as JSON')

    post_data = request.get_json()
    title = post_data.get('title')
    item_img = post_data.get('item_img')

    if title == None:
        return jsonify("Error: You must provide an 'Item Title' key")
    if item_img == None:
        return jsonify("Error: You must provide a 'Picture' key")

    new_record = Item(title, item_img)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(item_schema.dump(new_record))

# Delete Items

@app.route('/item/delete/<id>', methods=["DELETE"])
def item_to_delete(id):
    delete_item = db.session.query(Item).filter(Item.id == id).first()
    db.session.delete(delete_item)
    db.session.commit()
    return jsonify("Item Deleted")


if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask

# app = Flask(__name__)

# @app.route("/images")
# def images():
#     return {"images": ["Image1"] }


