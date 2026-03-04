from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import logging
from models import Transaction, Category, PaymentMethod
from utils.db import db

"""
Trasaction CRUD (Create, Read, Update, Delete) Routes
"""

transaction_bp = Blueprint('transaction', __name__, url_prefix = '/transactions')
"""
Blueprint는 flask에서 라우트 관련 함수들을 그룹화하여 관리할 수 있도록 도와주는 모듈임
"""

@transaction_bp.route('/')
@login_required
def list():
    """
    거래 내역 목록
    """

    # 필터 파라미터
    transaction_type = request.args.get('transaction_type', '')  # 'income' 또는 'expense' 또는 ''
    category_id = request.args.get('category_id', '')  # category_id를 Key 값으로 데이터를 바로 조회
    payment_method_id = request.args.get('payment_method_id', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    search = request.args.get('search', '')  # ?

    # 기본 쿼리 - 사용자 필터 추가
    query = Transaction.query.filter(Transaction.user_id == current_user.user_id)

    # 필터 적용
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)

    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    if payment_method_id:
        query = query.filter(Transaction.payment_method_id == payment_method_id)
    
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    if search:
        query = query.filter(
            (Transaction.description.like(f'%{search}%')) |
            (Transaction.memo.like(f'%{search}%'))
        )

    # 정렬 및 조회
    transactions = query.order_by(
        Transaction.date.desc(),
        Transaction.created_at.desc()
    ).all()

    # 필터용 데이터
    categories = Category.query.filter(Category.user_id == current_user.user_id).order_by(Category.category_type, Category.name).all()
    payment_methods = PaymentMethod.query.filter(PaymentMethod.user_id == current_user.user_id).order_by(PaymentMethod.name).all()

    # 통계용 데이터
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')

    return render_template('transaction/list.html',
                           transactions = transactions,
                           categories = categories,
                           payment_methods = payment_methods,
                           total_income = total_income,
                           total_expense = total_expense,
                           balance = total_income - total_expense,
                           filters = {
                               'transaction_type': transaction_type,
                               'category': category_id,
                               'payment_method': payment_method_id,
                               'start_date': start_date,
                               'end_date': end_date,
                               'search': search
                           })

@transaction_bp.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    """
    Add a New Transaction
    """

    if request.method == 'POST':
        # 받은 데이터 확인
        logging.info(f"From Data: {request.form}")

        try:
            transaction = Transaction(
                user_id = current_user.user_id,  # 현재 사용자 ID
                date = datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                description = request.form['description'],
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
            logging.error(f"Error details: {str(e)}", exc_info = True)
            db.session.rollback()
            flash(f'오류가 발생했습니다.: {str(e)}', 'danger')

    # GET 요청
    categories = Category.query.filter(Category.user_id == current_user.user_id).order_by(Category.category_type, Category.name).all()
    payment_methods = PaymentMethod.query.filter(PaymentMethod.user_id == current_user.user_id).order_by(PaymentMethod.name).all()

    return render_template('transaction/add.html',
                           categories = categories,
                           payment_methods = payment_methods,
                           today = datetime.now().strftime('%Y-%m-%d'))

@transaction_bp.route('/edit/<int:transaction_id>', methods = ['GET', 'POST'])
@login_required
def edit(transaction_id):
    """거래 내역 수정"""

    transaction = Transaction.query.filter_by(
        transaction_id = transaction_id,
        user_id = current_user.user_id
    ).get_or_404(transaction_id)

    if request.method == 'POST':
        try:
            transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            transaction.description = request.form['description']
            transaction.transaction_type = request.form['transaction_type']
            transaction.amount = request.form['amount']
            transaction.category_id = int(request.form['category_id'])
            transaction.payment_method_id = int(request.form['payment_method_id'])
            transaction.is_fixed = request.form.get('is_fixed') == 'on'
            transaction.memo = request.form.get('memo', '')
        
            db.session.commit()

            flash('거래가 수정되었습니다!', 'success!')
            return redirect(url_for('transaction.list'))

        except Exception as e:
            db.session.rollback()
            flash(f'오류가 발생했습니다: {str(e)}', 'error')

    # GET 요청
    categories = Category.query.filter(Category.user_id == current_user.user_id).order_by(Category.category_type, Category.name).all()
    payment_methods = PaymentMethod.query.filter(PaymentMethod.user_id == current_user.user_id).order_by(PaymentMethod.name).all()

    return render_template('transaction/edit.html',
                           transaction = transaction,
                           categories = categories,
                           payment_methods = payment_methods)

@transaction_bp.route('/delete/<int:transaction_id>', methods = ['POST'])
@login_required
def delete(transaction_id):
    """거래 내역 삭제"""

    try:
        transaction = Transaction.query.filter_by(
            transaction_id = transaction_id,
            user_id = current_user.id
        ).get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()

        flash('거래가 삭제되었습니다!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('transacction.list'))