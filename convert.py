import cv2
import os

mq3 = '/Users/nasoo/Project/hundai/c_data/VisionCam/mq3/image'
mq4 = '/Users/nasoo/Project/hundai/c_data/VisionCam/mq4/image'
dest = '/Users/nasoo/Project/hundai/dest'

def test(file):
    li = []
    a = os.listdir(file)
    for i in a:
        join_a = os.path.join(mq4,i)
        join_d = os.path.join(dest,i)

        src = cv2.imread(join_a, cv2.IMREAD_GRAYSCALE)
        dst = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)
        wri = cv2.imwrite(join_d, dst)
        read = cv2.imread(join_d)
        print('ndim :', read.ndim)


if __name__ == "__main__":
    test(mq4)
