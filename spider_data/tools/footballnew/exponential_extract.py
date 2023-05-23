def exponential_extract(rep_data, sectionName):
    # asia_pacific
    asia_pacific = {}
    asia_pacific["sectionName"] = sectionName
    if "oddsHeader" in rep_data["data"]:
        oddsHeader = rep_data["data"]["oddsHeader"]
        asia_pacific["oddsHeader"] = oddsHeader

    oddsList_count = int(len(rep_data["data"]["oddsList"]))
    if oddsList_count > 0:
        print("  " + sectionName, oddsList_count)
    oddsList = []
    for odd_count in range(oddsList_count):
        oddsDict = {}
        companyId = rep_data["data"]["oddsList"][odd_count]["companyId"]
        companyName = rep_data["data"]["oddsList"][odd_count]["companyName"]
        stHome = rep_data["data"]["oddsList"][odd_count]["stHome"]
        stFlat = rep_data["data"]["oddsList"][odd_count]["stFlat"]
        stAway = rep_data["data"]["oddsList"][odd_count]["stAway"]
        instHome = rep_data["data"]["oddsList"][odd_count]["instHome"]
        instHomeRiseOrfall = rep_data["data"]["oddsList"][odd_count]["instHomeRiseOrfall"]
        instFlat = rep_data["data"]["oddsList"][odd_count]["instFlat"]
        instFlatRiseOrfall = rep_data["data"]["oddsList"][odd_count]["instFlatRiseOrfall"]
        instAway = rep_data["data"]["oddsList"][odd_count]["instAway"]
        instAwayRiseOrfall = rep_data["data"]["oddsList"][odd_count]["instAwayRiseOrfall"]
        oddsDict["companyId"] = companyId
        oddsDict["companyName"] = companyName
        oddsDict["stHome"] = stHome
        oddsDict["stFlat"] = stFlat
        oddsDict["stAway"] = stAway
        oddsDict["instHome"] = instHome
        oddsDict["instHomeRiseOrfall"] = instHomeRiseOrfall
        oddsDict["instFlat"] = instFlat
        oddsDict["instFlatRiseOrfall"] = instFlatRiseOrfall
        oddsDict["instAway"] = instAway
        oddsDict["instAwayRiseOrfall"] = instAwayRiseOrfall
        oddsList.append(oddsDict)
    asia_pacific["oddsList"] = oddsList
    return asia_pacific


def exponential_extract_european_compensation(data_european_compensation, sectionName, oddsOtAvgList, indexOtAvgList):
    asia_pacific = {}
    asia_pacific["sectionName"] = sectionName
    asia_pacific["oddsOtAvgList"] = oddsOtAvgList
    asia_pacific["indexOtAvgList"] = indexOtAvgList
    oddsHeader = data_european_compensation["data"]["oddsHeader"]
    asia_pacific["oddsHeader"] = oddsHeader

    oddsList_count = int(len(data_european_compensation["data"]["oddsList"]))
    if oddsList_count > 0:
        print("  " + sectionName, oddsList_count)
    oddsList = []
    for odd_count in range(oddsList_count):
        oddsDict = {}
        companyId = data_european_compensation["data"]["oddsList"][odd_count]["companyId"]
        companyName = data_european_compensation["data"]["oddsList"][odd_count]["companyName"]
        stHome = data_european_compensation["data"]["oddsList"][odd_count]["stHome"]
        stFlat = data_european_compensation["data"]["oddsList"][odd_count]["stFlat"]
        stAway = data_european_compensation["data"]["oddsList"][odd_count]["stAway"]
        instHome = data_european_compensation["data"]["oddsList"][odd_count]["instHome"]
        instHomeRiseOrfall = data_european_compensation["data"]["oddsList"][odd_count]["instHomeRiseOrfall"]
        instFlat = data_european_compensation["data"]["oddsList"][odd_count]["instFlat"]
        instFlatRiseOrfall = data_european_compensation["data"]["oddsList"][odd_count]["instFlatRiseOrfall"]
        instAway = data_european_compensation["data"]["oddsList"][odd_count]["instAway"]
        instAwayRiseOrfall = data_european_compensation["data"]["oddsList"][odd_count]["instAwayRiseOrfall"]
        oddsDict["companyId"] = companyId
        oddsDict["companyName"] = companyName
        oddsDict["stHome"] = stHome
        oddsDict["stFlat"] = stFlat
        oddsDict["stAway"] = stAway
        oddsDict["instHome"] = instHome
        oddsDict["instHomeRiseOrfall"] = instHomeRiseOrfall
        oddsDict["instFlat"] = instFlat
        oddsDict["instFlatRiseOrfall"] = instFlatRiseOrfall
        oddsDict["instAway"] = instAway
        oddsDict["instAwayRiseOrfall"] = instAwayRiseOrfall
        oddsList.append(oddsDict)
    asia_pacific["oddsList"] = oddsList
    return asia_pacific
