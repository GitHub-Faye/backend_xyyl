import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path('/home/wyw123/小艺医疗web/backend_xyyl/.env')
load_dotenv(env_path)

# 添加项目路径
path = '/home/wyw123/小艺医疗web/backend_xyyl'
if path not in sys.path:
    sys.path.append(path)

# 设置 Django 设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend_xyyl.settings.production'

# 导入 Django WSGI 应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 