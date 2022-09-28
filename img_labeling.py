import os
from sys import flags
import cv2
import shutil
import numpy as np


def get_image(root):
    for path, dir, file in os.walk(root):
        file_path = [os.path.join(path, i) for i in file]
        png_path = [i for i in file_path if i.endswith('png')]

    return png_path

def check_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def main(root, normal, abnormal):

    png_path = get_image(root)
    normal = os.path.join(root, normal)
    abnormal = os.path.join(root, abnormal)

    check_dir(normal)
    check_dir(abnormal)

    for idx, img in enumerate(png_path):
        print(f'current : {idx+1} / {len(png_path)}')
        origin_img = cv2.imread(img, cv2.IMREAD_COLOR)
        cv2.namedWindow(img, flags=cv2.WINDOW_NORMAL)
        cv2.imshow(img, origin_img)

        if cv2.waitKey() == ord('1'):
            print(f'normal: {img}')
            shutil.copy2(img, normal)
            cv2.destroyAllWindows()
        else:
            print(f'abnormal: {img}')
            shutil.copy2(img, abnormal)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main('220826', 'normal', 'abnormal')
