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

class APITestError(Exception):
    """自定义API测试异常"""
    pass

# API基础URL
BASE_URL = 'http://localhost:8000/api'

def print_response_error(response, operation):
    """打印响应错误信息"""
    print(f"\n{operation} 失败:")
    print(f"状态码: {response.status_code}")
    print("响应头:", json.dumps(dict(response.headers), indent=2))
    try:
        print("响应内容:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("响应内容:", response.text)

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
    
    base_date = datetime.now() - timedelta(days=days)
    records = []
    
    # 创建每日记录，模拟真实数据波动
    for day in range(days):
        current_date = base_date + timedelta(days=day)
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
        print(f"创建记录 {day+1}/{days}")
    
    context.test_records = records
    return records

def test_get_records_by_date_range(context):
    """测试不同时间范围的记录获取"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    url = f'{BASE_URL}/health-records/'
    
    # 获取今天的日期
    today = datetime.now().date()
    
    # 测试不同时间范围
    ranges = [
        ('今日', today, today, "今日记录"),  # 今天到今天
        ('最近7天', today - timedelta(days=6), today, "最近7天记录"),  # 今天和前6天（共7天）
        ('最近30天', today - timedelta(days=29), today, "最近30天记录"),  # 今天和前29天（共30天）
        ('自定义范围', today - timedelta(days=20), today - timedelta(days=10), "自定义范围记录"),  # 20天前到10天前
    ]
    
    for name, start_date, end_date, desc in ranges:
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            raise APITestError(f"获取{name}记录失败: {response.status_code}")
        
        records = response.json()
        print(f"\n{desc}数量: {len(records)}")
        if records:
            print(f"第一条记录: {json.dumps(records[0], indent=2, ensure_ascii=False)}")
            print(f"时间范围: {params['start_date']} 到 {params['end_date']}")

def test_statistics(context):
    """测试统计功能"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    url = f'{BASE_URL}/health-records/statistics/'
    
    # 获取今天的日期
    today = datetime.now().date()
    
    # 测试不同时间范围的统计
    ranges = [
        ('今日', today, today),  # 今天到今天
        ('最近7天', today - timedelta(days=6), today),  # 今天和前6天（共7天）
        ('最近30天', today - timedelta(days=29), today),  # 今天和前29天（共30天）
        ('自定义范围', today - timedelta(days=20), today - timedelta(days=10)),  # 20天前到10天前
    ]
    
    for name, start_date, end_date in ranges:
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            raise APITestError(f"获取{name}统计失败: {response.status_code}")
        
        stats = response.json()
        print(f"\n{name}统计:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))

def test_record_operations(context):
    """测试记录的增删改查操作"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    
    # 创建记录
    url = f'{BASE_URL}/health-records/'
    data = {
        'weight': 71.5,
        'systolic_pressure': 118,
        'diastolic_pressure': 78,
        'heart_rate': 72,
        'record_time': datetime.now().isoformat()
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        raise APITestError(f"创建记录失败: {response.status_code}")
    
    record_id = response.json()['id']
    print("\n创建记录成功:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    # 更新记录
    url = f'{BASE_URL}/health-records/{record_id}/'
    data['weight'] = 72.0
    response = requests.put(url, json=data, headers=headers)
    if response.status_code != 200:
        raise APITestError(f"更新记录失败: {response.status_code}")
    
    print("\n更新记录成功:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    # 获取单条记录
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise APITestError(f"获取记录失败: {response.status_code}")
    
    print("\n获取单条记录成功:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    # 删除记录
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise APITestError(f"删除记录失败: {response.status_code}")
    
    print("\n删除记录成功")

def cleanup_test_data():
    """清理测试数据"""
    User.objects.filter(username__startswith='testuser_').delete()

def get_test_context():
    """从文件获取测试用户信息"""
    with open('test_user_info.json', 'r') as f:
        test_info = json.load(f)
    
    context = TestContext()
    context.username = test_info['username']
    context.password = test_info['password']
    context.email = test_info['email']
    
    # 登录获取token
    url = f'{BASE_URL}/auth/login/'
    data = {
        'username': context.username,
        'password': context.password
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise APITestError(f"用户登录失败: {response.status_code}")
    
    context.access_token = response.json()['access']
    return context

def main():
    """运行测试"""
    try:
        print("\n=== 开始健康记录测试 ===")
        
        # 获取测试上下文
        context = get_test_context()
        print(f"\n使用测试账号: {context.username}")
        
        # 测试查询和统计功能
        print("\n测试时间范围查询...")
        test_get_records_by_date_range(context)
        
        print("\n测试统计功能...")
        test_statistics(context)
        
        # 测试基本的CRUD操作
        print("\n测试记录基本操作...")
        test_record_operations(context)
        
        print("\n=== 健康记录测试完成 ===")
        return 0
        
    except APITestError as e:
        print(f"\n测试失败: {str(e)}")
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