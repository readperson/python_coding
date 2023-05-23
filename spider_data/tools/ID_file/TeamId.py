def teamid_w(teamId):
    teamId = list(set(teamId))
    teamId.sort()
    print("teamId 共有", len(teamId), "个")
    teamId = str(teamId)
    # w_file = "../../../tools/ID_file/TeamId.txt"
    w_file = "/opt/data_captureAPP/tools/ID_file/TeamId.txt"
    with open(w_file, "w", encoding="utf-8") as f:
        f.write(teamId)
