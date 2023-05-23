
def headers_json():
    headers = "../../../../tools/headers_json/headers.txt"
    # headers = "/opt/data_captureAPP/tools/headers_json/headers.txt"

    with open(headers, "r", encoding="utf-8") as f:
        lines = f.readlines()
        line_dict = {}
        for line in range(int(len(lines))):
            lin = lines[line].split(":")
            line_dict[lin[0]] = str(lin[1]).replace("\n", "").replace(" ","")
        return line_dict


if __name__ == '__main__':
    print(type(headers_json()))
