from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, render


class AuthMiddleware(MiddlewareMixin):
    # 登录才能进入页面
    def process_request(self, request): # 在视图函数执行之前调用
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
    # 只有超级管理员才可以访问全部用户信息
    def process_request(self, request):
        if '/admin/' in request.path_info:
            info_dict = request.session.get("info")
            group = info_dict['group']
            if group == 1:
                return
            else:
                return render(request, 'error.html', {'error_msg': '您不是超级管理员用户，无权访问用户信息'})


class UserEditMiddleware(MiddlewareMixin):
    # 个人信息编辑: 此入口只允许修改自己的信息，不允许访问别人
    def process_request(self, request):
        info_dict = request.session.get("info")
        if '/user/' in request.path_info and '/edit/' in request.path_info and request.path_info != '/user/{}/edit/'.format(info_dict['id']):
            # 如果访问/user/<int>/edit/而且访问的nid不是自己的id，不被允许
            # 后来想想自己写的不好，这样的话就不如直接写在user_edit函数中
            return render(request, 'error.html', {'error_msg': '您无权从此处修改他人信息，如果您是超级管理员，请从“用户管理”修改'})
