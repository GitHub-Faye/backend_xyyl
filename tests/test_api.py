import os
import sys
import django
import random
import string

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_xyyl.settings')
django.setup()

import requests
import json
from datetime import datetime, timedelta
import traceback
from django.contrib.auth.models import User
from user_management.models import UserProfile

# API基础URL
BASE_URL = 'http://localhost:8000/api'

class APITestError(Exception):
    """自定义API测试异常"""
    pass

def print_response_error(response, operation):
    """打印响应错误信息"""
    print(f"\n{operation} 失败:")
    print(f"状态码: {response.status_code}")
    print("响应头:", json.dumps(dict(response.headers), indent=2))
    try:
        print("响应内容:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("响应内容:", response.text)

def generate_random_username(prefix='testuser', length=6):
    """生成随机用户名"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{random_str}"

class TestContext:
    """测试上下文，存储测试过程中的共享数据"""
    def __init__(self):
        self.username = generate_random_username()
        self.email = f"{self.username}@example.com"
        self.password = 'testpass123'

def test_user_registration(context):
    """测试用户注册"""
    url = f'{BASE_URL}/users/'
    data = {
        'username': context.username,
        'email': context.email,
        'password': context.password
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code != 201:
            print_response_error(response, "用户注册")
            raise APITestError(f"用户注册失败: {response.status_code}")
        
        print("\n用户注册成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()
    except requests.RequestException as e:
        raise APITestError(f"请求异常: {str(e)}")

def test_user_login(context):
    """测试用户登录"""
    url = f'{BASE_URL}/auth/login/'
    data = {
        'username': context.username,
        'password': context.password
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print_response_error(response, "用户登录")
            raise APITestError(f"用户登录失败: {response.status_code}")
        
        result = response.json()
        if 'access' not in result:
            raise APITestError("登录响应中未包含access token")
        
        print("\n用户登录成功:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except requests.RequestException as e:
        raise APITestError(f"请求异常: {str(e)}")

def test_user_profile(token):
    """测试获取和更新用户资料"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 获取用户资料
        url = f'{BASE_URL}/users/me/profile/'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "获取用户资料")
            raise APITestError(f"获取用户资料失败: {response.status_code}")
        
        print("\n获取用户资料成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 更新用户资料
        data = {
            'name': '测试用户',
            'gender': 'M',
            'age': 25,
            'phone': '13800138000',
            'height': 175.5
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "更新用户资料")
            raise APITestError(f"更新用户资料失败: {response.status_code}")
        
        print("\n更新用户资料成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.RequestException as e:
        raise APITestError(f"请求异常: {str(e)}")

def test_health_records(token):
    """测试健康记录相关功能"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 创建健康记录
        url = f'{BASE_URL}/health-records/'
        data = {
            'weight': 70.5,
            'systolic_pressure': 120,
            'diastolic_pressure': 80,
            'heart_rate': 75,
            'record_time': datetime.now().isoformat()
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            print_response_error(response, "创建健康记录")
            raise APITestError(f"创建健康记录失败: {response.status_code}")
        
        print("\n创建健康记录成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        record_id = response.json()['id']

        # 获取记录列表
        params = {
            'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d')
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "获取健康记录列表")
            raise APITestError(f"获取健康记录列表失败: {response.status_code}")
        
        print("\n获取健康记录列表成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 获取统计数据
        url = f'{BASE_URL}/health-records/statistics/'
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "获取统计数据")
            raise APITestError(f"获取统计数据失败: {response.status_code}")
        
        print("\n获取统计数据成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 更新记录
        url = f'{BASE_URL}/health-records/{record_id}/'
        data['weight'] = 71.0
        response = requests.put(url, json=data, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "更新健康记录")
            raise APITestError(f"更新健康记录失败: {response.status_code}")
        
        print("\n更新健康记录成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 删除记录
        response = requests.delete(url, headers=headers)
        if response.status_code != 204:
            print_response_error(response, "删除健康记录")
            raise APITestError(f"删除健康记录失败: {response.status_code}")
        
        print("\n删除健康记录成功")
    except requests.RequestException as e:
        raise APITestError(f"请求异常: {str(e)}")

def test_password_operations(context, token):
    """测试密码相关操作"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 修改密码
        url = f'{BASE_URL}/users/me/change_password/'
        data = {
            'old_password': context.password,
            'new_password': 'newtestpass123'
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print_response_error(response, "修改密码")
            raise APITestError(f"修改密码失败: {response.status_code}")
        
        print("\n修改密码成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 请求密码重置
        url = f'{BASE_URL}/users/request_password_reset/'
        data = {'email': context.email}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print_response_error(response, "请求密码重置")
            raise APITestError(f"请求密码重置失败: {response.status_code}")
        
        print("\n请求密码重置成功:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.RequestException as e:
        raise APITestError(f"请求异常: {str(e)}")

def cleanup_test_data():
    """清理测试数据"""
    # 删除测试用户及其关联数据
    User.objects.filter(username__startswith='testuser_').delete()

def main():
    """运行所有测试"""
    try:
        print("\n=== 开始API测试 ===")
        
        print("\n清理旧测试数据...")
        cleanup_test_data()
        
        # 创建测试上下文
        context = TestContext()
        print(f"\n使用测试账号: {context.username}")
        
        print("\n1. 测试用户注册")
        user_data = test_user_registration(context)

        print("\n2. 测试用户登录")
        tokens = test_user_login(context)
        access_token = tokens['access']

        print("\n3. 测试用户资料")
        test_user_profile(access_token)

        print("\n4. 测试健康记录")
        test_health_records(access_token)

        print("\n5. 测试密码操作")
        test_password_operations(context, access_token)

        print("\n=== 所有测试完成 ===")
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