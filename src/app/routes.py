from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Inventory, Order, OrderItem
from . import db
from datetime import datetime
from decimal import Decimal

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@main_bp.route('/products')
@login_required
def products():
    items = Inventory.query.all()
    return render_template('products.html', items=items)

@main_bp.route('/order/<int:item_id>', methods=['GET', 'POST'])
@login_required
def order(item_id):
    item = Inventory.query.get_or_404(item_id)
    if item.available_quantity <= 0:
        return "Out of stock", 400

    if request.method == 'POST':
        qty = int(request.form['quantity'])

        if qty > item.available_quantity:
            return "Not enough stock", 400

        order = Order(
            user_id=current_user.id,
            order_date=datetime.utcnow(),
            status='pending',
            total=item.unit_price * qty
        )

        db.session.add(order)
        db.session.flush()  # order.id available before commit

        order_item = OrderItem(
            order_id=order.id,
            product_name=item.product_name,
            requested_quantity=qty,
            unit_price=item.unit_price
        )

        item.available_quantity -= qty

        db.session.add(order_item)
        db.session.commit()

        return redirect(url_for('main.products'))

    return render_template('order.html', item=item)
