from tools.json_package.json_package import json_package
import random


# 球队
def ball_game_lists(rep):
    ball_game_dict = {}
    list_status = ["A", "B"]
    index = random.randint(0, 1)
    ball_game_dict["groupName"] = list_status[index]

    json_package(rep, "status", "0", ball_game_dict)
    json_package(rep, "teamId", "0", ball_game_dict)
    json_package(rep, "teamName", "0", ball_game_dict)
    json_package(rep, "teamPortrait", "0", ball_game_dict)

    return ball_game_dict
