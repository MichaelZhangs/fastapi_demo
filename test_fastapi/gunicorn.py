# gunicorn的配置

import multiprocessing

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:7778"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
daemon = True
timeout = 60

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'uvicorn.workers.UvicornWorker'
x_forwarded_for_header = 'X-FORWARDED-FOR'
