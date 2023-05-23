def gameId_w(gameId):
    gameId = list(set(gameId))
    gameId.sort()
    print("gameId 共有", len(gameId), "个")
    gameId = str(gameId)
    # w_file = "../../../tools/ID_file/gameId.txt"
    w_file = "/opt/data_captureAPP/tools/ID_file/gameId.txt"
    with open(w_file, "w", encoding="utf-8") as f:
        f.write(gameId)
