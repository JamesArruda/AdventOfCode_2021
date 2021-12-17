from advent2021.helpers.BITS import (
    get_version_sum, process_packet,
    solve_packet
)


def solve_day_16(input: str) -> tuple[int, int]:
    packets = process_packet(input)
    ans_1 = get_version_sum(packets)
    ans_2 = solve_packet(packets)
    return ans_1, ans_2