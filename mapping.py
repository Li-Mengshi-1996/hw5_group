from cdn_info import MAPS

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
def get_nearest_cdn(source_ip):
    return MAPS[0]['ip']
