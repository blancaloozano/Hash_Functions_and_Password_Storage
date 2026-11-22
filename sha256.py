
# A1: Padding

def padding(msglen: int) -> bytes:

    if msglen < 0 or msglen >= 2**61:
        raise ValueError("Message length provided is not valid.")

    first_byte = b'\x80'

    zeros = (56 - (msglen + 1) % 64) % 64

    length = (msglen * 8).to_bytes(8, 'big')

    return first_byte + b'\x00' * zeros + length


# A2: Compression function and the full hash

# Adding eight initial state words and sixty-four round constants.
# Defined by FIPS 180-4

# URL: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf

# - page 16, section 4.2.2: The 64 K constants.
# - page 20, section 5.3.3: The 8 initial values of H.

# Initial hash values

H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Round constants

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def compress(state: list[int], block: bytes) -> list[int]:

    if len(block) != 64 or len(state) != 8:
        raise ValueError("Invalid block or state length.")

    # Divide the block --> 16 words of 32 bits
    w = []

    for i in range(0, 64, 4):
        word = int.from_bytes(block[i:i+4], "big")
        w.append(word)

    # Expand 16 words into 64 words
    for i in range(16, 64):
        x = w[i - 15]
        y = w[i - 2]

        s0 = (((x >> 7) | (x << 25)) & 0xffffffff) ^ \
             (((x >> 18) | (x << 14)) & 0xffffffff) ^ (x >> 3)

        s1 = (((y >> 17) | (y << 15)) & 0xffffffff) ^ \
             (((y >> 19) | (y << 13)) & 0xffffffff) ^ (y >> 10)

        word = (w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffff

        w.append(word)

    a, b, c, d, e, f, g, h = state

    # Main compression loop
    for i in range(64):

        s1 = (((e >> 6) | (e << 26)) & 0xffffffff) ^ \
             (((e >> 11) | (e << 21)) & 0xffffffff) ^ \
             (((e >> 25) | (e << 7)) & 0xffffffff)

        ch = (e & f) ^ (~e & g)

        temp1 = (h + s1 + ch + K[i] + w[i]) & 0xffffffff

        s0 = (((a >> 2) | (a << 30)) & 0xffffffff) ^ \
             (((a >> 13) | (a << 19)) & 0xffffffff) ^ \
             (((a >> 22) | (a << 10)) & 0xffffffff)

        maj = (a & b) ^ (a & c) ^ (b & c)

        temp2 = (s0 + maj) & 0xffffffff

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xffffffff


    # Update the hash state
    new_state = [a, b, c, d, e, f, g, h]

    for i in range(8):
        new_state[i] = (state[i] + new_state[i]) & 0xffffffff

    return new_state

# A2 + A3: Full sha256 function

def sha256(data: bytes, state: list[int] = None, already: int = 0) -> bytes:

     # Add padding to the original message considering previously processed bytes
    message = data + padding(already + len(data))

    # Initialize or resume hash state
    if state is None:
        state = H.copy()
    else:
        state = state.copy()

    # Process each 64-byte block
    for i in range(0, len(message), 64):
            block = message[i:i+64]
            state = compress(state, block)

    # Convert the final state into bytes
    digest = b''

    for word in state:
        digest += word.to_bytes(4, 'big')

    return digest


# A3: Resuming from a known state

def state_from_digest(digest: bytes) -> list[int]:

    if len(digest) != 32:
        raise ValueError("Invalid digest length.")

    state = []

    for i in range(0, 32, 4):
        word = int.from_bytes(digest[i:i+4], 'big')
        state.append(word)

    return state

