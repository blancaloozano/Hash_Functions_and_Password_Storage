from sha256 import sha256
from hmac import compare_digest

BLOCK_SIZE = 64

# C1: Naive MAC

def naive_mac(key: bytes, msg: bytes) -> bytes:
    return sha256(key + msg)


def naive_verify(key: bytes, msg: bytes, tag: bytes) -> bool:
    return compare_digest(naive_mac(key, msg), tag)

# C2: HMAC-SHA256

def hmac_sha256(key: bytes, msg: bytes) -> bytes:

    if len(key) > BLOCK_SIZE:
        key = sha256(key)
    key = key + b'\x00' * (BLOCK_SIZE - len(key))

    opad = bytes(b ^ 0x5c for b in key)
    ipad = bytes(b ^ 0x36 for b in key)

    inner = sha256(ipad + msg)
    return sha256(opad + inner)

if __name__ == "__main__":

    key = b"secret"
    msg = b"hello"

    tag = naive_mac(key, msg)

    print("C1 - Naive MAC")
    print("Original tag:", tag.hex())
    print("Valid message:", naive_verify(key, msg, tag))
    print("Modified message:", naive_verify(key, b"hello!", tag))

    print()
    print("C2 - HMAC-SHA256")
    hmac_tag = hmac_sha256(key, msg)
    print("HMAC tag:", hmac_tag.hex())