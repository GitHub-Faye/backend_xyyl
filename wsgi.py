import os
import sys

# 添加项目路径
path = '/home/wyw123/小艺医疗web/backend_xyyl'
if path not in sys.path:
    sys.path.append(path)

# 设置 Django 设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend_xyyl.settings.production'

# 导入 Django WSGI 应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 