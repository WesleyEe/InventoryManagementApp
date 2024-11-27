from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pytz
import uuid

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) 

# MySQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Singapore timezone
SGT = pytz.timezone('Asia/Singapore')

# Define the Item model
class Item(db.Model):
    __tablename__ = 'inventory_table'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    last_updated_dt = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Item {self.name}>"

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    time = datetime.now(SGT)

    # Check if item already exists
    item = Item.query.filter_by(name=name).first()
    if item:
        # Update the existing item
        item.price = price 
        item.last_updated_dt = time
        db.session.commit()
        return jsonify({"message": "Item updated", "id": item.id})
    else:
        # Create a new item
        new_item = Item(
            name=name,
            category=category,
            price=price, 
            last_updated_dt=time
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item created", "id": new_item.id}), 201

@app.route('/items', methods=['GET'])
def get_items():
    # Optional filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')

    query = Item.query

    # Apply filters if provided
    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date).astimezone(SGT)
        end_date = datetime.fromisoformat(end_date).astimezone(SGT)
        query = query.filter(Item.last_updated_dt.between(start_date, end_date))
    
    if category:
        query = query.filter_by(category=category)

    # Get all items
    items = query.all()

    # Calculate total price
    total_price = sum(item.price for item in items)

    # Serialize items
    items_data = [{
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': item.price,
        'last_updated_dt': item.last_updated_dt.isoformat()
    } for item in items]


    return jsonify({"items": items_data, "total_price": total_price})

@app.route('/items-filter-page-sort', methods=['POST'])
def get_filtered_items():
    # Get filters, pagination, and sorting options from request body
    data = request.json
    filters = data.get('filters', {})
    pagination = data.get('pagination', {})
    sort = data.get('sort', {})

    # Start query on Item model
    query = Item.query

    # Apply filters
    if filters.get('name'):
        query = query.filter(Item.name.like(f"%{filters['name']}%"))
    
    if filters.get('category'):
        query = query.filter_by(category=filters['category'])
    
    if filters.get('price_range'):
        min_price, max_price = filters['price_range']
        query = query.filter(Item.price.between(min_price, max_price))

    # Sorting: Apply sorting based on field and order
    if sort.get('field') and sort.get('order'):
        field = sort['field']
        order = sort['order']
        
        if order == 'asc':
            query = query.order_by(getattr(Item, field).asc())
        elif order == 'desc':
            query = query.order_by(getattr(Item, field).desc())

    # Pagination: Apply page and limit
    page = pagination.get('page', 1)
    limit = pagination.get('limit', 10)
    query = query.paginate(page=page, per_page=limit, error_out=False)

    # Get results
    items = query.items
    count = query.total

    # Serialize items to include necessary fields
    items_data = [{
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': item.price,
        'last_updated_dt': item.last_updated_dt.isoformat()
    } for item in items]

    # Response with filtered items, pagination info, and total count
    return jsonify({
        'items': items_data,
        'count': count,
        'page': page,
        'limit': limit
    })

if __name__ == '__main__':
    app.run(debug=True)
