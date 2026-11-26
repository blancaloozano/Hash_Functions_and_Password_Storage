from sha256 import sha256, padding, state_from_digest


# C1: Length-extension attack

def forge(msg: bytes, tag: bytes, keylen: int,
          suffix: bytes) -> tuple[bytes, bytes]:

    # Validate the input
    if keylen < 0:
        raise ValueError("Invalid key length.")

    if len(tag) != 32:
        raise ValueError("Invalid tag length.")

    if not isinstance(msg, (bytes, bytearray)) or not isinstance(suffix, (bytes, bytearray)):
        raise TypeError("msg and suffix must be bytes.")

    glue = padding(keylen + len(msg))

    extended_msg = msg + glue + suffix

    state = state_from_digest(tag)
    already = keylen + len(msg) + len(glue)
    forged_tag = sha256(suffix, state=state, already=already)

    return extended_msg, forged_tag

if __name__ == "__main__":

    # The server challenge given in the handout.
    msg = b"user=student&role=guest&expires=2026-12-31"
    tag = bytes.fromhex(
        "7daa0c342759f55c15bd8acc4a97b17f0adf1dad91e6b862cb0050afbdd92824"
    )
    keylen = 18
    suffix = b"&role=admin"

    extended_msg, forged_tag = forge(msg, tag, keylen, suffix)
    glue_len = len(extended_msg) - len(msg) - len(suffix)

    print("C1 - Length-extension forgery")
    print("Original message:", msg)
    print("Original tag:", tag.hex())
    print("Key length:", keylen)
    print("Glue padding bytes:", glue_len)
    print("Extended message length:", len(extended_msg))
    print("Extended message (hex):", extended_msg.hex())
    print("Forged tag:", forged_tag.hex())