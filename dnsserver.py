#!/usr/bin/python3
from dnslib import *
from mapping import *
import sys


def build_response(data, addr, domain, cache):
    domain = domain + "."
    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    q_name = str(request.q.qname)
    q_type = QTYPE[request.q.qtype]

    if q_type == 'A' and (q_name == domain or q_name.endswith('.' + domain)):
        if addr[0] not in cache:
            cache[addr[0]] = get_nearest_cdn(addr[0])

        ip = cache[addr[0]]
        reply.add_answer(RR(rname=q_name, rtype=QTYPE.A, ttl=300, rdata=A(ip)))

    return reply.pack()


def receive(sock):
    result = b''
    addr = None
    while True:
        data, addr = sock.recvfrom(1024)
        result += data

        if len(data) == 0:
            break
    return result, addr


def start(sock, domain, cache):
    while True:
        data, address = receive(sock)
        response = build_response(data, address, domain, cache)
        sock.sendto(response, address)


def main():
    port = int(sys.argv[2])
    name = sys.argv[4]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))

    cache = dict()

    try:
        start(sock, name, cache)
    except KeyboardInterrupt:
        sock.close()
        print("Bye")

    # print(args.n)
    # print(args.p)


main()
