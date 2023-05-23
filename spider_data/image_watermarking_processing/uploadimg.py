from PIL import Image


def img_stream_file():
    with open("../img/10.jpg", "rb") as f:
        img_stream = f.read()
        print(img_stream)
    #     with open("../img/")

    # with open(path + "" + img_name, "wb") as f:
    # open("test.jpg", "rb").read()
    # img_stream =cv2.imshow("../img/5138e7a8eb3af25900f84f4f71610188.jpg")
    # Image.

    # img = cv2.imread("../img/5138e7a8eb3af25900f84f4f71610188.jpg")
    # res = {"image": str(img.tolist()).encode('base64')}
    # print(res)

    # img_stream = Image.open("../img/5138e7a8eb3af25900f84f4f71610188.jpg")
    # width, height = img_stream.size
    # fh = open('../img/1.txt', 'w')
    # for i in range(height):
    #     for j in range(width):
    #         # 获取像素点颜色
    #         color = img_stream.getpixel((j, i))
    #         colorsum = color[0] + color[1] + color[2]
    #         if (colorsum == 0):
    #             fh.write('1')
    #         else:
    #             fh.write('0')
    #     fh.write('\n')
    # fh.close()

    # img = Image.open(filename)
    # bytesIO = BytesIO()
    # img.save(bytesIO, format='PNG')
    # print(bytesIO.getvalue())


if __name__ == '__main__':
    img_stream_file()
