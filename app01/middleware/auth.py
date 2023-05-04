from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, render


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info == "/login/":
            return

        # 1.根据请求体(request)中的cookie，读取当前访问的用户在session中的info信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect('/login/')


class UserManageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if '/admin/' in request.path_info:
            info_dict = request.session.get("info")
            group = info_dict['group']
            if group == 1:
                return
            else:
                return render(request, 'error.html', {'error_msg': '您不是超级管理员用户，无权访问用户信息'})
