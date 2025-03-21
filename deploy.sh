#!/bin/bash

echo "开始部署..."

# 进入项目目录
cd /home/wyw123/backend_xyyl

# 激活虚拟环境（虚拟环境可能位置不同，根据实际情况修改）
source ../venv/bin/activate || source ~/.virtualenvs/myevv/bin/activate

# 拉取最新代码
echo "拉取最新代码..."
git pull

# 安装/更新依赖
echo "更新依赖..."
pip install -r requirements.txt

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 设置文件权限
echo "设置文件权限..."
chmod 664 db.sqlite3
chmod -R 775 static
chmod -R 775 media
mkdir -p logs
chmod -R 775 logs

# 重启 web 应用
echo "重启 web 应用..."
touch /var/www/wyw123_pythonanywhere_com_wsgi.py

echo "部署完成!" 