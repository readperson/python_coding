import requests
# FE 点击
url = "https://log-api.pangolin-sdk-toutiao.com/service/2/app_log/"
headers = {
    "ss-sign": "006e09ea47d0371f6403ec25e68bfaaf9a86ca229e995d80d3723b6c77d5e48a583e09a7b71aed9f42fce928688c7ebf839887f7a1753c79f6e17621c53a9a3066ed0f2f25797f7103e40f4443795f196e6377857c9d3d4a1db06c3f17e6fe3476c47160165fb392f6dd94145309ba03ef7975e6cca89e5c1589063693b9764b06787fe3a1935df06c37",
    "Content-Type": "application/json; charset=utf-8"
}
data ={"message":"23fbe1d16e7a95484k8Dhe8ibtdW+mo\/82hF+MzCqTuwieuUWzhhdqhWbDmGBBzvmZuk62lkSqVq0bA+yAWFWUzSb0GRT\nXsPMLNaMi19FZHidcZxnVVwQ5pv9cXHVS61aSBvg6cqd3Z2bmrJpXhzWhTd\/j\/qHk1aA7Q4NP6ya\nMJkiYIvyven1nsy4QvIXj7Ly1rYPgqVOWoeYWgAo8NnW+85L0N8u06GFz6wEeQq3AW9ydH0dtzyF\n6l7AaBwDRZBWtfvoGu7ybUG7FFe18+Ip4tJcd3hmKvFUSVpGFy54J6RYXvCALgD2VZGJSd3sgtjM\nenJb9dC7\/SJZOuFzNGXDKrOZ0Ek9LLK9pZsGt7nNrENgZYA7haG8I7JeW7pFR+YWocrLG4VkQD0g\nawFsgnmINaW1ZfzEd\/sOBPmqByebf7BRTRH07Q9r6XCEKcaS3qF\/UU1SR98vO1YBuPS7zT1UwBJB\nqPszhDWZkclxmVFLBw7qJFcAJH526xavCv0N5fuiSy3e3ZNYpTUWVGQiVaKDeuILnqXJsPC22QMO\n7AF43HTR70e7fuwD4pCM7m7dq0RMLGMMh589NRPQ6GMVOgtz1XvddZ\/P7fC1a3azioYCJcndjtuE\n071tPBwjrFLDc9qOvJvEY1ZDeBOE94XuN2Xf1RiUMw+MtNQggPvbmxKSFLmJmKIY8X0BlvaV5wV9\nV1rsawpV03\/YqZvg4WUeTr7c7gJjDqC0Cl1yLNL+FYA2q\/uXZykq9QgafCqdQW7TqnFHYGIxiMkm\nGPpaA9XQorRqcDjCV6ni9idVRzG2aGk513qZXk58XgjR0RZYI1s\/o2wyirMGsIBG5XdNQ1\/66Fuh\nk0V8q91xj4txqToHjHE0YIZppef9u4OIdT4lWrm9XRKwO5hzzoRtDGUI2\/2KeRgKCKvt9xEozfIN\nXbsGDIzPS4rxX3ESRkY3BKdsJyUKsq0E1VX9UKtv9D0UIVLwYTLk91tTe8gSi+S4zRx8ZvMlCzsX\n8baX\/Vxi8yo0TbF7UNSXeK1ty8Zf62ypAnDI\/AWLRFc74CLirR00onivDdA1FXtSG4LLojqpxp4s\ngeaOUQRXyrTEIQz934xh2HKhJaGmtsNsR5wNuEA\/Tucuo0aB97ugggPrQkxtbtbSbf6ycG9dB6XS\nvkCmk\/n+AmDbbq\/5TdZI4Yj6+QkFFYLQ\/EErJxRjm7fNhqXhebYq\/FTPlJXe2wzk\/A0EfMz71LFR\nBVXzgzDKN5odc8cRBsI39TqHflCJIl2jdQ5JNuY\/XLYWWj6kyiw91vo1hXPRLZyrG0HH8FzFwGIr\nktyOeZAFyc1eW+1DAJL1A+9RAxskBtJ\/VtQE6rAhMFYi\/ygao7jZeqaQYcZPcag7\/IkON0EQCJMm\np1mDuwqu4d96leFCZwNOTBqrjHc4qP641I9u+x\/hN\/8PXreROLm4X\/zDFxk4fgKUmEJbKSWxFJX1\nBU61UhGPGkC2sfGjMlSsBroYpPLXlCM\/8IpRzMhpvv8pfjFhS3R5KbdZHoNvGKK2ZP1U9IC6I70E\nARL8tpSKs6JZ4EfjfqPTlqpxZmZePAEyFHE4\/Jck4ViyYqdEI3GHc3AnZJVAgR+yHVuB2\/r1MyLU\ntsgZroc1bm3l6jb4XvFXNBA9t56ILvF\/FUg5KUE3fxPv8Zmheyaf3gftI7vxthlnv5LWaO2BR16C\ncEeyrOdE97rTw4lS+97cR14o4kQbopkpd3FRlPzjLbBpppwn2xLvg2IThlEgQBgO3JBIGYwCjWix\n+6s\/7p8OIZW\/\/xs0\/ON3o3fl2GW3A7h\/h39aFfpDSoC\/8lbh9PXPNzESnSYUh4e1zajA9Uhy0QgE\n2\/cjFhOE\/b7BWI6p9u+ogU1ESq95fam3F6HjdwFSHDyfDY9zraz7UeK9tZUrAPaAosrJ946Ku+kI\nuH7E9lSwt7Wh+flDWFj5UE5eUCxm2z\/MPP\/DtkKXOAlPXBLt6yHdlkayJtY1AgBC1OHhLaCJqZDF\ncdjmebA4zeKKZ5asDHPDJrvMcnk3kQ==\n","cypher":2,"ad_sdk_version":"3.3.0.0"}

rep = requests.post(url=url,headers=headers,data=data).text
print(rep)