import os
import shutil


def main(root, output, flag):
    if not os.path.exists(root):
        print("Check root path")
        return

    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    for r, d, f in os.walk(root):
        if flag == "origin":
            file_path = [os.path.join(r, i) for i in f if not 'vis' in i and not 'infer' in i]
            for i in file_path:
                s_i =  os.path.split(i)
                if not s_i[1].startswith('0_vis'):
                    shutil.copy2(i, output)

        if flag == "vis":
            file_path = [os.path.join(r, i) for i in f if 'vis' in i and i.startswith('0')]
            for i in file_path:
                shutil.copy2(i, output)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract original image.")
    parser.add_argument('-i', '--input_root_dir', required=True, help='image root directory')
    parser.add_argument('-o', '--output_dir', required=True, help='output directory')
    parser.add_argument('-f', '--flag', required=True, help='extract image')

    args = parser.parse_args()

    main(args.input_root_dir, args.output_dir, args.flag)
