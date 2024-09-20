import re
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(128))

    def __init__(self, first_name, last_name, email, phone, password):
        self.first_name = self.validate_first_name(first_name)
        self.last_name = self.validate_last_name(last_name)
        self.email = self.validate_email(email)
        self.phone = self.validate_phone(phone)
        self.password = self.validate_password(password)

    def validate_first_name(self, first_name):
        if not first_name[0].isupper():
            raise ValueError("First name must start with a capital letter.")
        return first_name

    def validate_last_name(self, last_name):
        if not last_name[0].isupper():
            raise ValueError("Last name must start with a capital letter.")
        return last_name

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Email must be in a valid format.")
        return email

    def validate_phone(self, phone):
        if not re.match(r'^\d{10}$', phone):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if password.lower() == self.first_name.lower() or password.lower() == self.last_name.lower():
            raise ValueError("Password cannot be the same as the first or last name.")
        return password


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    timestamp = db.Column(db.DateTime)
