
import hashlib
import random
import unittest
from sha256 import padding, sha256, state_from_digest

class TestSHA256(unittest.TestCase):

    def test_padding(self):
        cases = {
            0: (64, 1, "0000000000000000"),
            3: (61, 1, "0000000000000018"),
            55: (9, 1, "00000000000001b8"),
            56: (72, 2, "00000000000001c0"),
            63: (65, 2, "00000000000001f8"),
            64: (64, 2, "0000000000000200"),
            119: (9, 2, "00000000000003b8"),
            1000: (24, 16, "0000000000001f40")
        }

        for n, (pad_length, blocks, last_eight) in cases.items():
            with self.subTest(length=n):
                p = padding(n)
                self.assertEqual(len(p), pad_length)
                self.assertEqual((n + len(p)) // 64, blocks)
                self.assertEqual(p[-8:].hex(), last_eight)

    def test_published_vectors(self):
        cases = {
            b"": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            b"abc": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            b"cryptography": "e06554818e902b4ba339f066967c0000da3fcda4fd7eb4ef89c124fa78bda419",
            b"Cryptography": "b584eec728548aced5a66c0267dd520a00871b5e7b735b2d8202f86719f61857"
        }

        for msg, expected in cases.items():
            with self.subTest(message=msg):
                self.assertEqual(sha256(msg).hex(), expected)

    def test_random_messages(self):
        rng = random.Random(12345)

        lengths = [55, 56, 63, 64, 65, 119, 120, 127, 128, 129]
        lengths += [rng.randint(0, 2000) for _ in range(100)]

        for n in lengths:
            msg = rng.randbytes(n)
            with self.subTest(length=n):
                self.assertEqual(
                    sha256(msg),
                    hashlib.sha256(msg).digest()
                )

    def test_resume(self):
        base = b"the first part"
        suffix = b"and the rest"

        digest = sha256(base)
        state = state_from_digest(digest)

        self.assertEqual(
            digest.hex(),
            "d2bba6892bc661a48fd99f726bdf084a4e53e9644d03f06002eb2c1d11ac194d"
        )

        resumed = sha256(suffix, state=state, already=64)
        full = sha256(base + padding(len(base)) + suffix)

        self.assertEqual(resumed, full)
        self.assertEqual(
            resumed.hex(),
            "cb32e653bcd5ed0800832787b264fab57a61f652a391177224fa3cbb1aab740d"
        )


if __name__ == "__main__":
    unittest.main()
