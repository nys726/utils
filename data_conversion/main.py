import os
import utiles

label_dir_path = os.path.abspath('labeling')

def run(path):
    if os.path.exists(path):
        file_path = utiles.detailed_path(path)
        for json, jpg in zip(file_path[0], file_path[1]):
            json_script = utiles.read_json(json)
            single_json = utiles.single_line_json(json_script)
            detail_json = utiles.detailed_json(single_json)
            utiles.read_image(jpg, detail_json[0], detail_json[1], detail_json[2])
    else:
        print('check_path')
        return None

if __name__ == "__main__":
    run(label_dir_path)


