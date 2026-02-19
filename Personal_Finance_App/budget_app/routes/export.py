from flask import Blueprint, request, send_file, flash, redirect, url_for
from datetime import datetime
from io import BytesIO
from services.analysis_service import AnalysisService
import pandas as pd

export_bp = Blueprint('export', __name__, url_prefix = '/export')

@export_bp.route('/csv')
def export_csv():
    """
    export with csv files
    """
    # get parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transaction_type = request.args.get('transaction_type')

    # change date
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    try:
        # Get dataframe
        df = AnalysisService.get_transaction_dataframe(start_date, end_date, transaction_type)
        
        if df.empty:
            flash('내보낼 데이터가 없습니다.', 'error')
            return redirect(url_for('transaction.list'))
        
        # select column
        export_df = df[[
            'date', 'type', 'description', 'amount', 'category', 'payment_method', 'is_fixed', 'memo'
        ]].copy()

        # change column name into Korean
        export_df.columns = ['날짜', '유형', '내용', '금액', '카테고리', '결제수단', '고정지출', '메모']

        # change type into Korean
        export_df['유형'] = export_df['유형'].map({'income': '수압', 'expense': '지출'})
        export_df['고정지출'] = export_df['고정지출'].map({True: '예', False: '아니오'})

        # change into csv
        output = BytesIO()
        export_df.to_csv(output, index = False, encoding = 'utf-8-sig')  # Excel에서 한글 깨짐 방지
        output.seek(0)

        # filename
        filename = f'transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}/.csv'

        return send_file(
            output,
            mimetype = 'text/csv',
            as_attachment = True,
            download_name = filename
        )
    
    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('transaction.list'))
    
@export_bp.route('/excel')
def export_excel():
    """
    download as excel file
    """

    # get parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transaction_type = request.args.get('transaction_type')

    # change dates
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    try:
        # get dataframe
        df = AnalysisService.get_transaction_dataframe(start_date, end_date, transaction_type)

        if df.empty:
            flash('내보낼 데이터가 없습니다.', 'error')
            return redirect(url_for('transaction.list'))
        
        # make excel file
        output = BytesIO()

        with pd.ExcelWriter(output, engine = 'openpyxl') as writer:
            # transaction sheet
            export_df = df[[
                'date', 'type', 'description', 'amount', 'category', 'payment_method', 'is_fixed', 'memo'
            ]].copy()

            export_df.columns = [
                '날짜', '유형', '내용', '금액', '카테고리', '결제수단', '고정지출', '메모'
            ]

            export_df['유형'] = export_df['유형'].map({'income': '수입', 'expense': '지출'})
            export_df['고정지출'] = export_df['고정지출'].map({True: '예', False: '아니오'})

            export_df.to_excel(writer, sheet_name = '거래내역', index = False)

            # category summary sheet
            income_df = df.query("Transaction_type == 'income'")
            expense_df = df.query("Transaction_type == 'expense'")

            category_summary = expense_df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
            category_summary.columns = ['총액', '건수', '평균']
            category_summary.to_excel(writer, sheet_name = '카테고리별 요약')

            # stats summary sheet
            summary_data = {
                '항목': ['총 수입', '총 지출', '잔액', '거래 건수'],
                '금액': [
                    income_df['amount'].sum(),
                    expense_df['amount'].sum(),
                    income_df['amount'].sum() - expense_df['amount'].sum(),
                    len(df)
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name = '통계_요약', index = False)
        
        output.seek(0)

        # create filename
        filename = f'transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment = True,
            download_name = filename
        )
    
    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('transaction.list'))