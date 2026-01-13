#!/usr/bin/env python3

#!/usr/bin/env python3
#!/usr/bin/env python3

from flask import Flask, request, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# -------------------------
# GET ROUTES
# -------------------------

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries]), 200


@app.route('/baked_goods')
def get_baked_goods():
    baked_goods = BakedGood.query.all()
    return jsonify([bg.to_dict() for bg in baked_goods]), 200


# -------------------------
# POST /baked_goods
# -------------------------

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    baked_good = BakedGood(
        name=request.form['name'],
        price=request.form['price'],
        bakery_id=request.form['bakery_id']
    )

    db.session.add(baked_good)
    db.session.commit()

    return jsonify(baked_good.to_dict()), 201


# -------------------------
# PATCH /bakeries/<int:id>
# -------------------------

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if 'name' in request.form:
        bakery.name = request.form['name']

    db.session.commit()
    return jsonify(bakery.to_dict()), 200


# -------------------------
# DELETE /baked_goods/<int:id>
# -------------------------

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good deleted successfully"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
