import csv


ASN_GROUPS = {
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


def generate(paths, current):
    data = {"asn": dict(), "org": dict()}
    for path in paths:
        reader = csv.DictReader(open(path, "r"))
        for row in reader:
            org = row['autonomous_system_organization']
            asn = row['autonomous_system_number']

            for k,v in ASN_GROUPS.items():
                if int(asn) in v:
                    org = k
                    break
            if not org in data["org"]:
                data["org"][org] = set()
            data["org"][org].add(asn)

            if not asn in data["asn"]:
                data["asn"][asn] = set()
            data["asn"][asn].add(row['network'])

    for org in sorted(data["org"].keys()):
        current += 1
        for asn in data["org"][org]:
            for address in data["asn"][asn]:
                print(address, "AS%d"%(current))
    return current
