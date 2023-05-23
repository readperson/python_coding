def matchid_return_list():
    r_file = "../matchId.txt"
    # r_file = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/matchId.txt"
    with open(r_file, "r", encoding="utf-8") as f:
        matchid = f.read().replace("'", "").replace('[', "").replace("]", "").split(", ")
        matchid = list(set(matchid))
        matchid.sort()
        return matchid
