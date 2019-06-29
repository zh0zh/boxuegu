import os
from celery import Celery

# 加载django配置
os.environ["DJANGO_SETTINGS_MODULE"]="boxuegu.settings"

# 建立celery实例
celery_app = Celery('boxuegu')

# 加载celery配置,指定消息队列为redis
celery_app.config_from_object('celery_tasks.config')

# 指定任务路径
celery_app.autodiscover_tasks([
    'celery_tasks.mail',
])


