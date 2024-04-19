from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_http_methods

from helpers import get_page_list, ajax_required
from .forms import CommentForm
from .models import Video, Classification



class IndexView(generic.ListView):
    model = Video
    template_name = 'video/index.html'
    context_object_name = 'video_list'
    paginate_by = 12
    c = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        classification_list = Classification.objects.filter(status=True).values()
        context['c'] = self.c
        context['classification_list'] = classification_list
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            classification = get_object_or_404(Classification, pk=self.c)
            return classification.video_set.all().order_by('-create_time')
        else:
            return Video.objects.filter(status=0).order_by('-create_time')


class SearchListView(generic.ListView):
    model = Video
    template_name = 'video/search.html'
    context_object_name = 'video_list'
    paginate_by = 8
    q = ''

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Video.objects.filter(title__contains=self.q).filter(status=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context
from django.shortcuts import render
from django.core.files.storage import default_storage
# from .png_cls import png_api
import os
import subprocess

def png_api(pre_py,png_path,model_path):
    print('='*20)
    print(png_path)
    print('=' * 20)


    command = [
        'python',
        pre_py,
        '--weights',
        model_path,
        '--img', '224',
        '--source',
        png_path
    ]

    try:
        completed_process = subprocess.run(command, capture_output=True, text=True, check=True)


    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，退出码：{e.returncode}\n标准输出：{e.stdout}\n标准错误：{e.stderr}")
    else:
        # 获取标准输出
        output = eval(completed_process.stdout)
        ai_label = output[1]
        acc = output[0]
        print(f"命令执行成功，标准输出：\n{output}")

        # 获取返回码
        return_code = completed_process.returncode
        print(acc,ai_label)
        print(return_code)
        return ai_label,acc

from skimage.io import imread
from skimage.metrics import structural_similarity as compare_ssim

import cv2
def compare_ssim_images(img1_path, img2_path):
    img1 = imread(img1_path)
    img2 = imread(img2_path)
    # 获取img2的尺寸
    height2, width2, _ = img2.shape

    # 调整img1的大小为img2的大小，INTER_LINEAR插值方法提供较好的质量
    img1_resized = cv2.resize(img1, (width2, height2), interpolation=cv2.INTER_LINEAR)
    # 计算SSIM
    ssim_value = compare_ssim(img1_resized, img2, channel_axis=-1)

    return ssim_value

def  SearchImgListView(request):
    # model = Video
    template_name = 'video/ai_detail.html'
    img_path = ''
    ai_label, acc='',''
    recommend_list=[]
    top_three_png_list=[]
    if request.method == 'POST':
        img_path =request.FILES.get('fileToUpload')
        if img_path:
            # 获取文件保存的完整路径
            # 保存上传的图片到默认存储位置
            saved_file_path = default_storage.save(img_path.name, img_path)
            img_path= '/upload/'+img_path.name
            print('img path:',img_path)
            base_dir = '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/recipe-master2'

            png_path =  base_dir+img_path

            print('png_path:++++++',png_path)
            ai_label1, acc = png_api(pre_py=r'/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py', png_path=png_path,model_path='/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/runs/train-cls/food14_exp8/weights/best.pt')

            print(ai_label,acc)
            ai_label='AI分类：apple_pie '+ai_label1
            acc = '准确率：'+str(acc)
            cls_mapping={
                'buildings':1,
                'forest': 2,
                'glacier': 3,
                'mountain': 4,
                'sea': 5,
                'street': 6,
                         }

            zh_cls_mapping = {
                'buildings': '建筑',
                'forest': '森林',
                'glacier': '冰川',
                'mountain': '山脉',
                'sea': '海洋',
                'street': '街道',
            }

            # recommend_list = Video.objects.filter(classification_id=cls_mapping[ai_label1])
            recommend_list = Video.objects.filter(classification_id=int(7))
            max3_recommend_list = []
            for li in recommend_list:
                li_path = os.path.join(base_dir,'upload/'+li.cover.name)

                # print('cover path:',li_path)
                smiler_score = compare_ssim_images(png_path,li_path)
                print('score:',smiler_score)
                max3_recommend_list.append([smiler_score,li])
            top_three_png = sorted(max3_recommend_list, key=lambda x: x[0], reverse=True)[:3]
            print(top_three_png)
            top_three_png_list = [x[1] for x in top_three_png]
        # print('img_path:',img_path,img_path.name)



        return render(request,'video/ai_search.html',context={'png_path':img_path,'ai_label':ai_label,'acc':acc,'recommend_list':top_three_png_list})
    # context_object_name = 'video_list'
    # paginate_by = 8
    # q = ''
    #
    # def get_queryset(self):
    #     self.q = self.request.GET.get("q", "")
    #     return Video.objects.filter(title__contains=self.q).filter(status=0)
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(SearchListView, self).get_context_data(**kwargs)
    #     paginator = context.get('paginator')
    #     page = context.get('page_obj')
    #     page_list = get_page_list(paginator, page)
    #     context['page_list'] = page_list
    #     context['q'] = self.q
    #     return context
class VideoDetailView(generic.DetailView):
    model = Video
    template_name = 'video/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        recommend_list = Video.objects.get_recommend_list()
        context['form'] = form
        context['recommend_list'] = recommend_list
        return context

@ajax_required
@require_http_methods(["POST"])
def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_like(user)
    return JsonResponse({"code": 0, "likes": video.count_likers(), "user_liked": video.user_liked(user)})


@ajax_required
@require_http_methods(["POST"])
def collect(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_collect(user)
    return JsonResponse({"code": 0, "collects": video.count_collecters(), "user_collected": video.user_collected(user)})



