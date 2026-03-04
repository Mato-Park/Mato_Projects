from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from services.statistics_service import StatisticsService
from services.analysis_service import AnalysisService
import json

dashboard_bp = Blueprint('dashboard', __name__, url_prefix = '/dashboard')

@dashboard_bp.route('/')
@login_required
def overview():
    """전체 대시보드"""

    # 현재 날짜
    today = datetime.now()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    # 월별 요약
    monthly_summary = StatisticsService.get_monthly_summary(year, month, current_user.user_id)

    # 월별 트렌드 (최근 12개월)
    monthly_trend = StatisticsService.get_monthly_trend(12, current_user.user_id)

    # 카테고리별 분석 (지출)
    expense_categories = StatisticsService.get_category_analysis('expense', year, month, current_user.user_id)

    # 카테고리별 분석 (수입)
    income_categories = StatisticsService.get_category_analysis('income', year, month, current_user.user_id)

    # 결제수단 별 분석
    payment_methods = StatisticsService.get_payment_method_analysis(year, month, current_user.user_id)

    # 고정지출 vs 변동지출
    fixed_vs_variable = StatisticsService.get_fixed_vs_variable(year, month, current_user.user_id)

    # 일별지출
    daily_expenses = StatisticsService.get_daily_expenses(year, month, current_user.user_id)

    return render_template('dashboard/overview.html',
                           year = year,
                           month = month,
                           monthly_summary = monthly_summary,
                           monthly_trend = json.dumps(monthly_trend),
                           expense_categories = expense_categories,
                           income_categories = income_categories,
                           payment_methods = payment_methods,
                           fixed_vs_variable = fixed_vs_variable,
                           daily_expenses = json.dumps(daily_expenses)
                           )

@dashboard_bp.route('/monthly')
@login_required
def monthly():
    """월별 상세 분석"""
    
    today = datetime.now()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    # 월별 요약
    summary = StatisticsService.get_monthly_summary(year, month, current_user.user_id)

    # 카테고리별 분석
    expense_categories = StatisticsService.get_category_analysis('expense', year, month, current_user.user_id)
    income_categories = StatisticsService.get_category_analysis('income', year, month, current_user.user_id)

    # 결제수단별 분석
    payment_methods = StatisticsService.get_payment_method_analysis(year, month, current_user.user_id)

    # 고정지출 vs 변동지출
    fixed_vs_variable = StatisticsService.get_fixed_vs_variable(year, month, current_user.user_id)

    # 일별 지출
    daily_expenses = StatisticsService.get_daily_expenses(year, month, current_user.user_id)

    # 연도/월 선택용 데이터
    years = list(range(2020, datetime.now().year + 1))
    months = list(range(1, 13))

    return render_template('dashboard/monthly.html',
                         year=year,
                         month=month,
                         years=years,
                         months=months,
                         summary=summary,
                         expense_categories=expense_categories,
                         income_categories=income_categories,
                         payment_methods=payment_methods,
                         fixed_vs_variable=fixed_vs_variable,
                         daily_expenses=json.dumps(daily_expenses))

@dashboard_bp.route('/category')
@login_required
def category():
    """카테고리별 상세 분석"""

    today = datetime.now()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))
    transaction_type = request.args.get('transaction_type', 'expense')

    # 카테고리별 분석
    categories = StatisticsService.get_category_analysis(transaction_type, year, month, current_user.user_id)

    # 연도/월 선택용 데이터
    years = list(range(2020, datetime.now().year + 1))
    months = list(range(1, 13))
    
    return render_template('dashboard/category.html',
                         year=year,
                         month=month,
                         years=years,
                         months=months,
                         transaction_type=transaction_type,
                         categories=categories)


@dashboard_bp.route('/analysis')
@login_required
def analysis():
    """
    고급 분석 페이지
    MoM, YoY, 커스텀 기간 분석
    """
    today = datetime.now()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    # MoM Analysis
    mom_data = AnalysisService.get_mom_comparison(year, month, current_user.user_id)

    # YoY Analysis
    yoy_data = AnalysisService.get_yoy_comparison(year, month, current_user.user_id)

    # expense pattern analysis
    spending_pattern = AnalysisService.get_spending_pattern_analysis(year, month, current_user.user_id)

    # year/month select
    years = list(range(2020, datetime.now().year + 1))
    months = list(range(1, 13))

    return render_template('dashboard/analysis.html',
                           year = year,
                           month = month,
                           years = years,
                           months = months,
                           mom_data = mom_data,
                           yoy_data = yoy_data,
                           spending_pattern = spending_pattern)

@dashboard_bp.route('/custom')
@login_required
def custom():
    """
    커스텀 기간 분석 페이지
    """
    # default: recent 30 days
    today = datetime.now().date()
    default_start = today - timedelta(days = 30)

    start_date_str = request.args.get('start_date', default_start.strftime('%Y-%m-%d'))
    end_date_str = request.args.get('end_date', today.strftime('%Y-%m-%d'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # custom analysis
    analysis_data = AnalysisService.get_custom_period_analysis(start_date, end_date, current_user.user_id)

    return render_template('dashboard/custom.html',
                           start_date = start_date_str,
                           end_date = end_date_str,
                           analysis_data = analysis_data)