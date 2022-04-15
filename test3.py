from dnslib import *

def build_response(data):
    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id,
                                qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    q_type = request.q.qtype
    qt = QTYPE[q_type]

    print(qn)
    return

    # if qt == 'A':
    #     if qn == domain or qn.endswith('.' + domain):
    #         if addr[0] not in cache:
    #             cache[addr[0]] = get_nearest_cdn(addr[0])
    #         ip = cache[addr[0]]
    #         reply.add_answer(RR(rname=qname, rtype=QTYPE.A, rclass=1, ttl=300, rdata=A(ip)))
    #
    # return reply.pack()

# packet = binascii.unhexlify(b'd5ad818000010005000000000377777706676f6f676c6503636f6d0000010001c00c0005000100000005000803777777016cc010c02c0001000100000005000442f95b68c02c0001000100000005000442f95b63c02c0001000100000005000442f95b67c02c0001000100000005000442f95b93')
#
# build_response(packet)

# print('"')
# import sys
#
# test=[1,2,3,4,5,6]
#
# print(sys.getsizeof(test))
f = open("pageviews.csv")

lines = f.readlines()

for line in lines:
    print(line)
    break

