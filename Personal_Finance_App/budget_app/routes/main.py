from flask import Blueprint, render_template, request
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from models import Transaction, Category, PaymentMethod
from utils.db import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Main Dashboard
    """

    # 현재 월의 시작일과 종료일
    today = datetime.now()
    first_day = today.replace(day = 1)
    if today.month == 12:
        last_day = today.replace(year = today.year + 1, month = 1, day = 1) - timedelta(days = 1)
    else:
        last_day = today.replace(month = today.month + 1, day = 1) - timedelta(days = 1)

    # 이번 달 수입/지출 계산
    month_income = db.session.query(func.sum(Transaction.amount))\
        .filter(
            Transaction.transaction_type == 'income',
            Transaction.date >= first_day.date(),
            Transaction.date <= last_day.date()
        ).scalar() or 0
    
    month_expense = db.session.query(func.sum(Transaction.amout))\
        .filter(
            Transaction.transaction_type == 'expense',
            Transaction.date >= first_day.date(),
            Transaction.date <= last_day.date()
        ).scalar() or 0
    
    # 전체 수입/지출 계산
    total_income = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.transaction_type == 'income').scalar() or 0
    total_expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.transaction_type == 'expense').scalar() or 0
    
    # 최근 거래 내역 (10개)
    recent_ten_transactions = Transaction.query\
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())\
        .limit(10).all()
    
    # 상위 카테고리별 지출 (10개)
    top_categories = db.session.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label('amount_sum')
    ).join(Transaction)\
    .filter(
        Transaction.transaction_type == 'expense',
        Transaction.date >= first_day.date(),
        Transaction.date <= last_day.date()
        # extract('month', Transaction.date) == today.month,
        # extract('year', Transaction.date) == today.year
    ).group_by(Category.category_id)\
    .order_by(func.sum(Transaction.amount).desc())\
    .limit(10)\
    .all()

    return render_template('index.html',
                            month_income = month_income,
                            month_expense = month_expense,
                            month_balance = month_income - month_expense,
                            total_income = total_income,
                            total_expense = total_expense,
                            total_balance = total_expense - total_income,
                            recent_ten_transactions = recent_ten_transactions,
                            top_categories = top_categories,
                            current_month = today.strftime('%Y년 %m월')
                           )