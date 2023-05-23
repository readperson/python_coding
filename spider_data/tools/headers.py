def headers_header():
    # headers = "/opt/data_captureAPP/tools/headers.txt"
    headers = "../tools/headers.txt"
    # headers = "../headers.txt"

    with open(headers, "r", encoding="utf-8") as f:
        lines = f.readlines()
        source = lines[0].split(": ")[1].replace("\n", "")
        lytime = lines[1].split(": ")[1].replace("\n", "")
        deviceid = lines[2].split(": ")[1].replace("\n", "")
        deviceaid = lines[3].split(": ")[1].replace("\n", "")
        requestRam = lines[4].split(": ")[1].replace("\n", "")
        sign = lines[5].split(": ")[1].replace("\n", "")
        return source, lytime, deviceid, deviceaid, requestRam, sign


if __name__ == '__main__':
    print(headers_header())
