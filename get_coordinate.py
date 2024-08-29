import cv2
import argparse

def click_event(event, x, y, flags, img):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'좌표: ({x}, {y})')
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow('image', img)

def process_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("이미지를 불러올 수 없습니다. 경로를 확인해 주세요.")
        return

    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="이미지에서 포인트 좌표를 추출합니다.")
    parser.add_argument("image_path", type=str, help="처리할 이미지의 경로를 입력하세요.")
    args = parser.parse_args()
    process_image(args.image_path)
