import os
import json
import math
import requests
import socket
import urllib.request

DNS_NODE = {
    'host': "p5-dns.5700.network",
    'ip': "45.33.90.91",
    "latitude": 40.738731384277344,
    "longitude": -74.19452667236328
}
# REPLICA_INFO = [
#     {
#         'host': "p5-http-b.5700.network",
#         'ip': "45.33.50.187",
#         "latitude": 37.5625,
#         "longitude": -122.0004
#     },
# ]
REPLICA_INFO = [
    {
        'host': "p5-http-a.5700.network",
        'ip': "50.116.41.109",
        "latitude": 33.844,
        "longitude": -84.4784
    },
    {
        'host': "p5-http-b.5700.network",
        'ip': "45.33.50.187",
        "latitude": 37.5625,
        "longitude": -122.0004
    },
    {
        'host': "p5-http-c.5700.network",
        'ip': "194.195.121.150",
        "latitude": -33.8715,
        "longitude": 151.2006
    },
    {
        'host': "p5-http-d.5700.network",
        'ip': "172.104.144.157",
        "latitude": 50.1188,
        "longitude": 8.6843
    },
    {
        'host': "p5-http-e.5700.network",
        'ip': "172.104.110.211",
        "latitude": 35.6893,
        "longitude": 139.6899
    },
    {
        'host': "p5-http-f.5700.network",
        'ip': "88.80.186.80",
        "latitude": 51.5095,
        "longitude": -0.0955
    },
    {
        'host': "p5-http-g.5700.network",
        'ip': "172.105.55.115",
        "latitude": 19.0748,
        "longitude": 72.8856
    },
]

REPLICA_IPS = ["50.116.41.109", "45.33.50.187", "194.195.121.150", "172.104.144.157", "172.104.110.211",
               "88.80.186.80", "172.105.55.115"]


#
# def calculate_dis(lat, lon, replica):
#     replica_lat = replica['latitude']
#     replica_lon = replica['longitude']
#
#     return math.pow(lat - replica_lat, 2) + math.pow(lon - replica_lon, 2)
#
#
# def get_geo_nearest_ip(source_ip):
#     try:
#         command = 'curl -u "707935:MJTXPGwfhnZh5PmK" "https://geolite.info/geoip/v2.1/city/{}?pretty"'.format(source_ip)
#         geo = json.loads(os.popen(command).read())
#         lat = geo['location']['latitude']
#         lon = geo['location']['longitude']
#
#         min_dis = calculate_dis(lat, lon, REPLICA_INFO[0])
#         min_replica = REPLICA_INFO[0]
#
#         for i in range(1, len(REPLICA_INFO)):
#             current_dis = calculate_dis(lat, lon, REPLICA_INFO[i])
#
#             if current_dis < min_dis:
#                 min_dis = current_dis
#                 min_replica = REPLICA_INFO[i]
#
#         return min_replica['ip']
#
#     except:
#         return REPLICA_INFO[0]['ip']

def get_geoLocation(ip):
    try:
        url = ('https://geolite.info/geoip/v2.1/city/' + ip + '?pretty')
        response = requests.get(url, auth=('708079', 'xYVsrhhTQiHs9b0M')).content.decode()
        json_str = json.loads(response)
        latitude = json_str['location']['latitude']
        longitude = json_str['location']['longitude']
        return float(latitude), float(longitude)
    except:
        return None, None


def get_geo_distance(lat1, lon1, lat2, lon2):
    """
    It takes the latitude and longitude of two points on the Earth, and returns the distance between
    them in kilometers

    :param lat1: latitude of the first point
    :param lon1: longitude of the first point
    :param lat2: latitude of the second point
    :param lon2: longitude of the second point
    :return: The distance between two points on the earth.
    """
    # R = 6373.0  # rad of earth
    # lat1 = math.radians(lat1)
    # lon1 = math.radians(lon1)
    # lat2 = math.radians(lat2)
    # lon2 = math.radians(lon2)
    # dlat = lat2 - lat1
    # dlon = lon2 - lon1
    # # Haversine formula
    # a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = abs(lon1 - lon2)
    if r > 180:
        r = 360 - r

    return math.pow(lat1 - lat2, 2) + math.pow(r, 2)


def get_nearest_ip(source_ip):
    """
    Given a source IP address, find the nearest CDN server by calculating the distance between the
    source IP address and the CDN server

    :param source_ip: The IP address of the client requesting the content
    :return: The IP address of the nearest CDN
    """
    latitude, longitude = get_geoLocation(source_ip)
    if latitude is None or longitude is None:
        return REPLICA_INFO[0]['ip']
    best_dist = -1
    best_cdn = None
    for c in REPLICA_INFO:
        dist = get_geo_distance(latitude, longitude, c['latitude'], c['longitude'])
        if best_cdn is None:
            best_dist = dist
            best_cdn = c['ip']
            continue
        if best_dist > dist:
            best_dist = dist
            best_cdn = c['ip']
    return best_cdn


def get_rtt(str):
    left = str.find("time=")
    right = str.find(" ms")

    rtt = str[left + 5: right]
    return float(rtt)


def get_fastest_ip(source_ip):
    best_rtt = -1
    best_ip = None
    for replica in REPLICA_INFO:
        try:
            host = replica["host"]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, 12345))
            sock.send(source_ip.encode())
            data = sock.recv(1024).decode()
            sock.close()

            if data == "error":
                continue

            rtt = get_rtt(data)

            if best_ip is None:
                best_rtt = rtt
                best_ip = replica["ip"]
            else:
                if best_rtt > rtt:
                    best_rtt = rtt
                    best_ip = replica["ip"]
        except:
            print("XXXXX")
            continue

    if best_ip is None:
        return REPLICA_INFO[0]["ip"]
    else:
        return best_ip

    # min_time = -1
    # min_ip = None
    #
    # file = open("result.txt", "w")
    #
    # for ip in REPLICA_IPS:
    #     try:
    #         command = "scamper -c 'ping -c 1 -i 1' -i {} | awk 'NR==2 {}'|cut -d '=' -f 2".format(ip, "{print $7}")
    #         result = os.popen(command).read()
    #         file.write(result)
    #
    #         time = float(result)
    #
    #         if min_time == -1:
    #             min_time = time
    #             min_ip = ip
    #         else:
    #             if time < min_time:
    #                 min_time = time
    #                 min_ip = ip
    #     except:
    #         continue
    #
    # if min_ip is None:
    #     file.write("fail")
    #     file.close()
    #     return REPLICA_IPS[0]
    # else:
    #     file.close()
    #     return min_ip


def active_measurement(source_ip):
    best_rtt = -1
    best_ip = None

    for replica in REPLICA_INFO:
        host = replica['host']

        try:
            url = "http://{}:40004/li_huang/{}".format(host, source_ip)
            req = urllib.request.urlopen(url)
            data = req.read().decode()

            rtt = get_rtt(data)

            if best_ip is None:
                best_rtt = rtt
                best_ip = replica["ip"]
            else:
                if best_rtt > rtt:
                    best_rtt = rtt
                    best_ip = replica["ip"]
        except:
            print("XXXXX")
            continue

    if best_ip is None:
        return REPLICA_INFO[0]["ip"]
    else:
        return best_ip




def get_best_cdn(source_ip):
    # ip = get_fastest_ip(source_ip)
    ip = get_nearest_ip(source_ip)

    # if source_ip == "13.234.54.32":
    #     return "172.105.55.115"

    return ip
