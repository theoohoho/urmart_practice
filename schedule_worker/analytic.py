from sqlalchemy.sql import func
from sqlalchemy.orm.session import Session

from schedule_worker.models import Order, Analytic
from schedule_worker.database_session import get_db_session

import datetime


def get_batch_num(db: Session) -> (int, int):
    """Get the batch number of last analysis result and current batch number
    """
    last_analytic = db.query(Analytic).select_from(
        Analytic).order_by(Analytic.batch.desc()).first()
    if not last_analytic:
        last_batch_num = 0
    else:
        last_batch_num = last_analytic.batch

    curr_batch_num = last_batch_num + 1
    return last_batch_num, curr_batch_num


def run_analysis() -> None:
    """Analyze order information and collect to database
    """
    print('Start to analysis order information...')
    with get_db_session() as db:

        last_batch_num, curr_batch_num = get_batch_num(db)
        print(
            f'Current bath num is: {str(curr_batch_num)}, last bath: {str(last_batch_num)}')

        # SELECT shop_id, COUNT(*), SUM(qty), SUM(price) FROM order GROUP BY shop_id
        analysis_result = db.query(
            Order.shop_id, func.count(), func.sum(Order.qty), func.sum(Order.price)
        ).select_from(Order).group_by(Order.shop_id).all()

        # ship analysis job, if database not contain order information
        if not analysis_result:
            print('Haven\' order information in database yet, skip analysis job...')
            return

        print('To store analysis result into database...')
        analysis_result_models = []
        for shop_id, total_orders, total_sales_products, total_sales_amount in analysis_result:
            analysis_result_models.append(Analytic(
                shop_id=shop_id,
                total_sales_amount=total_sales_amount,
                total_sales_products=total_sales_products,
                total_orders=total_orders,
                batch=curr_batch_num,
                timestamp=datetime.datetime.now()
            ))
        db.add_all(analysis_result_models)
        db.commit()
        print('Finish database operation...')
    print('Finish analysis job....')


if __name__ == "__main__":
    run_analysis()
