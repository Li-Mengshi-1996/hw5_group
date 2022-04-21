from cdn_info import MAPS
# from ipaddress import ip_network,ip_address
# import os
import json
import math
import requests

UNKNOWN = 'Unknown'
CDN_MAPPINGS = [
    {
        'hostname':'p5-http-a.5700.network',
        'ip_address':'50.116.41.109',
        'region':'US-Georgia',
        'latitude':'33.798458099365234',
        'longitude':'-84.3882827758789'
    },
    {
        'hostname':'p5-http-b.5700.network',
        'ip_address':'50.117.41.109',
        'region':'Arctic',
        'latitude':'-71.56731',
        'longitude':'-5.46090'
    },
    {
        'hostname':'p5-http-c.5700.network',
        'ip_address':'50.118.41.109',
        'region':'Afreca',
        'latitude':'-24.55842',
        'longitude':'-43.72558'
    },
    {
        'hostname':'p5-http-d.5700.network',
        'ip_address':'50.119.41.109',
        'region':'Australia',
        'latitude':'-6.98804',
        'longitude':'136.92702'
    },
    {
        'hostname':'p5-http-e.5700.network',
        'ip_address':'50.120.41.109',
        'region':'China',
        'latitude':'37.73839',
        'longitude':'90.67498'
    }
]

def get_geoLocation(ip):
    """
    It takes an IP address as input, and returns the latitude and longitude of the IP address
    
    :param ip: The IP address of the source
    :return: The latitude and longitude of the IP address.
    """
    # source_ip2=str.encode(ip)
    # Method1: Use Python requests
    try:
        url = ('https://geolite.info/geoip/v2.1/city/'+ip+'?pretty')
        response = requests.get(url, auth=('708079', 'xYVsrhhTQiHs9b0M')).content.decode()
        json_str = json.loads(response)
        latitude = json_str['location']['latitude']
        longitude = json_str['location']['longitude']
        return float(latitude), float(longitude)
    except:
        return None, None
    
    # Method2: Use os.popen + curl
    # try:
    #     output_stream=os.popen('curl -u "708079:xYVsrhhTQiHs9b0M" "https://geolite.info/geoip/v2.1/city/'+ip+'?pretty"')
    #     json_str=json.loads(output_stream.read().strip())
    #     # print (json_str)
    #     output_stream.close()
    #     latitude= (json_str['location']['latitude'])
    #     longitude=(json_str['location']['longitude'])
    #     return float(latitude), float(longitude)
    # except:
    #     return None, None

def get_geo_distance(lat1,lon1,lat2,lon2):
    """
    It takes the latitude and longitude of two points on the Earth, and returns the distance between
    them in kilometers
    
    :param lat1: latitude of the first point
    :param lon1: longitude of the first point
    :param lat2: latitude of the second point
    :param lon2: longitude of the second point
    :return: The distance between two points on the earth.
    """
    R = 6373.0  # rad of earth
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    print (R * c)
    return (R * c)

def get_geo_distance2(lat1,lon1,lat2,lon2):
    return ((lat2-lat1)*(lat2-lat1))+((lon2-lon1)*(lon2-lon1))

def get_nearest_ip(source_ip):
    """
    Given a source IP address, find the nearest CDN server by calculating the distance between the
    source IP address and the CDN server

    :param source_ip: The IP address of the client requesting the content
    :return: The IP address of the nearest CDN
    """
    latitude, longitude = get_geoLocation(source_ip)
    if latitude is None or longitude is None:
        return CDN_MAPPINGS[0]['ip_address']
    best_dist = 99999
    best_cdn = None
    for c in CDN_MAPPINGS:
        dist = get_geo_distance(latitude, longitude, float(c['latitude']), float(c['longitude']))
        if best_dist > dist:
            best_dist = dist
            best_cdn = c['ip_address']
    return best_cdn


def get_fastest_ip(source_ip):
    min_time = -1
    min_ip = None

    file = open("result.txt", "w")

    for ip in CDN_MAPPINGS:
        try:
            command = "scamper -c 'ping -c 1 -i 1' -i {} | awk 'NR==2 {}'|cut -d '=' -f 2".format(ip, "{print $7}")
            result = os.popen(command).read()
            file.write(result)

            time = float(result)

            if min_time == -1:
                min_time = time
                min_ip = ip
            else:
                if time < min_time:
                    min_time = time
                    min_ip = ip
        except:
            continue

    if min_ip is None:
        file.write("fail")
        file.close()
        return CDN_MAPPINGS[0]
    else:
        file.close()
        return min_ip


def get_best_cdn(source_ip):
    # ip = get_fastest_ip(source_ip)
    ip = get_nearest_ip(source_ip)

    return ip

get_best_cdn("52.62.170.156")