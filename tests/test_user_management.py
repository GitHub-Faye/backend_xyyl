import os
import sys
import django
import json
import requests
import traceback
from datetime import datetime

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_xyyl.settings')
django.setup()

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
        self.username = f"testuser_{datetime.now().strftime('%H%M%S')}"
        self.password = "testpass123"
        self.email = f"{self.username}@example.com"
        self.access_token = None
        self.refresh_token = None

def test_register(context):
    """测试用户注册"""
    url = f'{BASE_URL}/users/'
    data = {
        'username': context.username,
        'email': context.email,
        'password': context.password
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 201:
        print_response_error(response, "用户注册")
        raise APITestError(f"用户注册失败: {response.status_code}")
    
    print("\n用户注册成功:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def test_login(context):
    """测试用户登录"""
    url = f'{BASE_URL}/auth/login/'
    data = {
        'username': context.username,
        'password': context.password
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print_response_error(response, "用户登录")
        raise APITestError(f"用户登录失败: {response.status_code}")
    
    tokens = response.json()
    context.access_token = tokens['access']
    context.refresh_token = tokens['refresh']
    
    print("\n用户登录成功:")
    print(json.dumps(tokens, indent=2, ensure_ascii=False))
    return tokens

def test_refresh_token(context):
    """测试刷新token"""
    url = f'{BASE_URL}/auth/refresh/'
    data = {
        'refresh': context.refresh_token
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print_response_error(response, "刷新token")
        raise APITestError(f"刷新token失败: {response.status_code}")
    
    new_tokens = response.json()
    context.access_token = new_tokens['access']
    
    print("\nToken刷新成功:")
    print(json.dumps(new_tokens, indent=2, ensure_ascii=False))
    return new_tokens

def test_change_password(context):
    """测试修改密码"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    url = f'{BASE_URL}/users/me/change_password/'
    
    new_password = "newpass123"
    data = {
        'old_password': context.password,
        'new_password': new_password
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print_response_error(response, "修改密码")
        raise APITestError(f"修改密码失败: {response.status_code}")
    
    # 更新上下文中的密码
    context.password = new_password
    print("\n密码修改成功")

def test_request_password_reset(context):
    """测试请求密码重置"""
    url = f'{BASE_URL}/users/request_password_reset/'
    data = {
        'email': context.email
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print_response_error(response, "请求密码重置")
        raise APITestError(f"请求密码重置失败: {response.status_code}")
    
    print("\n请求密码重置成功:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_logout(context):
    """测试用户登出"""
    headers = {'Authorization': f'Bearer {context.access_token}'}
    url = f'{BASE_URL}/users/logout/'
    
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        print_response_error(response, "用户登出")
        raise APITestError(f"用户登出失败: {response.status_code}")
    
    print("\n用户登出成功")

def save_test_context(context):
    """保存测试用户信息到文件"""
    test_info = {
        'username': context.username,
        'password': context.password,
        'email': context.email
    }
    with open('test_user_info.json', 'w') as f:
        json.dump(test_info, f, indent=2)
    print("\n测试用户信息已保存到 test_user_info.json")

def main():
    """运行测试"""
    try:
        print("\n=== 开始用户管理测试 ===")
        
        # 创建测试上下文
        context = TestContext()
        print(f"\n创建测试账号: {context.username}")
        
        # 测试注册
        print("\n测试用户注册...")
        test_register(context)
        
        # 测试登录
        print("\n测试用户登录...")
        test_login(context)
        
        # 测试刷新token
        print("\n测试刷新token...")
        test_refresh_token(context)
        
        # 测试修改密码
        print("\n测试修改密码...")
        test_change_password(context)
        
        # 测试重新登录（使用新密码）
        print("\n测试使用新密码登录...")
        test_login(context)
        
        # 测试请求密码重置
        print("\n测试请求密码重置...")
        test_request_password_reset(context)
        
        # 测试登出
        print("\n测试用户登出...")
        test_logout(context)
        
        # 保存测试用户信息
        save_test_context(context)
        
        print("\n=== 用户管理测试完成 ===")
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

#测试上传