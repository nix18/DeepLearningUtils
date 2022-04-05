# 批量调整图片大小
import os
from PIL import Image
import struct

'''
检查并调整bg图片的宽高，确保宽高都是4的倍数，这样才可以使用ETC压缩格式
'''
size_base = 128

# 遍历目录中的png文件
def list_pic(dirpath):
    for root, dirs, fs in os.walk(dirpath):
        for f in fs:
            if f.endswith('.png') or f.endswith('.jpg'):
                yield os.path.join(root, f)


# 获取图片实际尺寸
def get_png_size(fpath):
    with open(fpath, 'rb') as f:
        f.seek(4 * 4, 0)
        return (struct.unpack(">ii", f.read(8)))


# 列出宽高不是4的倍数的图片
def list_not_4_pic(dirpath):
    for f in list_pic(dirpath):
        w, h = get_png_size(f)
        if w % size_base != 0 or h % size_base != 0:
            yield f


# 调整图片的尺寸，确保宽高是4的倍数
def resize_4_pic(dirpath):
    with open('resize_4_pic.output.log', 'w') as log:
        for f in list_not_4_pic(dirpath):
            img = Image.open(f)
            (w, h) = img.size
            nw = (w % size_base == 0) and w or (w + (size_base - (w % size_base)))
            nh = (h % size_base == 0) and h or (h + (size_base - (h % size_base)))

            print((w, h), '->', (nw, nh), f)
            log.write("%s | (%d,%d)-> (%d,%d)\n" % (f, w, h, nw, nh))
            img = img.resize((nw, nh), Image.ANTIALIAS)
            img.save(f)


if '__main__' == __name__:
    resize_4_pic(r'.\insulator\train\normal')
