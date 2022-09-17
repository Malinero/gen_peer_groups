# Generate peer grouping file

## Generate mapping file


```sh
python main.py > mapping.txt
```

### GeoIP

Download GeoLite2-ASN-Blocks-IPv4.csv/GeoLite2-ASN-Blocks-IPv6.csv from maxmind (requires email)

```sh
python main.py --include-geolite --path /path/to/GeoLite2-ASN-Blocks-IPv*.csv > mapping.txt
```


## Compress mapping file

```sh
git clone https://github.com/sipa/asmap -b nextgen
cd asmap
python3 asmap-tool.py encode ../mapping.txt mapping.bin
```


## Monero usage

```sh
monerod --asmap /path/to/mapping.bin ....
```
