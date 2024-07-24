import os
import shutil


def main():
    root = "/Users/nasoo/Downloads/rist/label_data_kim"
    dest = "/Users/nasoo/Downloads/rist/dummy_data"

    for ro, di, fa in os.walk(root):
        for i in fa:
            fp = os.path.join(ro, i)
            if os.path.splitext(fp)[1] == '.jpg':
                sp = os.path.splitext(fp)[0]
                cp = sp+'.json'
                if not os.path.exists(cp):
                    shutil.move(sp+'.jpg', dest)

if __name__=="__main__":
    main()
