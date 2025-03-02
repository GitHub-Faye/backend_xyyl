import os
import sys
import django
import random
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_xyyl.settings')
django.setup()

import requests
import json
import traceback
from django.contrib.auth.models import User
from health_info.models import HealthRecord

# API基础URL
BASE_URL = 'http://localhost:8000/api'

class APITestError(Exception):
    """自定义API测试异常"""
    pass

class TestContext:
    """测试上下文"""
    def __init__(self):
        self.username = f"testuser_{random.randint(1000, 9999)}"
        self.password = "testpass123"
        self.email = f"{self.username}@example.com"
        self.access_token = None
        self.test_records = []

def setup_test_user(context):
    """创建测试用户并获取token"""
    # 注册用户
    url = f'{BASE_URL}/users/'
    data = {
        'username': context.username,
        'email': context.email,
        'password': context.password
    }
    response = requests.post(url, json=data)
    if response.status_code != 201:
        raise APITestError(f"用户注册失败: {response.status_code}")

    # 登录获取token
    url = f'{BASE_URL}/auth/login/'
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise APITestError(f"用户登录失败: {response.status_code}")
    
    context.access_token = response.json()['access']
    return context

def create_test_records(context, days=30):
    """创建测试数据"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    url = f'{BASE_URL}/health-records/'
    
    # 修改：从今天开始，往前推30天
    end_date = datetime.now()
    records = []
    
    # 创建每日记录，模拟真实数据波动
    for day in range(days):
        # 从今天开始，每次减去一天
        current_date = end_date - timedelta(days=day)
        # 添加随机波动
        weight = 70.0 + random.uniform(-2.0, 2.0)
        systolic = 120 + random.randint(-10, 10)
        diastolic = 80 + random.randint(-5, 5)
        heart_rate = 75 + random.randint(-10, 10)
        
        data = {
            'weight': round(weight, 2),
            'systolic_pressure': systolic,
            'diastolic_pressure': diastolic,
            'heart_rate': heart_rate,
            'record_time': current_date.isoformat()
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            raise APITestError(f"创建记录失败: {response.status_code}")
        
        records.append(response.json())
        print(f"创建记录 {day+1}/{days} - {current_date.strftime('%Y-%m-%d')}")
    
    # 保存测试用户信息到文件，供测试脚本使用
    test_info = {
        'username': context.username,
        'password': context.password,
        'email': context.email
    }
    with open('test_user_info.json', 'w') as f:
        json.dump(test_info, f)
    
    context.test_records = records
    return records

def main():
    """准备测试数据"""
    try:
        print("\n=== 开始准备测试数据 ===")
        
        # 创建测试上下文
        context = TestContext()
        print(f"\n使用测试账号: {context.username}")
        
        # 设置测试用户
        setup_test_user(context)
        print("\n测试用户创建成功")
        
        # 创建30天的测试数据
        print("\n创建30天测试记录...")
        create_test_records(context)
        print("\n30天测试记录创建完成")
        
        print("\n=== 测试数据准备完成 ===")
        return 0
        
    except APITestError as e:
        print(f"\n准备失败: {str(e)}")
        return 1
    except Exception as e:
        print("\n发生未预期的错误:")
        print("错误类型:", type(e).__name__)
        print("错误信息:", str(e))
        print("\n详细错误信息:")
        traceback.print_exc()
        return 2

if __name__ == '__main__':
    sys.exit(main()) 