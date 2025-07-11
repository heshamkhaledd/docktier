from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    address = db.Column(JSONB, nullable=False)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), unique=True, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order_items = db.relationship(
        'OrderItem',
        backref='inventory_item',
        lazy=True,
        cascade='all, delete-orphan',
        foreign_keys='OrderItem.product_name',
        primaryjoin='Inventory.product_name==OrderItem.product_name'
    )


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Text, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('pending', 'transporting', 'delivered', 'cancelled', 'out of stock')"
        ),
    )

    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_name = db.Column(db.String(255), db.ForeignKey('inventory.product_name', ondelete='CASCADE'), nullable=False)
    requested_quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
