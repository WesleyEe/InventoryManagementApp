from flask import request, jsonify
from datetime import datetime
from config import SGT
from .db import db
from .models import Item

def register_routes(app):
    @app.route("/item", methods=["POST"])
    def add_item():
        data = request.json
        name = data.get("name")
        category = data.get("category")
        price = data.get("price")
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
                name=name, category=category, price=price, last_updated_dt=time
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message": "Item created", "id": new_item.id}), 201

    @app.route("/items", methods=["GET"])
    def get_items():
        # Optional filters
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        category = request.args.get("category")

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
        items_data = [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "price": item.price,
                "last_updated_dt": item.last_updated_dt.isoformat(),
            }
            for item in items
        ]

        return jsonify({"items": items_data, "total_price": total_price})

    @app.route("/items-filter-page-sort", methods=["POST"])
    def get_filtered_items():
        # Get filters, pagination, and sorting options from request body
        data = request.json
        filters = data.get("filters", {})
        pagination = data.get("pagination", {})
        sort = data.get("sort", {})

        # Start query on Item model
        query = Item.query

        # Apply filters
        if filters.get("name"):
            query = query.filter(Item.name.like(f"%{filters['name']}%"))

        if filters.get("category"):
            query = query.filter_by(category=filters["category"])

        if filters.get("price_range"):
            min_price, max_price = filters["price_range"]
            query = query.filter(Item.price.between(min_price, max_price))

        # Sorting: Apply sorting based on field and order
        if sort.get("field") and sort.get("order"):
            field = sort["field"]
            order = sort["order"]

            if order == "asc":
                query = query.order_by(getattr(Item, field).asc())
            elif order == "desc":
                query = query.order_by(getattr(Item, field).desc())

        # Pagination: Apply pagination based on page and size
        if pagination.get("page") and pagination.get("size"):
            page = pagination["page"]
            size = pagination["size"]
            query = query.paginate(page, size, False)

        # Get items
        items = query.all()

        # Calculate total price
        total_price = sum(item.price for item in items)

        # Serialize items
        items_data = [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "price": item.price,
                "last_updated_dt": item.last_updated_dt.isoformat(),
            }
            for item in items
        ]

        return jsonify({"items": items_data, "total_price": total_price})
