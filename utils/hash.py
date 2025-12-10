def uint32(value: int) -> int:
    return value & 0xFFFFFFFF

def arshift(value: int, bits: int) -> int:
    value = uint32(value)
    if value & 0x80000000:
        value = value - 0x100000000
    return value >> bits

def mix(a: int, b: int, c: int) -> tuple[int, int, int]:
    a = uint32(a - b)
    a = uint32(a - c)
    a = uint32(a ^ arshift(c, 13))
    b = uint32(b - c)
    b = uint32(b - a)
    b = uint32(b ^ uint32(a << 8))
    c = uint32(c - a)
    c = uint32(c - b)
    c = uint32(c ^ arshift(b, 13))
    a = uint32(a - b)
    a = uint32(a - c)
    a = uint32(a ^ arshift(c, 12))
    b = uint32(b - c)
    b = uint32(b - a)
    b = uint32(b ^ uint32(a << 16))
    c = uint32(c - a)
    c = uint32(c - b)
    c = uint32(c ^ arshift(b, 5))
    a = uint32(a - b)
    a = uint32(a - c)
    a = uint32(a ^ arshift(c, 3))
    b = uint32(b - c)
    b = uint32(b - a)
    b = uint32(b ^ uint32(a << 10))
    c = uint32(c - a)
    c = uint32(c - b)
    c = uint32(c ^ arshift(b, 15))
    return a, b, c

def word(code_units: list[int], offset: int) -> int:
    return uint32(
        code_units[offset]
        + (code_units[offset + 1] << 8)
        + (code_units[offset + 2] << 16)
        + (code_units[offset + 3] << 24)
    )

def hashInt32(string: str) -> int:
    """ Jenkin 32-bit hash implementation present in Playfish's AS3 implementation """
    
    if string is None:
        string = ""
    elif not isinstance(string, str):
        string = str(string)

    encoded = string.encode("utf-16-le", "surrogatepass")
    code_units = [encoded[i] | (encoded[i + 1] << 8) for i in range(0, len(encoded), 2)]

    length = len(code_units)
    idx = 0
    a = b = 0x9E3779B9
    c = uint32(0)

    while length - idx >= 12:
        a = uint32(a + word(code_units, idx))
        b = uint32(b + word(code_units, idx + 4))
        c = uint32(c + word(code_units, idx + 8))
        a, b, c = mix(a, b, c)
        idx += 12

    c = uint32(c + 1)
    remaining = length - idx

    if remaining >= 11:
        c = uint32(c + (code_units[idx + 10] << 24))
    if remaining >= 10:
        c = uint32(c + (code_units[idx + 9] << 16))
    if remaining >= 9:
        c = uint32(c + (code_units[idx + 8] << 8))
    if remaining >= 8:
        b = uint32(b + (code_units[idx + 7] << 24))
    if remaining >= 7:
        b = uint32(b + (code_units[idx + 6] << 16))
    if remaining >= 6:
        b = uint32(b + (code_units[idx + 5] << 8))
    if remaining >= 5:
        b = uint32(b + code_units[idx + 4])
    if remaining >= 4:
        a = uint32(a + (code_units[idx + 3] << 24))
    if remaining >= 3:
        a = uint32(a + (code_units[idx + 2] << 16))
    if remaining >= 2:
        a = uint32(a + (code_units[idx + 1] << 8))
    if remaining >= 1:
        a = uint32(a + code_units[idx])

    a, b, c = mix(a, b, c)
    return uint32(c)