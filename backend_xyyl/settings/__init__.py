import os

# 默认使用本地配置
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'backend_xyyl.settings.local')

if settings_module == 'backend_xyyl.settings.local':
    from .local import *
elif settings_module == 'backend_xyyl.settings.production':
    from .production import *
else:
    from .local import * 