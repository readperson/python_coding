def gameId_w(gameId):
    gameId = list(set(gameId))
    gameId.sort()
    print("gameId 共有", len(gameId), "个")
    gameId = str(gameId)
    # w_file = "game_id_list.txt"
    w_file = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/game_id_list.txt"
    with open(w_file, "w", encoding="utf-8") as f:
        f.write(gameId)
