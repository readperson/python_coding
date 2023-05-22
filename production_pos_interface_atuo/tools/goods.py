goods_dict = {}


def set_goods(goods):
    goods_dict["goods"] = goods


def get_goods():
    return goods_dict.get("goods")


if __name__ == '__main__':
    set_goods("米")
    print(get_goods())
