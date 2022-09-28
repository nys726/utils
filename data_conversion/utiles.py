import cv2
import os
import json
import numpy as np
import coco_cate as co

label_file_path = os.path.abspath('test/ori/a1/dog.json')


def check_to_ext_list(path, ext):
    if os.path.exists(path):
        extension = os.path.splitext(path)[-1]
        if extension == ext:
            return path
        else:
            return None
    else:
        return None


def read_image(path, pts, cate, ar):
    # color = coloring_by_category(cate)
    basename = os.path.basename(path)
    split_name = os.path.splitext(basename)[0]
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    label_img = np.zeros((img.shape[0], img.shape[1]), np.int8)
    for pt, col, a in zip(pts, cate, ar):
        arr = np.array(pt).reshape(1, -1, 2)
        cv2.fillPoly(label_img, np.array(arr), (col), cv2.LINE_AA)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', label_img)
        key = cv2.waitKey(0)
        if key == 27: # esc
            cv2.destroyAllWindows()
            break

    return cv2.imwrite('copy/'+split_name+'.png', label_img)


def read_json(path):
    print()
    print('[==============:', path, ':===============]\n')
    with open(path, "r") as js:
        js_dic = json.loads(js.read())

        return js_dic


def single_line_json(data):
    sorted_arr = sorted(data['annotations'], key=lambda x: (-x['area'], x['category_id']))

    return sorted_arr


def detailed_json(sing_json):
    location_name = [j for i in sing_json for j in i['segmentation']]   # 좌표
    category_id = [j for i in sing_json for j in [i['category_id']]]    # 카테고리
    area = [j for i in sing_json for j in [i['area']]]    # 너비

    return location_name, category_id, area


def detailed_path(path):
    json_li = []
    jpg_li = []
    for pt, dr, files in os.walk(path):
        for file in files:
            file_path = os.path.join(pt, file)
            if check_to_ext_list(file_path, '.json'):
                json_li.append(file_path)
            elif check_to_ext_list(file_path, '.jpg'):
                jpg_li.append(file_path)
    return json_li, jpg_li


# category color check
def coloring_by_category(cate_id):
    coco_data = co.COCO_CATEGORIES
    li = []
    for cat in cate_id:
        for i in coco_data:
            if cat == i['id']:
                color= i['color']
                color_tu = tuple(color)
                li.append(color_tu)
    return li


if __name__ == "__main__":
#      a = check_to_ext_list(label_file_path, '.json')
    a=label_file_path
    b = read_json(a)
    c = single_line_json(b)
    i, j, k = detailed_json(c)
#     d = detailed_json(c)
#     e = detailed_name(b)
#     coloring_by_category(d)
#     f = read_image(e, d[0], d[1], d[2])

