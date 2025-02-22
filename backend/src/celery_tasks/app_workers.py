from celery import Celery

from src.config.app_config import Config as cc


def get_celery_app(name):
    app = Celery(
        name,
        broker=cc.MQ_URL,  
        backend=cc.REDIS_URL  
    )


    app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='Asia/Ho_Chi_Minh', 
        enable_utc=True
    )

    app.conf.update(
        worker_hijack_root_logger=False,
        worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
        worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    )

    return app