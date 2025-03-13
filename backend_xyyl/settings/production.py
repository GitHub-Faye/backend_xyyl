from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2dzb=hq9wju8ok_1a90-js79_00mn$*pbcm*ev))u&b(8tazm='

DEBUG = False

ALLOWED_HOSTS = ['wyw123.pythonanywhere.com']

# Database
# 使用SQLite数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/wyw123/小艺医疗web/backend_xyyl/db.sqlite3',
    }
}

# 静态文件配置
STATIC_ROOT = '/home/wyw123/小艺医疗web/backend_xyyl/static'
STATIC_URL = '/static/'

# 媒体文件配置
MEDIA_ROOT = '/home/wyw123/小艺医疗web/backend_xyyl/media'
MEDIA_URL = '/media/'

# CORS配置
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://servicewechat.com",
    "https://wyw123.pythonanywhere.com",
]

# 微信小程序配置
WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', 'wx1a1bc043dae03c3e')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', '28c9f799686403a0cb8c5412d14e76a7')

# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# 安全设置
SECURE_SSL_REDIRECT = False  # PythonAnywhere 已经处理了 SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/wyw123/小艺医疗web/backend_xyyl/logs/django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'medication_reminder': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
} 