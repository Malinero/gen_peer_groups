import argparse

import gen_from_geolite as gl
import gen_from_static as gs
import gen_from_urls as gu


def main():
    parser = argparse.ArgumentParser(description="Generate AS mapping file")
    parser.add_argument("--method", choices=["geolite", "urls"], default="geolite", help="Method (%(default)s)")
    parser.add_argument("--include-geolite", action="store_true", help="Include geolite data (require downloading geolite database before)")
    parser.add_argument("--geolite-path", default=["GeoLite2-ASN-Blocks-IPv4.csv", "GeoLite2-ASN-Blocks-IPv6.csv"], nargs="+", help="Path to GeoLite2-ASN-Blocks-IPv4.csv")
    args = parser.parse_args()
    current = 0
    current = gu.generate(current)
    current = gs.generate(current)
    if args.include_geolite:
        gl.generate(args.geolite_path, current)


if __name__ == "__main__":
    main()
