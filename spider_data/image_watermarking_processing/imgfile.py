import cv2

with open("imgs.txt", "r", encoding="utf-8") as f:
    lens = f.readlines()
    print(len(lens))
    for i in range(int(len(lens))):
        file_name = str(lens[i]).replace('\n', "")
        img = cv2.imread(file_name)
        if img is not None:
            print("===============", file_name, i + 1)
            # print(img)
            # 高度,宽度
            img = img[0:-150, 0:img.shape[1]]
            if img.size != 0:
                cv2.imwrite("E:/img/" + file_name, img)
            else:
                print("======图片为0=====", file_name)
                # with open("/opt/linux-x64_netcoreapp3.1/content/ground_img/" + file_name, "rb") as fr:
                #     img_content = fr.read()
                #     with open("/home/ground_img/" + file_name, "wb") as fw:
                #         fw.write(img_content)

                continue
        else:
            print("======图片为None=====")
            continue
