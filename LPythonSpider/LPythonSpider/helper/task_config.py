# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
from ConfigHelper import ConfigManager


# Broker and Backend
BROKER_URL = 'redis://{0}:{1}'.format(ConfigManager.redis_host, ConfigManager.redis_port)
CELERY_RESULT_BACKEND = 'redis://{0}:{1}/0'.format(ConfigManager.redis_host, ConfigManager.redis_port)
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'

CELERY_IMPORTS = (
    'tasks',
)
# schedules
CELERYBEAT_SCHEDULE = {
    'multiply-at-some-time': {
        'task': 'tasks.start_spider',
        'schedule':crontab(minute=0,hour=0),  # 每天早上 00点 00分执行一次
        'args': (1,1)  # 任务函数参数
    },
    'multiply-at-some-time': {
        'task': 'tasks.push_url_to_redis',
        'schedule': crontab(minute=01,hour=0),  # 每天早上 00 点 01分执行一次
        'args': (1,1)  # 任务函数参数
    }
}