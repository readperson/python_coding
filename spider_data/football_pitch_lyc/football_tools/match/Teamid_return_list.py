def teamid_return_list():
    # r_file = "../TeamId.txt"
    r_file = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/TeamId.txt"
    with open(r_file, "r", encoding="utf-8") as f:
        teamId = f.read().replace("'", "").replace('[', "").replace("]", "").split(", ")
        teamId = list(set(teamId))
        teamId.sort()
        return teamId
