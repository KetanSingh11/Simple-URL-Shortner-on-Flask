
MAP = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "0123456789"    #sequence matters
BASE = len(MAP)

def shorten(long_url_id):
    global MAP
    global BASE
    short_url = ""

    while long_url_id > 0:
        short_url = short_url + MAP[long_url_id%BASE]
        long_url_id = long_url_id // BASE

    return short_url[::-1]


def unshorten(short_str):
    global MAP
    global BASE
    num = 0

    for char in short_str:
        num = num * BASE + MAP.index(char)

    return num


if __name__ == "__main__":
    print(shorten(9894487878))
    print(unshorten("kXMqsk"))