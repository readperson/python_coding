def teamid_return_list():
    r_file = "../../../tools/ID_file/TeamId.txt"
    # r_file = "/opt/data_captureAPP/tools/ID_file/TeamId.txt"
    with open(r_file, "r", encoding="utf-8") as f:
        teamId = f.read().replace("'", "").replace('[', "").replace("]", "").split(", ")
        teamId = list(set(teamId))
        teamId.sort()
        return teamId
