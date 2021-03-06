#!/usr/bin/env python3
import argparse
from dnslib import *
import logging

BUFFER_SIZE = 4096
TTL = 300
cache = {}


def get_dns_response(data, address, origin_domain):
    request = DNSRecord.parse(data)
    global cache
    reply = DNSRecord(DNSHeader(id=request.header.id,
                                qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]
    if qt in ['*', 'A']:
        if qn == origin_domain or qn.endswith('.' + origin_domain):
            if address[0] not in cache:
                cache[address[0]] = find_best_cdn(address[0])
            ip = cache[address[0]]
            reply.add_answer(RR(rname=qname, rtype=QTYPE.A, rclass=1, ttl=TTL, rdata=A(ip)))

    return reply.pack()


def recv_dns_request(s):
    buffer = b''
    address = None
    while True:
        data, address = s.recvfrom(BUFFER_SIZE)
        buffer += data
        if not data or len(data) < BUFFER_SIZE:
            break
    return buffer, address


def start_dns_server(s, origin_domain):
    while True:
        data, address = recv_dns_request(s)
        response = get_dns_response(data, address, origin_domain)
        s.sendto(response, address)


def main():
    parser = argparse.ArgumentParser(description='Start a DNS Server.')
    parser.add_argument(
        '-p', type=int, help='Port number that DNS server binds to.', required=True, metavar='port')
    parser.add_argument(
        '-n', type=str, help='CDN-specific name.', required=True, metavar='name')
    parser.add_argument('--verbose', '-v', help='Print all debug message from dns server', action='store_true')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', args.p))
    try:
        start_dns_server(s, args.n + '.')
    except KeyboardInterrupt:
        pass
    finally:
        s.close()


if __name__ == '__main__':
    main()
