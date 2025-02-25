from celery import Celery

from src.config.app_config import Config as cfg


def get_celery_app(name):
    app = Celery(
        name,
        broker=cfg.MQ_URL,  
        backend=cfg.REDIS_URL  
    )


    app.conf.update(
        task_serializer='json',
        result_serializer='json',
        acfgept_content=['json'],
        timezone='Asia/Ho_Chi_Minh', 
        enable_utc=True
    )

    app.conf.update(
        worker_hijack_root_logger=False,
        worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
        worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    )

    return app