from flask import Blueprint, reneder_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import Transaction, Category, PaymentMethod
from utils.db import db

"""
Trasaction CRUD (Create, Read, Update, Delete) Routes
"""

transaction_bp = Blueprint('transaction', __name__, url_prefix = '/transactions')

@transaction_bp.route('/add', methods = ['GET', 'POST'])
def add():
    """
    Add a New Transaction
    """

    if request.method == 'POST':
        try:
            transaction = Transaction(
                user_id = 1,  # 임시 사용자 ID, Phase 1에서는 고정
                date = datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                desctription = request.form['description'],
                transaction_type = request.form['transaction_type'],
                amount = int(request.form['amount']),
                category_id = int(request.form['category_id']),
                payment_method_id = int(request.form['payment_method_id']),
                is_fixed = request.form.get('is_fixed') == 'on',
                memo = request.form.get('memo', '')
            )
            
            db.session.add(transaction)
            db.session.commit()

            flash('거래가 추가되었습니다!!', 'success')
            return redirect(url_for('transaction.list'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'오류가 발생했습니다.: {str(e)}', 'danger')