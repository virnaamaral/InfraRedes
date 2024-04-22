import struct

header_format = 'I I B B H'
header_size = struct.calcsize(header_format)

def calculate_checksum(data):
    checksum = 0
    for i, byte in enumerate(data):
        checksum += (byte * (i + 1)) % 256
    return checksum % 256

def pack_header(seq_num, ack_num, flags, checksum, payload_len):
    return struct.pack(header_format, seq_num, ack_num, flags, checksum, payload_len)

def unpack_header(header_bytes):
    return struct.unpack(header_format, header_bytes)
