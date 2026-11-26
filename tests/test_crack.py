
import hashlib
import unittest

from crack import crack_unsalted, make_dictionary, salted_hash


class TestPasswordStorage(unittest.TestCase):

    def test_crack_unsalted(self):

        dictionary = ["hello", "world", "example"]
        digest = hashlib.sha256(b"hello").hexdigest()

        recovered = crack_unsalted([digest], dictionary)

        self.assertEqual(recovered, {digest: "hello"})

    def test_password_not_found(self):

        dictionary = ["hello", "world"]
        digest = hashlib.sha256(b"example").hexdigest()

        recovered = crack_unsalted([digest], dictionary)

        self.assertEqual(recovered, {})

    def test_dictionary_size(self):

        dictionary = make_dictionary(n=100)

        self.assertEqual(len(dictionary), 100)

    def test_dictionary_reproducibility(self):

        self.assertEqual(
            make_dictionary(n=100, seed=20357),
            make_dictionary(n=100, seed=20357)
        )

    def test_unsalted_hash(self):

        self.assertEqual(
            salted_hash("123456"),
            "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
        )

    def test_salted_hashes(self):

        salt1 = bytes.fromhex("a3f1c0d94e2b7865")
        salt2 = bytes.fromhex("7b2e4f81cc09a512")

        self.assertEqual(
            salted_hash("123456", salt1),
            "3982dc6b270d4efa6654080c616e7001ee31148d48a44a79129ea1ec47052caa"
        )

        self.assertEqual(
            salted_hash("123456", salt2),
            "4cfd6301e91c2f90dc044561097abc13a1d5a7d9d7c8534cc5538cd65ce7f887"
        )

    def test_different_salts(self):

        password = "123456"

        salt1 = bytes.fromhex("a3f1c0d94e2b7865")
        salt2 = bytes.fromhex("7b2e4f81cc09a512")

        self.assertNotEqual(
            salted_hash(password, salt1),
            salted_hash(password, salt2)
        )


if __name__ == "__main__":
    unittest.main()
