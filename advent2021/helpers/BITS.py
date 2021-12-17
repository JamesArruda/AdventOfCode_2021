from typing import Callable, Union, Iterable, List
PacketBase = tuple[int, int, Union[Iterable['PacketBase'], int]]
Packet = List[PacketBase]

def _decode(hex_pack: str) -> str:
    """Turn a hexadecimal string into a binary string,
    padded for 4 bits per hex.
    """
    bin_pack_raw = bin(int(hex_pack,16))[2:]
    bin_pack = bin_pack_raw.zfill(4*len(hex_pack))
    return bin_pack


def _get_packet_func(pack_type: int) -> Callable[[str], tuple[Packet, Union[str, Packet]]]:
    # TODO: If AoC2021 gets more complicated, we have
    # flexibility here
    return _literal if pack_type == 4 else _operator


def _packet(pack: str) -> Packet:
    version = int(pack[:3], 2)
    pack_type = int(pack[3:6], 2)
    rest = pack[6:]
    the_packets = [[version, pack_type, None], ]
    pack_data, rem = _get_packet_func(pack_type)(rest)
    the_packets[-1][-1] = pack_data
    # if there is remaining, it is at the same level
    if isinstance(rem, list) and rem:
        the_packets.extend(rem)
    elif rem and not int(rem, 2) == 0:
        the_packets.extend(_packet(rem))
    return [tuple(x) for x in the_packets]


def _literal(pack: str) -> tuple[int, str]:
    num = ""
    for i in range(0,len(pack)+10,5):
        num += pack[i+1:i+5]
        if pack[i] == '0':
            return int(num, 2), pack[i+5:]


def _operator(pack: str) -> tuple[int, Union[str, Packet]]:
    len_id = pack[0]
    n_sub = 15 if len_id == '0' else 11
    v = int(pack[1:n_sub + 1], 2)
    if n_sub == 15:
        packets = _packet(pack[n_sub+1:n_sub+1+v])
        return packets, pack[n_sub+1+v:]
    else:
        sub_packs = pack[n_sub+1:]
        packets = _packet(sub_packs)
        return packets[:v], packets[v:]
    
from math import prod
_op_map = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda x: x[0] > x[1],
    6: lambda x: x[0] < x[1],
    7: lambda x: x[0] == x[1],
}

def _packet_op(packets: Packet) -> int:
    # Gather the values for this operator
    # If the value is an operator, get it
    __version__ = packets[0]
    op = packets[1]
    if op == 4:
        return packets[-1]
    values = [_packet_op(p) for p in packets[2]]
    return _op_map[op](values)

# The outward-facting functions
def get_version_sum(packets: Packet) -> int:
    s = 0
    if isinstance(packets, int):
        return s
    s = sum(p[0] for p in packets)
    for p in packets:
        s += get_version_sum(p[-1])
    return s


def process_packet(hex_packet: str) -> Packet:
    bin_packet = _decode(hex_packet)
    return _packet(bin_packet)


def solve_packet(packet: Packet) -> int:
    assert len(packet) == 1, "Packets usually start with 1 operation"
    return _packet_op(packet[0])