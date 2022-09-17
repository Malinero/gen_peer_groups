import re
import requests


# NB: doesn't take into account https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-byoip.html
def aws():
    ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()
    ipv4 = [item["ip_prefix"] for item in ip_ranges["prefixes"]]
    ipv6 = [item["ipv6_prefix"] for item in ip_ranges["ipv6_prefixes"]]
    return ipv4 + ipv6


def azure():
    response = requests.get("https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519")
    found = re.search("href=\"https://download\.microsoft\.com/download/.*/ServiceTags_Public_.*\.json\"", response.text)
    if not found:
        raise ValueError("Failed to extract Azure download url")
    response = requests.get(found.group()[len('href="'):-1])
    res = []
    for entry in response.json()["values"]:
        res.extend(entry["properties"]["addressPrefixes"])
    return res


def cloudflare():
    return requests.get("https://www.cloudflare.com/ips-v4").text.split("\n") + requests.get("https://www.cloudflare.com/ips-v6").text.split("\n")


def google():
    def _get_google(url):
        prefixes = requests.get("https://www.gstatic.com/ipranges/goog.json").json()["prefixes"]
        return [p["ipv4Prefix"] if "ipv4Prefix" in p else p["ipv6Prefix"] for p in prefixes]
    return _get_google("https://www.gstatic.com/ipranges/goog.json") + _get_google("https://www.gstatic.com/ipranges/cloud.json")


# https://en.wikipedia.org/wiki/United_States_Department_of_Defense
def us_dod():
    return ["6.0.0.0/8", "7.0.0.0/8", "11.0.0.0/8", "21.0.0.0/8", "22.0.0.0/8", "26.0.0.0/8", "28.0.0.0/8", "29.0.0.0/8", "30.0.0.0/8", "55.0.0.0/8", "205.0.0.0/8", "214.0.0.0/8", "215.0.0.0/8"]


def generate(current):
    for config in [aws, azure, cloudflare, google, us_dod]:
        current += 1
        for entry in config():
            print(entry, "AS%d"%(current))
    return current
