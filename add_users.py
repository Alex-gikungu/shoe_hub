from app import app, db
from models import User, Message, Review, Product, Transaction
from datetime import datetime

# Push the app context to allow database operations
with app.app_context():
    db.create_all()  # Create tables if they don't exist

    # Add users
    user1 = User(first_name='Alex', last_name='Gikungu', email='alex@example.com', phone='123456789', password='password123')
    user2 = User(first_name='Jane', last_name='Doe', email='jane@example.com', phone='987654321', password='password123')
    
    db.session.add(user1)
    db.session.add(user2)

    # Add products
    product1 = Product(name='Product 1', price=19.99, description='Description for product 1')
    product2 = Product(name='Product 2', price=29.99, description='Description for product 2')
    
    db.session.add(product1)
    db.session.add(product2)

    # Add messages
    message1 = Message(user_id=1, content='Hello, this is a message.', timestamp=datetime.now())
    message2 = Message(user_id=2, content='Hi, another message here.', timestamp=datetime.now())
    
    db.session.add(message1)
    db.session.add(message2)

    # Add reviews
    review1 = Review(user_id=1, rating=5, comment='Great product!')
    review2 = Review(user_id=2, rating=4, comment='Very good service.')

    db.session.add(review1)
    db.session.add(review2)

    # Add transactions
    transaction1 = Transaction(user_id=1, product_id=1, timestamp=datetime.now())
    transaction2 = Transaction(user_id=2, product_id=2, timestamp=datetime.now())
    
    db.session.add(transaction1)
    db.session.add(transaction2)

    # Commit the session to save all the data
    db.session.commit()

    print("Database populated with initial data successfully!")
