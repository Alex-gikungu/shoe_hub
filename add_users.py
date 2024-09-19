# add_users.py
from app import app
from models import db, User, Message, Transaction, Product, Review

# Initialize the app and database
with app.app_context():
    db.create_all()  # Create tables if they don't exist

    # Add users with a phone number
    user1 = User(first_name="John", last_name="Doe", email="jon@example.com", phone="1453367890", password="password123")
    user2 = User(first_name="Jane", last_name="Smith", email="je@example.com", phone="0956654321", password="password456")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Add messages
    message1 = Message(user_id=1, content="Hello, this is a message from John.")
    message2 = Message(user_id=2, content="Hi, this is a message from Jane.")
    
    db.session.add(message1)
    db.session.add(message2)

    # Add products
    product1 = Product(name="Product 1", price=29.99, description="Description of Product 1")
    product2 = Product(name="Product 2", price=49.99, description="Description of Product 2")
    
    db.session.add(product1)
    db.session.add(product2)

    # Add reviews
    review1 = Review(user_id=1, rating=5, comment="Great product!")
    review2 = Review(user_id=2, rating=4, comment="Good quality, but could be better.")
    
    db.session.add(review1)
    db.session.add(review2)

    # Add transactions
    transaction1 = Transaction(user_id=1, product_id=1)
    transaction2 = Transaction(user_id=2, product_id=2)
    
    db.session.add(transaction1)
    db.session.add(transaction2)

    # Commit all changes
    db.session.commit()

    print("Users, messages, products, reviews, and transactions added successfully!")
