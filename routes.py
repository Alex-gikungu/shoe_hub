from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Message, Review, Product, Transaction

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize database
with app.app_context():
    db.create_all()
# Routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the API!'})

# Signup route - POST (Create user), GET (Get all users), PUT (Update user)
@app.route('/signup', methods=['POST', 'GET', 'PUT'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    elif request.method == 'GET':
        users = User.query.all()
        users_list = [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users]
        return jsonify(users_list)

    elif request.method == 'PUT':
        data = request.get_json()
        user = User.query.filter_by(id=data['id']).first()
        if user:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.phone = data['phone']
            user.password = generate_password_hash(data['password'], method='sha256')
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        return jsonify({'message': 'User not found'}), 404


# Login route - POST (Authenticate user)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Message route - POST (Submit message), GET (Get all messages), PUT (Update message)
@app.route('/message', methods=['POST', 'GET', 'PUT'])
def message():
    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(user_id=data['user_id'], content=data['content'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201

    elif request.method == 'GET':
        messages = Message.query.all()
        message_list = [{'id': m.id, 'user_id': m.user_id, 'content': m.content, 'timestamp': m.timestamp} for m in messages]
        return jsonify(message_list)

    elif request.method == 'PUT':
        data = request.get_json()
        message = Message.query.filter_by(id=data['id']).first()
        if message:
            message.content = data['content']
            db.session.commit()
            return jsonify({'message': 'Message updated successfully'}), 200
        return jsonify({'message': 'Message not found'}), 404


# Review route - POST (Submit review), GET (Get all reviews), PUT (Update review)
@app.route('/review', methods=['POST', 'GET', 'PUT'])
def review():
    if request.method == 'POST':
        data = request.get_json()
        new_review = Review(user_id=data['user_id'], rating=data['rating'], comment=data['comment'])
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review submitted successfully'}), 201

    elif request.method == 'GET':
        reviews = Review.query.all()
        review_list = [{'id': r.id, 'user_id': r.user_id, 'rating': r.rating, 'comment': r.comment} for r in reviews]
        return jsonify(review_list)

    elif request.method == 'PUT':
        data = request.get_json()
        review = Review.query.filter_by(id=data['id']).first()
        if review:
            review.rating = data['rating']
            review.comment = data['comment']
            db.session.commit()
            return jsonify({'message': 'Review updated successfully'}), 200
        return jsonify({'message': 'Review not found'}), 404


# Products route - GET (Get all products), POST (Add new product), PUT (Update product)
@app.route('/products', methods=['GET', 'POST', 'PUT'])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        product_list = [{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in products]
        return jsonify(product_list)

    elif request.method == 'POST':
        data = request.get_json()
        new_product = Product(name=data['name'], price=data['price'], description=data['description'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        product = Product.query.filter_by(id=data['id']).first()
        if product:
            product.name = data['name']
            product.price = data['price']
            product.description = data['description']
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        return jsonify({'message': 'Product not found'}), 404


# Transaction route - POST (Record transaction), GET (Get all transactions), PUT (Update transaction)
@app.route('/transaction', methods=['POST', 'GET', 'PUT'])
def transaction():
    if request.method == 'POST':
        data = request.get_json()
        new_transaction = Transaction(user_id=data['user_id'], product_id=data['product_id'])
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction recorded successfully'}), 201

    elif request.method == 'GET':
        transactions = Transaction.query.all()
        transaction_list = [{'id': t.id, 'user_id': t.user_id, 'product_id': t.product_id, 'timestamp': t.timestamp} for t in transactions]
        return jsonify(transaction_list)

    elif request.method == 'PUT':
        data = request.get_json()
        transaction = Transaction.query.filter_by(id=data['id']).first()
        if transaction:
            transaction.product_id = data['product_id']
            db.session.commit()
            return jsonify({'message': 'Transaction updated successfully'}), 200
        return jsonify({'message': 'Transaction not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
