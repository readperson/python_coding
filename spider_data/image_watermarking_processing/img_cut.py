import cv2


def img_cut_handle():
    # print(imgpath + "" + imgname)
    img = cv2.imread("./1.jpe")
    # print(img)
    # 高度 宽度
    img = img[0:-150, 0:img.shape[1]]
    # cv2.imwrite("imgpath + "/" + imgname", img)
    cv2.imwrite('../img/cropped_tree1.jpg', img)


if __name__ == '__main__':
    img_cut_handle()
