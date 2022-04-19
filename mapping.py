from cdn_info import MAPS
from ipaddress import ip_network,ip_address
import os
import json
import math

UNKNOWN = 'Unknown'
CDN_MAPPINGS = [
    {
        'hostname':'p5-http-a.5700.network',
        'ip_address':'50.116.41.109',
        'region':'US-Georgia',
        'latitude':'33.798458099365234',
        'longitude':'-84.3882827758789'
    }
]

def get_geoLocation(ip):
    source_ip2=str.encode(ip)
    try:
        output_stream=os.popen('curl -u "708079:xYVsrhhTQiHs9b0M" "https://geolite.info/geoip/v2.1/city/'+source_ip2+'?pretty"')
        json_str=json.loads(output_stream.read().strip())
        latitude= (json_str['location']['latitude'])
        longitude=(json_str['location']['longitude'])
        return latitude, longitude
    except Exception as e:
        return None, None

def get_geo_distance(lat1,lon1,lat2,lon2):
    R = 6373.0#rad of earth
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    #Haversine formula
    a = math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return R*c
    
def get_nearest_cdn(source_ip):
    latitude,longitude = get_geoLocation(source_ip)
    if latitude is None or longitude is None:
        return CDN_MAPPINGS[0]['ip_address']
    best_dist=None
    best_cdn=None
    for c in CDN_MAPPINGS:
        dist = get_geo_distance(latitude,longitude,c['latitude'],c['longitude'])
        if not best_dist or best_dist > dist:
            best_dist = dist
            best_cdn = c['ip_address']
    return best_cdn

get_nearest_cdn("")
