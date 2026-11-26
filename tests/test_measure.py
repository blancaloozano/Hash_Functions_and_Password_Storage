import unittest
from sha256 import sha256
from measure import avalanche, truncate, find_collision


class TestMeasure(unittest.TestCase):

    def test_avalanche(self):

        results = avalanche(100, 32, 20357)

        self.assertEqual(len(results), 100)

        for value in results:
            self.assertTrue(0 <= value <= 256)

        # Check reproducibility
        self.assertEqual(
            results,
            avalanche(100, 32, 20357)
        )

    def test_truncate(self):

        digest = sha256(b"abc")

        self.assertEqual(truncate(digest, 16), 0xba78)
        self.assertEqual(truncate(digest, 20), 0xba781)
        self.assertEqual(truncate(digest, 24), 0xba7816)
        self.assertEqual(truncate(digest, 28), 0xba7816b)
        self.assertEqual(truncate(digest, 32), 0xba7816bf)
        self.assertEqual(truncate(digest, 36), 0xba7816bf8)

    def test_find_collision(self):

        for nbits in [16, 20]:

            with self.subTest(nbits=nbits):

                first, second, hashes = find_collision(nbits)

                self.assertNotEqual(first, second)

                first_hash = truncate(
                    sha256(first.encode("ascii")), nbits
                )

                second_hash = truncate(
                    sha256(second.encode("ascii")), nbits
                )

                self.assertEqual(first_hash, second_hash)
                self.assertEqual(hashes, int(second) + 1)


if __name__ == "__main__":
    unittest.main()