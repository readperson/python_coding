def record_extract(rep_data, j, sectionName, home_name, away_name):
    history_count = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
    record_extract_dict = {}
    record_extract_dict["sectionName"] = sectionName
    leagueMatchList_list = []
    for hE_count in range(history_count):
        leagueMatchList_dict = {}

        histroy_homeName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["teamName"]
        # 赢
        teamRecordWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["teamRecordWin"]

        # 平
        teamRecordTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["teamRecordTie"]

        # 输
        teamRecordLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["teamRecordLost"]
        textColorWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["textColorWin"]
        textColorTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["textColorTie"]
        textColorLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]["textColorLost"]
        if "competitionDataOdds" in rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count]:
            competitionDataOdds = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][hE_count][
                "competitionDataOdds"]
            if int(len(competitionDataOdds)) > 0:
                print("  " + sectionName, int(len(competitionDataOdds)))
            leagueMatchList_dict["homeName"] = histroy_homeName
            leagueMatchList_dict["teamRecordWin"] = teamRecordWin
            leagueMatchList_dict["teamRecordTie"] = teamRecordTie
            leagueMatchList_dict["teamRecordLost"] = teamRecordLost
            leagueMatchList_dict["textColorWin"] = textColorWin
            leagueMatchList_dict["textColorTie"] = textColorTie
            leagueMatchList_dict["textColorLost"] = textColorLost

            competitionDataOdds_list = []
            for titionData_count in range(int(len(competitionDataOdds))):
                competitionDataOdds_dict = {}
                if competitionDataOdds[titionData_count]["home"] == "客":
                    competitionDataOdds_dict["away_name"] = away_name
                    competitionDataOdds_dict["competitionId"] = competitionDataOdds[titionData_count]["competitionId"]
                    competitionDataOdds_dict["competitionName"] = competitionDataOdds[titionData_count][
                        "competitionName"]
                    competitionDataOdds_dict["date"] = competitionDataOdds[titionData_count]["date"]
                    competitionDataOdds_dict["score"] = competitionDataOdds[titionData_count]["score"]
                    competitionDataOdds_dict["halfScore"] = competitionDataOdds[titionData_count]["halfScore"]
                    competitionDataOdds_dict["home_name"] = home_name
                    if "let" in competitionDataOdds[titionData_count]:
                        competitionDataOdds_dict["let"] = competitionDataOdds[titionData_count]["let"]
                    else:
                        competitionDataOdds_dict["let"] = competitionDataOdds[titionData_count].setdefault("let", "")

                    competitionDataOdds_dict["winOrLose"] = competitionDataOdds[titionData_count]["winOrLose"]
                    competitionDataOdds_dict["bigSmall"] = competitionDataOdds[titionData_count]["bigSmall"]
                    competitionDataOdds_dict["home"] = competitionDataOdds[titionData_count]["home"]
                    competitionDataOdds_dict["away"] = competitionDataOdds[titionData_count]["away"]
                    competitionDataOdds_list.append(competitionDataOdds_dict)

                if competitionDataOdds[titionData_count]["home"] == "主":
                    competitionDataOdds_dict["home_name"] = home_name
                    competitionDataOdds_dict["competitionId"] = competitionDataOdds[titionData_count]["competitionId"]
                    competitionDataOdds_dict["competitionName"] = competitionDataOdds[titionData_count][
                        "competitionName"]
                    competitionDataOdds_dict["date"] = competitionDataOdds[titionData_count]["date"]
                    competitionDataOdds_dict["score"] = competitionDataOdds[titionData_count]["score"]
                    competitionDataOdds_dict["halfScore"] = competitionDataOdds[titionData_count]["halfScore"]
                    competitionDataOdds_dict["away_name"] = away_name
                    if "let" in competitionDataOdds[titionData_count]:
                        competitionDataOdds_dict["let"] = competitionDataOdds[titionData_count]["let"]
                    else:
                        competitionDataOdds_dict["let"] = competitionDataOdds[titionData_count].setdefault("let", "")
                    competitionDataOdds_dict["winOrLose"] = competitionDataOdds[titionData_count]["winOrLose"]
                    competitionDataOdds_dict["bigSmall"] = competitionDataOdds[titionData_count]["bigSmall"]
                    competitionDataOdds_dict["home"] = competitionDataOdds[titionData_count]["home"]
                    competitionDataOdds_dict["away"] = competitionDataOdds[titionData_count]["away"]
                    competitionDataOdds_list.append(competitionDataOdds_dict)
        else:
            competitionDataOdds_list = []

        leagueMatchList_dict["competitionDataOdds"] = competitionDataOdds_list
        leagueMatchList_list.append(leagueMatchList_dict)
        record_extract_dict["leagueMatchList_list"] = leagueMatchList_list
    return record_extract_dict
