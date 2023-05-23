def gameid_return_list():
    r_file = "../../../../tools/ID_file/gameId.txt"
    # r_file = "/opt/data_captureAPP/tools/ID_file/gameId.txt"
    with open(r_file, "r", encoding="utf-8") as f:
        gameid = f.read().replace("'", "").replace('[', "").replace("]", "").split(", ")
        gameid = list(set(gameid))
        gameid.sort()
        return gameid
