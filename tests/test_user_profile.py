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

def get_test_context():
    """从文件获取测试用户信息"""
    with open('test_user_info.json', 'r') as f:
        test_info = json.load(f)
    return test_info

def test_get_profile(access_token):
    """测试获取用户资料"""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{BASE_URL}/users/me/'
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print_response_error(response, "获取用户资料")
        raise APITestError(f"获取用户资料失败: {response.status_code}")
    
    print("\n获取用户资料成功:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def test_update_profile(access_token):
    """测试更新用户资料"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f'{BASE_URL}/users/me/'
    
    # 更新数据
    update_data = {
        'profile': {
            'name': '测试用户',
            'gender': 'M',  # 注意：使用模型中定义的选项
            'age': 30,
            'phone': '13800138000',
            'height': 175.0
        }
    }
    
    response = requests.patch(url, json=update_data, headers=headers)
    if response.status_code != 200:
        print_response_error(response, "更新用户资料")
        raise APITestError(f"更新用户资料失败: {response.status_code}")
    
    print("\n更新用户资料成功:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def test_change_password(access_token, old_password, new_password):
    """测试修改密码"""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{BASE_URL}/auth/change-password/'
    
    data = {
        'old_password': old_password,
        'new_password': new_password
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print_response_error(response, "修改密码")
        raise APITestError(f"修改密码失败: {response.status_code}")
    
    print("\n修改密码成功")

def main():
    """运行测试"""
    try:
        print("\n=== 开始用户资料测试 ===")
        
        # 获取测试用户信息
        test_info = get_test_context()
        print(f"\n使用测试账号: {test_info['username']}")
        
        # 登录获取token
        url = f'{BASE_URL}/auth/login/'
        data = {
            'username': test_info['username'],
            'password': test_info['password']
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise APITestError(f"用户登录失败: {response.status_code}")
        
        access_token = response.json()['access']
        
        # 测试获取用户资料
        print("\n测试获取用户资料...")
        original_profile = test_get_profile(access_token)
        
        # 测试更新用户资料
        print("\n测试更新用户资料...")
        updated_profile = test_update_profile(access_token)
        
        # 验证更新结果
        print("\n验证更新结果...")
        current_profile = test_get_profile(access_token)
        
        # 测试修改密码（可选，取消注释以测试）
        # print("\n测试修改密码...")
        # test_change_password(access_token, test_info['password'], 'new_password123')
        
        print("\n=== 用户资料测试完成 ===")
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