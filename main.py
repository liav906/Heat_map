import json
from scapy.all import *
from scapy.layers.http import *
import io

from scapy.layers.inet import UDP, IP


def xor_bytes(data: bytes, key: bytes) -> bytes:
    n_data = []
    for i in range(len(data)):
        n_data.append(data[i] ^ key[i % len(key)])
    return bytes(n_data)


file_path = r"C:\Users\s8438605\Desktop\udpsnif.pcap"
with open(file_path, 'rb') as f:
    pcap_bytes = f.read()

pcap_flow = rdpcap(io.BytesIO(pcap_bytes))

#key = b'stam'
key = b'WeLoveMaof'
l = []
message_counter = 0
bad_messages_counter = 0
gps_error_counter=0
for p in pcap_flow:
    message_counter += 1
    decoded_data = xor_bytes(p[UDP].payload.raw_packet_cache, key)
    l.append(len(decoded_data))
    try:
        # print(decoded_data)
        decoded_text = str(decoded_data, 'utf-8')
        json_data = json.loads(decoded_text)
        if json_data['lat'] == 'error' or json_data['lon'] == 'error' or json_data['alt'] == 'error' or json_data['snm'] == 'error':
            gps_error_counter +=1
        # print(json_data['uptime'])
    except Exception as e:
        bad_messages_counter += 1
        print(p[UDP].payload.raw_packet_cache)
        print("packet number: " + str(message_counter))
        # print(i)
        # print(p[IP].src)
        continue

print("number of not json messages: " + str(bad_messages_counter))
print("number of messages with gps error: " + str(gps_error_counter))
# print(f"max: {max(l)}")
