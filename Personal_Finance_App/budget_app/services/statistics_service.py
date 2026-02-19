from sqlalchemy import func, extract
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from models import Transaction, Category, PaymentMethod
from utils.db import db

class StatisticsService:
    """통계 계산 서비스"""

    @staticmethod
    def get_monthly_summary(year = None, month = None):
        """월별 요약 통계"""
        if year is None or month is None:
            today = datetime.now()
            year = today.year()
            month = today.month()

        # 해당 월의 시작일과 종료일
        first_day = datetime(year, month, 1).date()
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days = 1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days = 1)

        # 수입/지출 계산
        income = db.session.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.transaction_type == 'income',
                Transaction.date >= first_day,
                Transaction.date <= last_day
            ).scalar() or 0
        
        expense = db.session.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.transaction_type == 'expense',
                Transaction.date >= first_day,
                Transaction.date <= last_day
            ).scalar() or 0

        # 고정/변동 지출
        fixed_expense = db.session.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.transaction_type == 'expense',
                Transaction.is_fixed == True,
                Transaction.date >= first_day,
                Transaction.date <= last_day
            ).scalar() or 0
        
        variable_expense = expense - fixed_expense

        return {
            'year': year,
            'month': month,
            'income': income,
            'expense': expense,
            'balance': income - expense,
            'fixed_expense': fixed_expense,
            'variable_expense': variable_expense,
            'savings_rate': round((income - expense) / income * 100, 2) if income > 0 else 0
        }

    @staticmethod
    def get_yearly_summary(year = None):
        """연도별 요약 통계"""
        if year is None:
            year = datetime.now().year
        
        first_day = datetime(year, 1, 1).date()
        last_day = datetime(year, 12, 31).date()

        income = db.session.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.transaction_type == 'income',
                Transaction.date >= first_day,
                Transaction.date <= last_day
            ).scalar() or 0
        
        expense = db.session.query(func.sum(Transaction.amount))\
            .filter(
                Transaction.transaction_type == 'expense',
                Transaction.date >= first_day,
                Transaction.date <= last_day,
            ).scalar() or 0
        
        return {
            'year': year,
            'income': income,
            'expense': expense,
            'balance': income - expense
        }
    
    @staticmethod
    def get_monthly_trend(months = 12):
        """월별 트렌드 (최근 N개월)"""
        results = []
        today = datetime.now()

        for i in range(months - 1, -1, -1):
            target_date = today - relativedelta(months = i)
            year = target_date.year
            month = target_date.month

            summary = StatisticsService.get_monthly_summary(year, month)
            results.append({
                'label': f'{year}-{month:02d}',
                'year': year,
                'month': month,
                'income': summary['income'],
                'expense': summary['expense'],
                'balance': summary['balance']
            })

        return results
    
    @staticmethod
    def get_category_analysis(transaction_type = 'expense', year = None, month = None):
        """카테고리 별 분석"""
        query = db.session.query(
            Category.category_id,
            Category.name,
            Category.color,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.transaction_id).label('count')
        ).join(Transaction)\
        .filter(Transaction.transaction_type == transaction_type)

        # 기간 필터
        if year and month:
            first_day = datetime(year, month, 1).date()
            if month == 12:
                last_day = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
            else:
                last_day = datetime(year, month + 1, 1).date() - timedelta(days = 1)
            
            query = query.filter(
                Transaction.date >= first_day,
                Transaction.date <= last_day
            )
        
        results = query.group_by(Category.category_id)\
                        .order_by(func.sum(Transaction.amount).desc()).all()
        
        total_amount = sum(r.total for r in results)

        return [{
            'category_id': r.category_id,
            'name': r.name,
            'color': r.color,
            'total': r.total,
            'count': r.count,
            'percentage': round(r.total / total_amount * 100, 1) if total_amount > 0 else 0
        } for r in results]
    
    @staticmethod
    def get_payment_method_analysis(year = None, month = None):
        """결제수단 별 분석"""
        query = db.session.query(
            PaymentMethod.payment_method_id,
            PaymentMethod.name,
            PaymentMethod.payment_method_type,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.transaction_id).label('count')
        ).join(Transaction)

        # 기간 필터
        if year and month:
            first_day = datetime(year, month, 1).date()
            if month == 12:
                last_day = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
            else:
                last_day = datetime(year, month + 1, 1).date() - timedelta(days = 1)

            query = query.filter(
                Transaction.date >= first_day,
                Transaction.date <= last_day,
                Transaction.transaction_type == 'expense'
            )
        
        results = query.group_by(PaymentMethod.payment_method_id)\
                        .order_by(func.sum(Transaction.amount).desc()).all()
        
        total_amount = sum(r.total for r in results)

        return [{
            'payment_method_id': r.payment_method_id,
            'name': r.name,
            'type': r.payment_method_type,
            'total': r.total,
            'count': r.count,
            'percentage': round(r.total / total_amount * 100, 1) if total_amount > 0 else 0
        } for r in results]
    
    @staticmethod
    def get_daily_expenses(year, month):
        """일별 지출 (히트맵용)"""
        first_day = datetime(year, month, 1).date()
        if month == 12:
            last_day = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
        else:
            last_day = datetime(year, month + 1, 1).date() - timedelta(days = 1)

        results = db.session.query(
            Transaction.date,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.transaction_type == 'expense',
            Transaction.date >= first_day,
            Transaction.date <= last_day
        ).group_by(Transaction.date)\
        .all()

        # transform into dictionary
        daily_data = {r.date.day: r.total for r in results}

        return daily_data
    
    @staticmethod
    def get_fixed_vs_variable(year = None, month = None):
        """고정지출 vs 변동지출"""
        query_base = db.session.query(func.sum(Transaction.amount))\
                                .filter(Transaction.transaction_type == 'expense')
        
        if year and month:
            first_day = datetime(year, month, 1).date()
            if month == 12:
                last_day = datetime(year + 1, 1, 1).date() - timedelta(days = 1)
            else:
                last_day = datetime(year, month + 1, 1).date() - timedelta(days = 1)

            query_base = query_base.filter(
                Transaction.date >= first_day,
                Transaction.date <= last_day
            )

        fixed = query_base.filter(Transaction.is_fixed == True).scalar() or 0
        # total = query_base.scalar() or 0
        variable = query_base.filter(Transaction.is_fixed == False).scalar() or 0
        # variable = total - fixed
        total = fixed + variable

        print(fixed, variable, total)

        return {
            'fixed': fixed,
            'variable': variable,
            'total': total,
            'fixed_percentage': round(fixed / total * 100, 1) if total > 0 else 0,
            'variable_percentage':round(variable / total * 100, 1) if total > 0 else 0
        }