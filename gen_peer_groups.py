import argparse
import csv
import re
import requests


GROUPS = {
    # grep -i google GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "google": [139070, 139190, 15169, 16550, 16591, 19527, 36384, 36385, 36492, 395973, 396982, 41264, 43515, 45566],
    # grep -i microsoft GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "ms": [12076, 200517, 23468, 35106, 3598, 45139, 58862, 59067, 6584, 8068, 8069, 8070, 8071, 8075],
    # grep -i -E "amazon|aws-" GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "amazon": [ 14618, 16509, 19047, 22449, 262486, 262772, 263639, 264167, 264344, 264509, 266122, 266194, 267242, 268063, 271017, 271047, 36263, 52994, 61577, 62785, 7224, 8987],
    # grep -i cloudflare GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "cloudflare": [ 132892, 13335, 139242, 202623, 203898, 209242, 395747],
    # grep -i ovh GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "ovh": [16276, 35540],
    # grep -i -E "digital.*ocean" GeoLite2-ASN-Blocks-IPv4.csv | cut -d , -f 2 | sort | uniq
    "digitalocean": [14061, 205301, 209396, 39690],
    # https://ipinfo.io/countries/ma
    "morocco": [6713, 36925, 36903, 36884, 30983, 36941, 327989, 328066, 328867, 328055, 328577, 328709, 328493, 328671, 328541, 327917, 328272, 328280, 328799, 37450, 328268, 37787, 328960, 36956]
}

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


def generate_from_geolite(paths):
    data = {"asn": dict(), "org": dict()}
    for path in paths:
        reader = csv.DictReader(open(path, "r"))
        for row in reader:
            org = row['autonomous_system_organization']
            asn = row['autonomous_system_number']
            
            for k,v in GROUPS.items():
                if int(asn) in v:
                    org = k
                    break
            if not org in data["org"]:
                data["org"][org] = set()
            data["org"][org].add(asn)
    
            if not asn in data["asn"]:
                data["asn"][asn] = set()
            data["asn"][asn].add(row['network'])

    for index, org in enumerate(sorted(data["org"].keys())):
        index += 1
        for asn in data["org"][org]:
            for address in data["asn"][asn]:
                print(address, "AS%d"%(index))


def generate_from_url():
    current = 0
    for config in [aws, azure, cloudflare, google, us_dod]:
        current += 1
        for entry in config():
            print(entry, "AS%d"%(current))


def main():
    parser = argparse.ArgumentParser(description="Generate AS mapping file")
    parser.add_argument("--method", choices=["geolite", "urls"], default="geolite", help="Method (%(default)s)")
    parser.add_argument("--path", default=["GeoLite2-ASN-Blocks-IPv4.csv", "GeoLite2-ASN-Blocks-IPv6.csv"], nargs="+", help="Path to GeoLite2-ASN-Blocks-IPv4.csv")
    args = parser.parse_args()
    if args.method == "geolite":
        generate_from_geolite(args.path)
    elif args.method == "urls":
        generate_from_url()
    else:
        raise ValueError("bug")


if __name__ == "__main__":
    main()
