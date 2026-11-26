import random
import hashlib
import time

# Common passwords from the reference code

TOP = [
    "123456", "password", "123456789", "qwerty",
    "abc123", "letmein", "monkey", "dragon",
    "football", "iloveyou", "admin", "welcome",
    "sunshine", "princess", "baseball", "shadow",
    "master", "trustno1"
]

# Generate a reproducible password dictionary

def make_dictionary(n: int = 200_000,
                    seed: int = 20357) -> list[str]:

    rng = random.Random(seed)
    words = TOP.copy()
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Generate additional password candidates
    while len(words) < n:

        length = rng.randint(5, 8)

        password = "".join(
            rng.choice(alphabet) for _ in range(length)
        )

        words.append(password)

    return words[:n]


# D1: Cracking unsalted password hashes

def crack_unsalted(hashes: list[str], dictionary: list[str]) -> dict[str, str]:

    # Build a lookup table of hashes and passwords
    table = {}

    for password in dictionary:
        digest = hashlib.sha256(password.encode()).hexdigest()
        table[digest] = password

    # Recover passwords by matching the target hashes
    recovered = {}

    for digest in hashes:
        if digest in table:
            recovered[digest] = table[digest]

    return recovered

# Compute a password hash with an optional salt

def salted_hash(password: str, salt: bytes = b"") -> str:

    return hashlib.sha256(salt + password.encode()).hexdigest()



if __name__ == "__main__":

    # Generate the dictionary
    dictionary = make_dictionary()

    # Controlled test hashes
    test_passwords = [
        "123456", "password", "123456789", "qwerty",
        "abc123", "letmein", "monkey", "dragon"
    ]

    hashes = [
        hashlib.sha256(password.encode()).hexdigest()
        for password in test_passwords
    ]

    # Measure the execution time
    start = time.perf_counter()

    recovered = crack_unsalted(hashes, dictionary)

    elapsed = time.perf_counter() - start

    # Display results
    print("D1 - Cracking unsalted password hashes")
    print()

    print("Dictionary size:", len(dictionary))
    print("Hashes computed:", len(dictionary))
    print("Passwords recovered:", len(recovered), "/", len(hashes))
    print(f"Execution time: {elapsed:.6f} seconds")

    print()
    print("Recovered passwords:")

    for digest in hashes:
        print(digest, "->", recovered.get(digest, "Not found"))

    
    # Password storage with and without salt

    password = "123456"

    salt1 = bytes.fromhex("a3f1c0d94e2b7865")
    salt2 = bytes.fromhex("7b2e4f81cc09a512")

    unsalted = salted_hash(password)
    salted1 = salted_hash(password, salt1)
    salted2 = salted_hash(password, salt2)

    print()
    print("D1 - Password storage and salting")
    print()

    print("Password:", password)
    print("Unsalted hash:", unsalted)
    print()

    print("Salt 1:", salt1.hex())
    print("Salted hash 1:", salted1)
    print()

    print("Salt 2:", salt2.hex())
    print("Salted hash 2:", salted2)

    # Compare the computational cost

    users = 500
    unsalted_cost = len(dictionary)
    salted_cost = users * len(dictionary)

    print()
    print("D1 - Computational cost")
    print()

    print("Number of users:", users)
    print("Unsalted hashes required:", unsalted_cost)
    print("Salted hashes required:", salted_cost)
    print("Cost multiplier:", salted_cost // unsalted_cost)

