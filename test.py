def get_flag(flags):
    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])

    r_flags = ''

    QR = '1'

    OPCODE = ''

    for bit in range(1, 5):
        OPCODE += str(ord(byte1) & (1 << bit))

    AA = '1'
    TC = '0'
    RD = '0'

    RA = '0'
    Z = '000'

    RCODE = '0000'

    return int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder='big') + int(RA + Z + RCODE, 2).to_bytes(1,
                                                                                                             byteorder='big')
def get_domain(data):
    state = 0
    expected_length = 0

    domain_string = ''
    domain_parts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            domain_string += chr(byte)
            x += 1
            if x == expected_length:
                domain_parts.append(domain_string)
                domain_string = ''
                state = 0
                x = 0
            if byte == 0:
                domain_parts.append(domain_string)
                break

        else:
            state = 1
            expected_length = byte

        x += 1
        y += 1
    question_type = data[y+1:y+3]

    return domain_parts, question_type


def build_response(data):
    # Get transaction ID
    trans_id = data[:2]
    tid = ''
    for i in trans_id:
        tid += hex(i)[2:]

    # Get the flags
    flags = get_flag(data[2:4])

    # Question count
    QDCOUNT = b'\x00\x01'

    # Answer Count


    return



# ssh -i ~/.ssh/id_ed25519.pub li_huang@cs5700cdnproject.ccs.neu.edu

# dns node
# ssh -i ~/.ssh/id_ed25519.pub li_huang@p5-dns.5700.network

# replica
# ssh -i ~/.ssh/id_ed25519.pub li_huang@p5-http-a.5700.network

# ./deployCDN -p 40004 -o cs5700cdnorigin.ccs.neu.edu -n cs5700cdn.example.com -u li_huang -i ~/.ssh/id_ed25519.pub
# ./runCDN -p 40004 -o cs5700cdnorigin.ccs.neu.edu -n cs5700cdn.example.com -u li_huang -i ~/.ssh/id_ed25519.pub
# ./stopCDN -p 40004 -o cs5700cdnorigin.ccs.neu.edu -n cs5700cdn.example.com -u li_huang -i ~/.ssh/id_ed25519.pub

# ps aux | grep li_huang.*dnsserver | grep -v grep | awk '{ print $2 }'

# ssh mengshi@login.khoury.northeastern.edu
# ssh mengshi@cs5700cdnproject.ccs.neu.edu

# dig @45.33.90.91 -p 40004 cs5700cdn.example.com