def matchId_w(matchId):
    matchId = list(set(matchId))
    matchId.sort()
    print("matchId 共有", len(matchId), "个")
    matchId = str(matchId)
    # w_file = "matchId.txt"
    w_file = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/matchId.txt"
    with open(w_file, "w", encoding="utf-8") as f:
        f.write(matchId)
