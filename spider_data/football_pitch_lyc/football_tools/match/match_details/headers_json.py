def headers_json():
    headers = "headers.txt"
    # headers = "/opt/data_captureAPP/football_pitch_lyc/football_tools/match/match_details/headers.txt"

    with open(headers, "r", encoding="utf-8") as f:
        lines = f.readlines()
        line_dict = {}
        for line in range(int(len(lines))):
            lin = lines[line].split(":")
            line_dict[lin[0]] = str(lin[1]).replace("\n", "").replace(" ","")
        return line_dict


if __name__ == '__main__':
    print(type(headers_json()))
