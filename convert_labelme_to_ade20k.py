import json
import os
import numpy as np
from PIL import Image
import labelme
import glob

# 고정된 색상 맵
label_colors = {
    '_background_': [0, 0, 0],  # 검정색
    'scrap': [255, 0, 0],  # 빨간색
    'etc': [0, 255, 0],  # 초록색
}

def labelme_to_ade20k(json_file, output_mask_dir, output_colored_mask_dir):
    with open(json_file) as f:
        data = json.load(f)

    label_map = {'_background_': 0}
    for shape in data['shapes']:
        label = shape['label']
        if label not in label_map:
            label_map[label] = len(label_map)

    height = data['imageHeight']
    width = data['imageWidth']
    mask = np.zeros((height, width), dtype=np.uint8)
    colored_mask = np.zeros((height, width, 3), dtype=np.uint8)

    for shape in data['shapes']:
        points = shape['points']
        label = shape['label']
        value = label_map[label]
        shape_mask = labelme.utils.shape_to_mask((height, width), points, shape['shape_type'])
        mask[shape_mask] = value
        colored_mask[shape_mask] = label_colors.get(label, [255, 255, 255])  # 기본값: 흰색

    output_mask_path = os.path.join(output_mask_dir, os.path.splitext(os.path.basename(json_file))[0] + '.png')
    Image.fromarray(mask).save(output_mask_path)

    output_colored_mask_path = os.path.join(output_colored_mask_dir, os.path.splitext(os.path.basename(json_file))[0] + '_colored.png')
    Image.fromarray(colored_mask).save(output_colored_mask_path)

def main(labelme_dir, output_mask_dir, output_colored_mask_dir):
    if not os.path.exists(output_mask_dir):
        os.makedirs(output_mask_dir)

    if not os.path.exists(output_colored_mask_dir):
        os.makedirs(output_colored_mask_dir)

    json_files = glob.glob(os.path.join(labelme_dir, '*.json'))
    for json_file in json_files:
        labelme_to_ade20k(json_file, output_mask_dir, output_colored_mask_dir)
        print(f"Processed {json_file}")

if __name__ == "__main__":
    labelme_dir = '/Users/nasoo/Downloads/rist/label_data_kim'
    output_mask_dir = '/Users/nasoo/Downloads/rist/output'
    output_colored_mask_dir = '/Users/nasoo/Downloads/rist/color_mask'
    main(labelme_dir, output_mask_dir, output_colored_mask_dir)
