import json

import jsonschema
from scapy.all import *
from scapy.layers.http import *
import io
from scapy.layers.inet import UDP, IP

with open(r'C:\Users\s9292756\Desktop\schema.json', 'r') as f:
    schema = json.load(f)
    validator = jsonschema.Draft4Validator(schema)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    n_data = []
    for i in range(len(data)):
        n_data.append(data[i] ^ key[i % len(key)])
    return bytes(n_data)


ex_start = datetime(2024, 5, 24 , 8 , 00, 00)
ex_end = None
# ex_end = datetime(2024, 5, 23, 10, 00, 00)
key = b'MEgCQQDQ8zr1m159eoVQoR6J9ooKzJapk6xyj7F/lI5Er4hPYJBbhtE+RnqwFmJg7Tn4GQJtnZa1I3qjmXA/2sVSPHU7AgMBAAE='
# key = b'WeLoveMaof'
delta = 35  # in minutes
mmaps_delta = 120
file_path = r"C:\Users\s9292756\Desktop\24052024.pcap"

with open(file_path, 'rb') as f:
    pcap_bytes = f.read()

pcap_flow = rdpcap(io.BytesIO(pcap_bytes))

# with open(file_path, 'rb') as f:
# file_str = f.read().decode('utf-8')

on_off_counter = 0

decoded_messages = []
message_counter = 0
bad_messages_counter = 0
gps_error_counter = 0
bad_reports = []
for p in pcap_flow:
    if datetime.fromtimestamp(int(p.time)) < ex_start:
        continue
    if ex_end is not None:
        if datetime.fromtimestamp(int(p.time)) > ex_end:
            continue
    message_counter += 1
    try:
        decoded_data = xor_bytes(p[UDP].payload.raw_packet_cache, key)
    except:
        print(p.raw_packet_cache)
        continue
    try:
        # print(decoded_data)
        decoded_text = str(decoded_data, 'utf-8')
        decoded_text = decoded_text.replace("\r\n", "")
        json_data = json.loads(decoded_text)
        try:
            if json_data['Log'].startswith("240521"):
                with open(r'./all_jsons/' + str(message_counter) + '.json', 'w') as f:
                    # json_data['lon'] = float(json_data['lon'] )
                    # json_data['lat'] = float(json_data['lat'])
                    # json_data['alt'] = float(json_data['lon'])
                    # json_data['spd'] = float(json_data['spd'])
                    # json_data['snm'] = int(json_data['snm'])
                    json.dump(json_data, f)
            # pass
        except Exception as e:
            if json_data['Log'].startswith("240521"):
                with open(r'./bad_jsons/' + str(message_counter) + '.json', 'w') as f:
                    # json_data['lon'] = float(json_data['lon'] )
                    # json_data['lat'] = float(json_data['lat'])
                    # json_data['alt'] = float(json_data['lon'])
                    # json_data['spd'] = float(json_data['spd'])
                    # json_data['snm'] = int(json_data['snm'])
                    json.dump(json_data, f)
        if 'state' in json_data:
            on_off_counter += 1
            # print(json_data)
            continue
        if json_data['lat'] == 'error' or json_data['lon'] == 'error' or json_data['alt'] == 'error' or json_data[
            'snm'] == 'error':
            gps_error_counter += 1
        json_data['created_at'] = datetime.fromtimestamp(int(p.time))
        decoded_messages.append(json_data)
        # print(json_data)
    except Exception as e:
        bad_messages_counter += 1
        print(e)
        print("packet number: " + str(message_counter + 1))
        print("time: " + str(datetime.fromtimestamp(int(p.time))))
        print("encoded: ")
        print(p[UDP].payload.raw_packet_cache)
        print("decoded: ")
        print(decoded_data)
        bad_reports.append(p[UDP].payload.raw_packet_cache)
        # print("packet number: " + str(message_counter))
        # print(i)
        # print(p[IP].src)
        continue
