import logging
import smtplib
import subprocess
import datetime
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import *
from django.template.loader import render_to_string
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from comment.models import Comment
from helpers import get_page_list, AdminUserRequiredMixin, ajax_required, SuperUserRequiredMixin, send_html_email
from users.models import User, Feedback
from video.models import Video, Classification
from .forms import UserLoginForm, VideoPublishForm, VideoEditForm, UserAddForm, UserEditForm, ClassificationAddForm, \
    ClassificationEditForm
from .models import MyChunkedUpload

logger = logging.getLogger('my_logger')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_staff:
                auth_login(request, user)
                return redirect('myadmin:index')
            else:
                form.add_error('', '请输入管理员账号')
    else:
        form = UserLoginForm()
    return render(request, 'myadmin/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('myadmin:login')


class IndexView(AdminUserRequiredMixin, generic.View):
    """
    总览数据
    """

    def get(self, request):
        video_count = Video.objects.get_count()
        video_has_published_count = Video.objects.get_published_count()
        video_not_published_count = Video.objects.get_not_published_count()
        user_count = User.objects.count()
        user_today_count = User.objects.exclude(date_joined__lt=datetime.date.today()).count()
        comment_count = Comment.objects.get_count()
        comment_today_count = Comment.objects.get_today_count()
        data = {"video_count": video_count,
                "video_has_published_count": video_has_published_count,
                "video_not_published_count": video_not_published_count,
                "user_count": user_count,
                "user_today_count": user_today_count,
                "comment_count": comment_count,
                "comment_today_count": comment_today_count}
        return render(self.request, 'myadmin/index.html', data)

class AIView(SuperUserRequiredMixin, generic.View):
    """
    总览数据
    """

    def get(self, request):
        return render(self.request, 'myadmin/video_edit.html')
class AddVideoView(SuperUserRequiredMixin, TemplateView):
    template_name = 'myadmin/video_add.html'
class AddAiView(SuperUserRequiredMixin, TemplateView):
    template_name = 'myadmin/video_add2.html'

class MyChunkedUploadView(ChunkedUploadView):
    model = MyChunkedUpload
    field_name = 'the_file'


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = MyChunkedUpload

    def on_completion(self, uploaded_file, request):
        print('uploaded--->', uploaded_file.name)
        print('uploaded--->', uploaded_file)
        pass

    def get_response_data(self, chunked_upload, request):
        video = Video.objects.create(file=chunked_upload.file)
        return {'code': 0, 'video_id': video.id, 'msg': 'success'}
import shutil
import os

class VideoPublishView(SuperUserRequiredMixin, generic.UpdateView):
    model = Video
    form_class = VideoPublishForm
    template_name = 'myadmin/video_publish.html'

    def get_context_data(self, **kwargs):
        context = super(VideoPublishView, self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list':clf_list}
        context.update(clf_data)
        return context

    def get_success_url(self):
        return reverse('myadmin:video_publish_success')
# class VideoPublishView(SuperUserRequiredMixin, generic.UpdateView):
#     model = Video
#     form_class = VideoPublishForm
#     template_name = 'myadmin/video_publish.html'
#
#     def get_context_data(self, **kwargs):
#         #print(**kwargs)
#         context = super(VideoPublishView, self).get_context_data(**kwargs)
#         clf_list = Classification.objects.all().values()
#         # print(context)
#         clf_data = {'clf_list':clf_list}
#         context.update(clf_data)
#         print('context',context)
#         # print('context',context['video'].id)
#         # print('context',context['video'].file)
#         # 假设我们有一个命令行程序 `my_program` 需要接收两个参数
#         current_file_path = os.path.dirname(os.path.abspath(__file__))
#         py_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#         print(current_file_path)
#         print(py_file_path)
#         source_path = os.path.join('/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/recipe-master/upload',context['video'].file)
#         shutil.copy(source_path, source_path.replace('.part','.png'))
#         png_path =source_path.replace('.part','.png')
#         py_path = os.path.join(py_file_path,'yolov5/classify/predict.py')
#         py_path =r'/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py'
#         print(py_path)
#         command = [
#             'python',
#             '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py',
#             '--weights',
#             '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/runs/train-cls/food14_exp8/weights/best.pt',
#             '--img', '224',
#             '--source',
#             png_path
#         ]
#
#         try:
#             completed_process = subprocess.run(command, capture_output=True, text=True, check=True)
#
#
#         except subprocess.CalledProcessError as e:
#             print(f"命令执行失败，退出码：{e.returncode}\n标准输出：{e.stdout}\n标准错误：{e.stderr}")
#         else:
#             # 获取标准输出
#             output = eval(completed_process.stdout)
#             ai_label = output[1]
#             print(f"命令执行成功，标准输出：\n{output}")
#
#             # 获取返回码
#             return_code = completed_process.returncode
#             print(f"命令执行的返回码：{return_code}")
#         old_Videos = Video.objects.filter(title=ai_label)
#
#         # print('old title', context['form']['fields'].title)
#         source_dict = {'source':{'title':'','desc':''}}
#         if old_Videos.exists():
#             old_Video= old_Videos.first()
#             #print(old_Video.desc)
#             context['video'].desc = old_Video.desc
#             source_dict['source']['title'] = old_Video.title
#             source_dict['source']['desc'] = old_Video.desc
#         context.update(source_dict)
#
#         # print('desc',context['form'].desc)
#         # print('title',context['form'].title)
#
#         return context
#
#     def get_success_url(self):
#         return reverse('myadmin:video_publish_success')


class VideoPublishSuccessView(generic.TemplateView):
    template_name = 'myadmin/video_publish_success.html'


def edit_view(request):
    if request.method=='GET':

        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list': clf_list}

        return render(request, 'myadmin/video_edit2.html',context=clf_data)
    if request.method == 'POST':
        model = Video()
        form_class = VideoPublishForm
        print(form_class)
        titile = request.POST.get('title')
        model.title=titile
        model.desc =request.POST.get('desc')
        model.cover =request.FILES.get('the_file')
        dropdown_choice = request.POST.get('option')
        print(dropdown_choice)
        model.save()
        print(request.POST)
        print(request.FILES.get('the_file'))
        print(request.FILES)
        print(titile)

        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list': clf_list,'form':model}
        return render(request, 'myadmin/video_edit2.html', context=clf_data)



class VideoEditView(SuperUserRequiredMixin, generic.UpdateView):
    model = Video
    form_class = VideoEditForm
    template_name = 'myadmin/video_edit.html'

    def get_context_data(self, **kwargs):

        context = super(VideoEditView, self).get_context_data(**kwargs)

        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list':clf_list}
        context.update(clf_data)
        return context

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:video_edit', kwargs={'pk': self.kwargs['pk']})

class VideoEditView2(SuperUserRequiredMixin, generic.UpdateView):
    model = Video
    form_class = VideoEditForm
    template_name = 'myadmin/video_edit.html'

    def get_context_data(self, **kwargs):
        context = super(VideoEditView, self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list':clf_list}
        context.update(clf_data)
        return context

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:video_edit', kwargs={'pk': self.kwargs['pk']})
@ajax_required
@require_http_methods(["POST"])
def video_delete(request):
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    video_id = request.POST['video_id']
    instance = Video.objects.get(id=video_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class VideoListView(AdminUserRequiredMixin, generic.ListView):
    model = Video
    template_name = 'myadmin/video_list.html'
    context_object_name = 'video_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Video.objects.get_search_list(self.q)


class ClassificationListView(AdminUserRequiredMixin, generic.ListView):
    model = Classification
    template_name = 'myadmin/classification_list.html'
    context_object_name = 'classification_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClassificationListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Classification.objects.filter(title__contains=self.q)


class ClassificationAddView(SuperUserRequiredMixin, generic.View):
    def get(self, request):
        form = ClassificationAddForm()
        return render(self.request, 'myadmin/classification_add.html', {'form': form})

    def post(self, request):
        form = ClassificationAddForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(self.request, 'myadmin/classification_add_success.html')
        return render(self.request, 'myadmin/classification_add.html', {'form': form})


@ajax_required
@require_http_methods(["POST"])
def classification_delete(request):
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    classification_id = request.POST['classification_id']
    instance = Classification.objects.get(id=classification_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class ClassificationEditView(SuperUserRequiredMixin, generic.UpdateView):
    model = Classification
    form_class = ClassificationEditForm
    template_name = 'myadmin/classification_edit.html'

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:classification_edit', kwargs={'pk': self.kwargs['pk']})


class CommentListView(AdminUserRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'myadmin/comment_list.html'
    context_object_name = 'comment_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Comment.objects.filter(content__contains=self.q).order_by('-timestamp')


@ajax_required
@require_http_methods(["POST"])
def comment_delete(request):
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    comment_id = request.POST['comment_id']
    instance = Comment.objects.get(id=comment_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class UserListView(AdminUserRequiredMixin, generic.ListView):
    model = User
    template_name = 'myadmin/user_list.html'
    context_object_name = 'user_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return User.objects.filter(username__contains=self.q).order_by('-date_joined')


class UserAddView(SuperUserRequiredMixin, generic.View):
    def get(self, request):
        form = UserAddForm()
        return render(self.request, 'myadmin/user_add.html', {'form': form})

    def post(self, request):
        form = UserAddForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return render(self.request, 'myadmin/user_add_success.html')
        return render(self.request, 'myadmin/user_add.html', {'form': form})


class UserEditView(SuperUserRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'myadmin/user_edit.html'

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:user_edit', kwargs={'pk': self.kwargs['pk']})


@ajax_required
@require_http_methods(["POST"])
def user_delete(request):
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    user_id = request.POST['user_id']
    instance = User.objects.get(id=user_id)
    if instance.is_superuser:
        return JsonResponse({"code": 1, "msg": "不能删除管理员"})
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class SubscribeView(SuperUserRequiredMixin, generic.View):

    def get(self, request):
        video_list = Video.objects.get_published_list()
        return render(request, "myadmin/subscribe.html" ,{'video_list':video_list})

    def post(self, request):
        if not request.user.is_superuser:
            return JsonResponse({"code": 1, "msg": "无权限"})
        video_id = request.POST['video_id']
        video = Video.objects.get(id=video_id)
        subject = video.title
        context = {'video': video,'site_url':settings.SITE_URL}
        html_message = render_to_string('myadmin/mail_template.html', context)
        email_list = User.objects.filter(subscribe=True).values_list('email',flat=True)
        # 分组
        email_list = [email_list[i:i + 2] for i in range(0, len(email_list), 2)]

        if email_list:
            for to_list in email_list:
                try:
                    send_html_email(subject, html_message, to_list)
                except smtplib.SMTPException as e:
                    logger.error(e)
                    return JsonResponse({"code": 1, "msg": "发送失败"})
            return JsonResponse({"code": 0, "msg": "success"})
        else:
            return JsonResponse({"code": 1, "msg": "邮件列表为空"})


class FeedbackListView(AdminUserRequiredMixin, generic.ListView):
    model = Feedback
    template_name = 'myadmin/feedback_list.html'
    context_object_name = 'feedback_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FeedbackListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Feedback.objects.filter(content__contains=self.q).order_by('-timestamp')


@ajax_required
@require_http_methods(["POST"])
def feedback_delete(request):
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    feedback_id = request.POST['feedback_id']
    instance = Feedback.objects.get(id=feedback_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})

