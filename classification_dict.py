import os
import shutil
import argparse
from sklearn.model_selection import train_test_split

def copy(data_dir, train_dir, test_dir):

    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    
    if os.path.exists(data_dir):

        # extension 
        jpg_file = [i for i in os.listdir(data_dir) if i.endswith('.jpg')]
        txt_file = [i for i in os.listdir(data_dir) if i.endswith('.txt')]

        # dataset(8 : 2)
        x_train, x_test, y_train, y_test = train_test_split(jpg_file, txt_file, test_size=0.2, random_state=42)

        # src
        train_image_data= [os.path.join(data_dir, i) for i in x_train]
        test_image_data= [os.path.join(data_dir, i) for i in y_train]
        train_txt_data= [os.path.join(data_dir, i) for i in x_test]
        test_txt_data= [os.path.join(data_dir, i) for i in y_test]

        # copy
        for i in train_image_data:
            shutil.copy(i, train_dir)
        for x in test_image_data:
            shutil.copy(x, train_dir)
        for i in train_txt_data:
            shutil.copy(i, test_dir)
        for x in test_txt_data:
            shutil.copy(x, test_dir)

    else:
        print('path check')

    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Data Path')
    parser.add_argument('-d', '--data_path', required=True, help='Dir with data')
    parser.add_argument('-r', '--train_dir', required=True, help='Train dir')
    parser.add_argument('-t', '--test_dir', required=True, help='Test dir')
    args = parser.parse_args()

    copy(args.data_path, args.train_dir, args.test_dir)
