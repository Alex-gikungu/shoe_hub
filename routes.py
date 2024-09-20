from flask import jsonify, request
from app import app, db
from flask_cors import CORS
from models import User, Message, Review, Product, Transaction

CORS(app)
@app.route('/')
def home():
    return 'Welcome to the API'
# Route to get all users
## Get Method 
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [{'id': user.id, 'first_name': user.first_name, 
                         'last_name': user.last_name, 'email': user.email, 
                         'phone': user.phone} for user in users]
    return jsonify({'users': serialized_users})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('first_name', 'last_name', 'email', 'phone')):
        return jsonify({'error': 'Missing fields'}), 400

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created', 'id': new_user.id}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted'}), 204

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    serialized_user = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone
    }
    return jsonify({'user': serialized_user})


@app.route('/messages', methods=['GET'])
def get_all_messages():
    messages = Message.query.all()
    serialized_messages = [{'id': message.id, 'user_id': message.user_id, 
                            'content': message.content, 'timestamp': message.timestamp} 
                           for message in messages]
    return jsonify({'messages': serialized_messages})

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_id', 'content')):
        return jsonify({'error': 'Missing fields'}), 400

    new_message = Message(
        user_id=data['user_id'],
        content=data['content']
    )
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'message': 'Message created', 'id': new_message.id}), 201

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()
    
    return jsonify({'message': 'Message deleted'}), 204


@app.route('/reviews', methods=['GET'])
def get_all_reviews():
    reviews = Review.query.all()
    serialized_reviews = [{'id': review.id, 'user_id': review.user_id, 
                            'comment': review.comment, 
                           'rating': review.rating} 
                          for review in reviews]
    return jsonify({'reviews': serialized_reviews})

@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_id', 'product_id', 'comment', 'rating')):
        return jsonify({'error': 'Missing fields'}), 400

    new_review = Review(
        user_id=data['user_id'],
        product_id=data['product_id'],
        comment=data['comment'],
        rating=data['rating']
    )
    db.session.add(new_review)
    db.session.commit()
    
    return jsonify({'message': 'Review created', 'id': new_review.id}), 201

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted'}), 204


@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    serialized_products = [{'id': product.id, 'name': product.name, 
                            'price': product.price, 'description': product.description} 
                           for product in products]
    return jsonify({'products': serialized_products})

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'price')):
        return jsonify({'error': 'Missing fields'}), 400

    new_product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description')  # Optional
    )
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'message': 'Product created', 'id': new_product.id}), 201

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted'}), 204


@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()
    serialized_transactions = [{
        'id': transaction.id,
        'user_id': transaction.user_id,
        'product_id': transaction.product_id,
        'timestamp': transaction.timestamp.isoformat()
    } for transaction in transactions]
    return jsonify({'transactions': serialized_transactions})

@app.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_id', 'product_id')):
        return jsonify({'error': 'Missing fields'}), 400

    new_transaction = Transaction(
        user_id=data['user_id'],
        product_id=data['product_id']
    )
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({'message': 'Transaction created', 'id': new_transaction.id}), 201

@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify({'message': 'Transaction deleted'}), 204
