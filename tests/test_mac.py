import unittest

from mac import naive_mac, naive_verify
from forge import forge


class TestC1Forgery(unittest.TestCase):

    def test_forgery_verifies_with_chosen_key(self):
        # We choose our own key here only to check that forge() produces
        # something naive_verify accepts; the attack itself never uses
        # the key value, only its length, so this validates the method.
        key = b"0123456789abcdef12"[:18]  # 18 bytes, same length as C1
        msg = b"user=student&role=guest&expires=2026-12-31"
        tag = naive_mac(key, msg)

        ext_msg, forged_tag = forge(msg, tag, len(key), b"&role=admin")

        self.assertTrue(naive_verify(key, ext_msg, forged_tag))
        self.assertTrue(ext_msg.endswith(b"&role=admin"))
        self.assertNotEqual(ext_msg, msg)

    def test_forged_message_contains_glue_padding(self):
        key = b"a" * 18
        msg = b"hello"
        tag = naive_mac(key, msg)

        ext_msg, _ = forge(msg, tag, len(key), b"world")

        # The server's own padding byte (0x80) must appear right after
        # the original message, inside the glue.
        self.assertEqual(ext_msg[len(msg)], 0x80)


class TestC2Hmac(unittest.TestCase):

    def test_rfc4231_vectors(self):
        from mac import hmac_sha256

        vectors = [
            (bytes.fromhex("0b" * 20), b"Hi There",
             "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"),
            (b"Jefe", b"what do ya want for nothing?",
             "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"),
            (b"secret", b"user=student&role=guest",
             "b4d022e95ee9053940f3514268c414bbc5571d891a3430487fc2e59a07e8039c"),
        ]
        for key, msg, expected in vectors:
            self.assertEqual(hmac_sha256(key, msg).hex(), expected)

    def test_length_extension_fails_against_hmac(self):
        from mac import hmac_sha256

        key = b"a" * 18
        msg = b"user=student&role=guest"
        tag = hmac_sha256(key, msg)

        # Reuse the same forge() logic that broke naive_mac.
        ext_msg, forged_tag = forge(msg, tag, len(key), b"&role=admin")

        def hmac_verify(key, msg, tag):
            import hmac as hmac_module
            return hmac_module.compare_digest(hmac_sha256(key, msg), tag)

        self.assertFalse(hmac_verify(key, ext_msg, forged_tag))


if __name__ == "__main__":
    unittest.main()