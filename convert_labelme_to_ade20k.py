import json
import os
import numpy as np
from PIL import Image
import labelme
import glob

def labelme_to_ade20k(json_file, output_mask_dir):
    # Read the JSON file
    with open(json_file) as f:
        data = json.load(f)

    # Create the label map
    label_map = {}
    for shape in data['shapes']:
        label = shape['label']
        if label not in label_map:
            label_map[label] = len(label_map) + 1

    # Create a blank mask image
    height = data['imageHeight']
    width = data['imageWidth']
    mask = np.zeros((height, width), dtype=np.uint8)

    # Fill the mask with the label values
    for shape in data['shapes']:
        points = shape['points']
        label = shape['label']
        value = label_map[label]
        mask = labelme.utils.shape_to_mask((height, width), points, shape['shape_type'])
        mask[mask > 0] = value

    # Save the mask as a PNG file
    output_mask_path = os.path.join(output_mask_dir, os.path.splitext(os.path.basename(json_file))[0] + '.png')
    Image.fromarray(mask).save(output_mask_path)

def main(labelme_dir, output_mask_dir):
    if not os.path.exists(output_mask_dir):
        os.makedirs(output_mask_dir)

    json_files = glob.glob(os.path.join(labelme_dir, '*.json'))
    for json_file in json_files:
        labelme_to_ade20k(json_file, output_mask_dir)
        print(f"Processed {json_file}")

if __name__ == "__main__":
    labelme_dir = '/Users/nasoo/Downloads/rist/label_data_kim'
    output_mask_dir = '/Users/nasoo/Downloads/rist/mask'
    main(labelme_dir, output_mask_dir)

