def gameid_return_list():
    # r_file = "game_id_list.txt"
    # D:\pythonworkspace\data_captureAPP\football_pitch_lyc\football_tools\match\game_id_list.txt
    r_file = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/game_id_list.txt"
    with open(r_file, "r", encoding="utf-8") as f:
        gameid = f.read().replace("'", "").replace('[', "").replace("]", "").split(", ")
        gameid = list(set(gameid))
        gameid.sort()
        return gameid
