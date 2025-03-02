from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

# Create your views here.

class WechatLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """微信小程序登录"""
        # 记录请求内容，帮助调试
        print(f"收到微信登录请求，数据: {request.data}")
        
        code = request.data.get('code')
        if not code:
            print("错误: 请求中缺少code参数")
            return Response(
                {'error': '缺少code参数'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 这里需要替换为您的小程序AppID和AppSecret
            appid = settings.WECHAT_APP_ID
            secret = settings.WECHAT_APP_SECRET
            
            print(f"使用的配置 - AppID: {appid}, AppSecret: {secret[:3]}***")
            
            # 调用微信API获取openid
            wx_url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
            response = requests.get(wx_url)
            data = response.json()
            
            print(f"微信API响应: {data}")
            
            if 'errcode' in data and data['errcode'] != 0:
                print(f"微信API错误: {data.get('errcode')} - {data.get('errmsg')}")
                return Response(
                    {'error': f'微信登录失败: {data.get("errmsg")}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            openid = data.get('openid')
            if not openid:
                print("错误: 未获取到openid")
                return Response(
                    {'error': '微信登录失败: 未获取到openid'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 查找或创建用户
            try:
                profile = UserProfile.objects.get(openid=openid)
                user = profile.user
                username = user.username  # 为现有用户获取username
                print(f"找到已存在用户: {username}")
            except UserProfile.DoesNotExist:
                # 创建新用户
                username = f'wx_{openid}'
                user = User.objects.create_user(
                    username=username,
                    password=None,  # 微信用户无需密码
                    email=''
                )
                # 创建或获取用户档案
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.openid = openid
                profile.save()
                print(f"创建新用户: {username}")
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            
            # 转换gender字段为数字类型
            gender_map = {'M': 1, 'F': 2, 'O': 0}
            gender_value = gender_map.get(profile.gender, 0) if profile.gender else 0
            
            response_data = {
                'token': str(refresh.access_token),
                'refreshToken': str(refresh),
                'expiresIn': 3600,  # 令牌有效期（秒）
                'userInfo': {
                    'id': str(user.id),  # 确保id是字符串类型
                    'openId': profile.openid,
                    'nickName': profile.nickname or username,
                    'avatarUrl': profile.avatar_url or '',
                    'gender': gender_value,  # 使用转换后的数字类型
                    'country': profile.country or '',
                    'province': profile.province or '',
                    'city': profile.city or '',
                    'createdAt': user.date_joined.isoformat(),
                    'updatedAt': profile.updated_at.isoformat() if hasattr(profile, 'updated_at') else user.date_joined.isoformat()
                }
            }
            
            print("登录成功，返回用户信息和令牌")
            print(f"返回数据: {response_data}")
            return Response(response_data)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"服务器错误: {str(e)}")
            print(f"错误详情: {error_trace}")
            return Response(
                {'error': f'服务器错误: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_permissions(self):
        """根据不同的action返回不同的权限"""
        if self.action in ['create', 'request_password_reset']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """获取或更新当前用户的完整信息（包括资料）"""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        # PATCH 方法处理部分更新
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put'], url_path='me/profile')
    def my_profile(self, request):
        """获取或更新当前用户的详细资料"""
        profile = request.user.profile
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='me/change_password')
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'error': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': '密码修改成功'})

    @action(detail=False, methods=['post'])
    def request_password_reset(self, request):
        """请求密码重置"""
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # TODO: 发送重置密码邮件
            return Response({'message': '重置密码邮件已发送'})
        except User.DoesNotExist:
            return Response(
                {'error': '该邮箱未注册'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        try:
            # TODO: 验证token并重置密码
            return Response({'message': '密码重置成功'})
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # 可以在这里添加token黑名单逻辑
        return Response({'message': '注销成功'})
