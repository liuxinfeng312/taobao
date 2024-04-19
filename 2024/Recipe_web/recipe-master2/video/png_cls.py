
import os
import subprocess


def png_api(pre_py,png_path,model_path):

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

# png_api(pre_py=r'/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py',png_path=r'/Users/xfliu/PycharmProjects/taobao/2024/landscape_web/landscape-master/upload/20071.jpg',
#         model_path='/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/runs/train-cls/fengjing/weights/best.pt')
from skimage.io import imread
from skimage.metrics import structural_similarity as compare_ssim
import matplotlib.pyplot as plt

def compare_ssim_images(img1_path, img2_path):
    img1 = imread(img1_path)
    img2 = imread(img2_path)

    # 计算SSIM
    ssim_value = compare_ssim(img1, img2, channel_axis=-1)



    return ssim_value

# 使用函数
ssim_score = compare_ssim_images('/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/seg_test/train/buildings/20057.jpg',\
                                 '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/seg_test/train/buildings/20060.jpg')
ssim_score = compare_ssim_images('/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/seg_test/train/buildings/20057.jpg',\
                                 '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/seg_test/train/sea/20115.jpg')
