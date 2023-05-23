from tools.json_package.json_package import json_None


def schedule_list(info_schedule):
    matchDict = {}
    json_None(info_schedule, "court_id", "", matchDict)
    json_None(info_schedule, "court_number_id", "", matchDict)
    json_None(info_schedule, "Turns", "", matchDict)
    json_None(info_schedule, "GroupName", "", matchDict)
    json_None(info_schedule, "fieldNumber", "", matchDict)
    json_None(info_schedule, "homeTeamId", "", matchDict)
    json_None(info_schedule, "awayTeamId", "", matchDict)
    json_None(info_schedule, "homeName", "", matchDict)
    json_None(info_schedule, "awayName", "", matchDict)
    json_None(info_schedule, "homeIcon", "", matchDict)
    json_None(info_schedule, "awayIcon", "", matchDict)
    json_None(info_schedule, "homeScore", "", matchDict)
    json_None(info_schedule, "awayScore", "", matchDict)
    json_None(info_schedule, "courtName", "", matchDict)
    json_None(info_schedule, "turnsName", "", matchDict)
    json_None(info_schedule, "gameId", "", matchDict)
    json_None(info_schedule, "matchId", "", matchDict)

    json_None(info_schedule, "description", "", matchDict)
    json_None(info_schedule, "matchTime", "", matchDict)
    return matchDict
