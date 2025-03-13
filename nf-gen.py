#
# NetFlow v5 generator
#
import socket
import struct
import random
import time
from ipaddress import IPv4Address

# Format:
# https://www.cisco.com/c/en/us/td/docs/net_mgmt/netflow_collection_engine/3-6/user/guide/format.html
# 

def generate_random_ip():
    return str(IPv4Address(random.randint(167772160, 184549375)))  # 10.0.0.0/8

"""
    •   '!': This specifies the byte order, alignment, and size. The ! indicates network byte order (big-endian), which is commonly used in network protocols.
    •   'H': Represents an unsigned short (2 bytes). There are two H characters, indicating that two unsigned short integers will be packed.
    •   'I': Represents an unsigned int (4 bytes). There are five I characters, indicating that five unsigned integer values will be packed.
    •   'B': Represents an unsigned char (1 byte). There are two B characters, indicating that two unsigned byte values will be packed.
"""
def create_netflow_header():
    return struct.pack('!HHIIIIBBH',
        5,      # version                                    
        1,      # number of flows, count                                  
        int((time.time() * 1000) % 4294967295),# sys_uptime
        int(time.time() % 4294967295),         # unix_secs
        0,                                     # unix_nsecs
        random.randint(0, 65535),              # flow_sequence
        1,                                     # engine_type
        2,                                     # engine_id
        24                                     # sampling_interval 
    )


def create_flow_record(j,i):
    return struct.pack('!4s4s4sHHIIIIHHBBBBHHBBBB',    
        socket.inet_aton("10.5.1.1"),              # src_addr, 4s
        socket.inet_aton("10.6."+str(j)+"."+str(i)),        # dst_addr, 4s 
        socket.inet_aton('0.0.0.0'),               # next_hop, 4s
        random.randint(0, 65535),                  # input_if, H
        random.randint(0, 65535),                  # output_if, H
        random.randint(1, 1000),                   # packets, I
        random.randint(64, 150000),                # octets, I
        int(time.time() * 1000) % 4294967295,      # first, I
        (int(time.time() * 1000) + 1000) % 4294967295,  # last, I
        random.randint(1024, 65535),               # src_port, H
        #random.randint(1, 65535),                 # dst_port, H
        443,                                       # dst_port, H  
        0,                                         # pad1 Unused (zero) bytes 1 BYTE, B
        0,                                         # tcp_flags, B
        6,                                         # protocol (TCP), B
        0,                                         # tos, B
        0,                                         # src_as, H
        0,                                         # dst_as, H
        24,                                        # src_mask, B
        24,                                        # dst_mask, B
        0,                                         # pad2a (zero), B
        0                                          # pad2b (zero), B
    )

def main():
    # Define the server IP and the port
    collector_ip = 'fc.company.com'  # Flow Collector
    collector_port = 2055
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for j in range(250):
        for i in range(250):
            packet = create_netflow_header() + create_flow_record(j,i)
            sock.sendto(packet, (collector_ip, collector_port))
            time.sleep(0.03)
    
    sock.close()

if __name__ == '__main__':
    main()