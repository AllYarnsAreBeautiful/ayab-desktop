from pathlib import Path


WIDTH = 3
HEIGHT = 2
PATTERN = bytes((0, 1, 0, 0x83, 1))
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def set_word(data: bytearray, offset: int, value: int) -> None:
    data[offset : offset + 2] = value.to_bytes(2, "little")


def pascal_string(data: bytes, offset: int) -> bytes:
    size = data[offset]
    return data[offset + 1 : offset + size + 1]


def stp_xor_key(data: bytes) -> bytearray:
    def word(offset: int) -> int:
        return int.from_bytes(data[offset : offset + 2], "little")

    def dword(offset: int) -> int:
        return int.from_bytes(data[offset : offset + 4], "little")

    def append(current: bytes, value: bytes, max_size: int) -> bytes:
        return (current + value)[:max_size]

    key1 = dword(0x35) >> 1
    key1 += word(0x3F) << 2
    key1 += dword(0x39)
    key1 += word(0x3D)
    key1 += data[0x20]
    salt1 = word(0x39)
    salt2 = int((dword(0x35) & 0xFFFF) > 0)
    key_string = pascal_string(data, 0x60)
    key_string = append(key_string, pascal_string(data, 0x41), 0x6E)
    key_string = append(key_string, str(word(0x3D)).encode(), 0x7D)
    key_string = append(key_string, str(data[0x20]).encode(), 0x8C)
    key_string = append(key_string, pascal_string(data, 0x41), 0xAA)
    key_string = append(key_string, str(data[0x20]).encode(), 0xB9)
    key_string = append(key_string, str(word(0x3D)).encode(), 0xC8)

    key2 = key1
    for index, value in enumerate(key_string, start=1):
        half_value = value // 2
        switch = index % 3
        if switch == 0:
            key2 += index * half_value + (salt2 + half_value) // 7
        elif switch == 1:
            key2 += index * salt2
            key2 += half_value * 6
            key2 += half_value // 5 * word(0x3F)
        else:
            key2 += index * salt1
            key2 += half_value * 4

    key_string = str(key2 * 3).encode()
    key_string = append(key_string, str(key2).encode(), 0x1E)
    key_string = append(key_string, str(key2 * 4).encode(), 0x2D)
    key_string = append(key_string, str(key2 * 2).encode(), 0x3C)
    key_string = append(key_string, str(key2 * 5).encode(), 0x4B)
    key_string = append(key_string, str(key2 * 6).encode(), 0x5A)
    key_string = append(key_string, str(key2 * 8).encode(), 0x69)
    key_string = append(key_string, str(key2 * 7).encode(), 0x78)

    xor_key = bytearray(21000)
    for index in range(len(xor_key)):
        key_index = (index + 1) % len(key_string)
        xor_key[index] = key_string[key_index] ^ (key2 % (index + 1) & 0xFF)
    return xor_key


def make_pat() -> bytes:
    data = bytearray(0x165)
    data[0:3] = b"D4C"
    data[3:0x83] = b"\xFF" * 0x80
    data[3] = 0
    data[4] = 1
    data[0x105:0x108] = bytes(reversed(RED))
    data[0x108:0x10B] = bytes(reversed(BLUE))
    set_word(data, 0x13A, WIDTH)
    set_word(data, 0x13C, HEIGHT)
    data.extend(PATTERN)
    data.extend(b"\x00\xFE")
    return bytes(data)


def make_stp() -> bytes:
    data = bytearray(0xF8)
    data[0:3] = b"D7c"
    set_word(data, 3, WIDTH)
    set_word(data, 5, HEIGHT)
    xor_key = stp_xor_key(data)

    data.extend(HEIGHT.to_bytes(2, "little"))
    data.extend(len(PATTERN).to_bytes(2, "little"))
    data.extend(value ^ xor_key[index] for index, value in enumerate(PATTERN))

    data.extend(HEIGHT.to_bytes(2, "little"))
    data.extend(b"\x00\x00")

    colors = bytearray(0x47 * 0x19)
    for index, rgb in enumerate((RED, BLUE)):
        offset = index * 0x19
        colors[offset] = 0x10
        colors[offset + 3] = index
        colors[offset + 6 : offset + 9] = bytes(rgb)
    data.extend(colors)
    return bytes(data)


def make_cut() -> bytes:
    data = bytearray()
    data.extend(WIDTH.to_bytes(2, "little"))
    data.extend(HEIGHT.to_bytes(2, "little"))
    data.extend(b"\x00\x00")
    data.extend(b"\x05\x00\x03\x00\x7F\xFF\x00")
    data.extend(b"\x03\x00\x83\x40\x00")
    return bytes(data)


def main() -> None:
    directory = Path(__file__).parent
    (directory / "synthetic.pat").write_bytes(make_pat())
    (directory / "synthetic.stp").write_bytes(make_stp())
    (directory / "synthetic.cut").write_bytes(make_cut())


if __name__ == "__main__":
    main()
