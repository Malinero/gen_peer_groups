# https://en.wikipedia.org/wiki/United_States_Department_of_Defense


def us_dod():
    return [
        "6.0.0.0/8",
        "7.0.0.0/8",
        "11.0.0.0/8",
        "21.0.0.0/8",
        "22.0.0.0/8",
        "26.0.0.0/8",
        "28.0.0.0/8",
        "29.0.0.0/8",
        "30.0.0.0/8",
        "55.0.0.0/8",
        "205.0.0.0/8",
        "214.0.0.0/8",
        "215.0.0.0/8"
    ]


# List of assigned /8 blocks to commercial organisations
def singles():
    return [
        "12.0.0.0/8",  # AT&T
        "17.0.0.0/8",  # Apple
        "19.0.0.0/8",  # Ford Motor
        "38.0.0.0/8",  # Cogent communication
        "48.0.0.0/8",  # Prudential securities
        "53.0.0.0/8",  # Mercedes Benz
        "56.0.0.0/8",  # US postal services
        "73.0.0.0/8",  # Comcast
    ]


def generate(current):
    for entry in us_dod():
        print(entry, "AS%d"%(current))
    for entry in singles():
        current += 1
        print(entry, "AS%d"%(current))
    return current
