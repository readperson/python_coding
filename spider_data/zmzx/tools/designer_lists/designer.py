def designer(designer_lists):
    designer_lists = list(set(designer_lists))
    designer_lists.sort()
    print("designer_lists 共有", len(designer_lists), "个")
    designer_lists = str(designer_lists)
    ddesigner = "designer_id.txt"
    with open(ddesigner, "w", encoding="utf-8") as f:
        f.write(designer_lists)
