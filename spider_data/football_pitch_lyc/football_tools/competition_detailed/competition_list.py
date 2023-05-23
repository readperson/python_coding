from tools.json_package.json_package import json_package


def competition_list(rep, base):
    json_package(rep, "gameId", "0", base)
    json_package(rep, "gamename", "0", base)
    json_package(rep, "teamnumber", "0", base)
    json_package(rep, "starttime", "0", base)
    json_package(rep, "portrait", "0", base)
    json_package(rep, "gametype", "0", base)
    # json_package(rep, "game_status", "0", base)
    json_package(rep, "roundRobin", "0", base)
    json_package(rep, "ruleName", "0", base)
    json_package(rep, "statusName", "0", base)
    json_package(rep, "gameTitle", "0", base)
    teamList_count = int(len(rep["teamList"]))
    teamList = []
    for t_count in range(teamList_count):
        teamDict = {}
        json_package(rep["teamList"][t_count], "teamId", "0", teamDict)
        json_package(rep["teamList"][t_count], "teamName", "0", teamDict)
        json_package(rep["teamList"][t_count], "portrait", "0", teamDict)
        json_package(rep["teamList"][t_count], "success", "1", teamDict)
        json_package(rep["teamList"][t_count], "dual", "1", teamDict)
        json_package(rep["teamList"][t_count], "lose", "1", teamDict)
        json_package(rep["teamList"][t_count], "credit", "1", teamDict)
        json_package(rep["teamList"][t_count], "NetScore", "1", teamDict)
        json_package(rep["teamList"][t_count], "closedCredit", "1", teamDict)
        json_package(rep["teamList"][t_count], "closedNetScore", "1", teamDict)
        json_package(rep["teamList"][t_count], "closedScore", "1", teamDict)
        json_package(rep["teamList"][t_count], "haveSmallCycle", "1", teamDict)
        json_package(rep["teamList"][t_count], "rank", "1", teamDict)
        teamList.append(teamDict)
    base["teamList"] = teamList
    return base
