# Hash_Functions_and_Password_Storage

This practice forms part of the subject Cryptography for the Bachelor in Data Science and Engineering, CEU San Pablo University 26/27. It focuses on implementing the SHA-256 cryptographic hash function from the FIPS 180-4 specification, measuring its security properties, exploring length-extension attacks against message authentication codes, and studying password storage vulnerabilities.

## 1. How to run everything

The project is implemented in Python 3.11+ and it is organized into independent files, each responsible for a different cryptographic task. All modules are tested from the terminal using the automated test suite.

To run the automated tests:
```bash
python -m unittest discover -s tests
```
To verify the SHA-256 implementation from part A, run:
```bash
python -c "from sha256 import sha256; print(sha256(b'abc').hex())"
```
Expected output:
```bash
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```
To run the avalanche effect and birthday bound experiments
from Part B, install matplotlib and run:

```bash
python -m pip install matplotlib
python measure.py
```

The program displays the experimental measurements,
calculates the fitted slope and saves both plots in
the `images/` directory.

To run the MAC and HMAC implementations from Part C:
```bash
python mac.py
```
To run the length-extension experiment from Part C1:
```bash
python forge.py

```
To run the password storage experiment from Part D:
```bash
python crack.py
```

## 2. A3 - Resuming from a known state

### Question
*State in two lines why the second and third bullets agree, and what that tells you about what a SHA-256 digest reveals.*

### Explanation
Both results agree because the SHA-256 digest contains the internal state after processing the original message and its padding, allowing the algorithm to continue from that state. 

This means that knowing a SHA-256 digest and the original message length makes it possible to extend the hashed message without knowing its original contents.

### Verification
Using `base = b"the first part"` and `suffix = b"and the rest"`, the original digest is:
```bash
d2bba6892bc661a48fd99f726bdf084a4e53e9644d03f06002eb2c1d11ac194d
```

Resuming SHA-256 from that digest with `already = 64` produces:
```bash
cb32e653bcd5ed0800832787b264fab57a61f652a391177224fa3cbb1aab740d
```
This matches the result of hashing `base + padding(len(base)) + suffix` directly. 

## 3. B1 - The avalanche effect

### Measurements

The experiment was performed by generating random messages, flipping a single random bit and counting the number of different bits between the original and modified SHA-256 digests.

| Parameter | Value |
|---|---:|
| Number of trials | 2000 |
| Message length | 32 bytes |
| Random seed | 20357 |
| Mean | 128.2795 bits |
| Minimum | 105 bits |
| Maximum | 158 bits |
| Theoretical mean | 128 bits |
| Absolute deviation | 0.2795 bits |

Histogram with 8-bit bins:

![B1 avalanche histogram](images/b1_avalanche_histogram.png)

| Bin | Count |
|---|---:|
| 104-111 | 33 |
| 112-119 | 220 |
| 120-127 | 639 |
| 128-135 | 750 |
| 136-143 | 309 |
| 144-151 | 48 |
| 152-159 | 1 |

### Question
*State the value theory predicts and how far your mean is from it.*

### Explanation

For an ideal 256-bit hash function, changing a single input bit should change each output bit with a probability of 50%. Therefore, the theoretical mean is 256 × 0.5 = 128 bits.

The measured mean is 128.2795 bits, which is only 0.2795 bits above the theoretical value (a relative deviation of 0.2184%). These results are consistent with the expected avalanche effect of SHA-256.

## 4. B2 - The birthday bound

### Measurements

The experiment was performed by truncating SHA-256 to
different output lengths and hashing consecutive decimal
strings until the first collision was found.

Collision table for 16, 20, 24, 28, 32 and 36 bits:

| Bits | First string | Second string | Hashes computed | Prediction | Ratio |
|---:|---:|---:|---:|---:|---:|
| 16 | 157 | 251 | 252 | 320.85 | 0.7854 |
| 20 | 270 | 1877 | 1878 | 1283.39 | 1.4633 |
| 24 | 4163 | 8864 | 8865 | 5133.57 | 1.7269 |
| 28 | 16095 | 23815 | 23816 | 20534.30 | 1.1598 |
| 32 | 69235 | 95303 | 95304 | 82137.20 | 1.1603 |
| 36 | 63964 | 393644 | 393645 | 328548.78 | 1.1981 |


Plot log₂(hashes) against n, fit a straight line and report the measured slope:

![B2 birthday bound](images/b2_birthday_bound.png)

| Parameter | Value |
|---|---:|
| Measured slope | 0.510484 |
| Theoretical slope | 0.5 |
| Absolute deviation | 0.010484 |
| Relative deviation | 2.10% |


### Question
*State what you measured, what the theory predicts, and whether a single measurement per width is enough to tell them apart.*

### Explanation

According to the birthday bound, the expected number of
hashes required to find a collision is approximately
sqrt(pi/2) × 2^(n/2). Therefore, the theoretical slope
of log2(hashes) against the output length is 0.5.

The measured slope is 0.510484, which is close to the
theoretical value. This means that each additional output
bit increases the collision resistance by approximately
half a bit of computational work.

A single measurement per width is not sufficient to
establish a statistically significant difference between
the measured and theoretical slopes, since collision
searches have natural statistical variability.

Multiple independent experiments per width would be
necessary to obtain more reliable estimates. The measured
results are consistent with the birthday bound.

## 5. C1 - The forgery

### Results

The server challenge was:

- message: `user=student&role=guest&expires=2026-12-31`
- tag: `7daa0c342759f55c15bd8acc4a97b17f0adf1dad91e6b862cb0050afbdd92824`
- key length: 18 bytes
- target suffix: `&role=admin`

`forge()` computes the glue padding the server itself would have appended
when hashing `key || msg` (based on the total length `keylen + len(msg)`),
resumes SHA-256 from the state encoded in the given tag, and hashes only
the suffix from there.

| Parameter | Value |
|---|---:|
| Glue padding bytes | 68 |
| Extended message length | 121 bytes |

Extended message (hexadecimal):
```
757365723d73747564656e7426726f6c653d677565737426657870697265733d323032362d31322d333180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001e026726f6c653d61646d696e
```

Forged tag:
```
b0464fec2a6ca6532b99e20da7f485d4ca0fb3ac10d39e0746d4c243b119d4d0
```

This was verified against `naive_verify` with a self-chosen 18-byte key
in `tests/test_mac.py` (`test_forgery_verifies_with_chosen_key`), since
the real server key is never available to us — the attack's correctness
depends only on the key *length*, not its value.

### Question
*What would you do if the key length had not been given to you?*

### Explanation
Without the key length, the attacker does not know where to place the
glue padding or how many bytes `state_from_digest` has already absorbed,
so a single candidate forgery is not enough. The fix is to try every
plausible key length one at a time (for example 1 to 64 bytes, or
whatever range is reasonable for the system), computing `forge()` and
submitting the resulting message to the server for each guess. Only the
guess that matches the real key length produces a glue padding aligned
with the one the server actually used when it first hashed `key || msg`,
so only that one message is accepted — every other guess is rejected.
This turns a single forgery into a brute-force search over key lengths,
which is still cheap: it costs one SHA-256 call and one server request
per candidate length, not per key value.

## 6. C2 - HMAC

### Results
`hmac_sha256()` was verified against the three published RFC 4231
vectors (keys `0x0b`×20, `"Jefe"`, `"secret"`), all matching exactly —
see `tests/test_mac.py::TestC2Hmac::test_rfc4231_vectors`.

The same C1 attack was then run against an HMAC tag of the message
`user=student&role=guest` with an 18-byte key, attempting to append
`&role=admin`. The forged tag does **not** verify
(`test_length_extension_fails_against_hmac`): `hmac_verify` returns
`False` for the extended message.

### Question
*Explain why the outer hash in HMAC prevents the length-extension attack.*

### Explanation
HMAC is `H((K ⊕ opad) || H((K ⊕ ipad) || msg))`. The published tag reveals the final state of the outer hash, so that hash can technically be extended. However, the result is not a valid HMAC of the extended message: the verifier computes a fresh inner hash of that message using the secret key, and the outer hash always processes a fixed-length inner digest. The tag does not reveal the inner hash state needed to extend it. Therefore, the naive length-extension attack does not produce a valid HMAC.

## 7. D1 - Password Storage

### Measurements

A dictionary of 200,000 password candidates was generated using a fixed
random seed of 20357, following the reference code.

The following results were obtained by running `python crack.py` against the eight official hashes in the handout:

| Parameter | Result |
|---|---:|
| Dictionary size | 200,000 |
| Hashes computed | 200,000 |
| Passwords recovered | 8/8 |
| Execution time | 0.177215 seconds |

The execution time was measured in the ChatGPT Python environment during the final revision; it may differ on other machines.

| SHA-256 hash | Recovered password |
|---|---|
| `6382deaf1f5dc6e792b76db4a4a7bf2ba468884e000b25e7928e621e27fb23cb` | `football` |
| `a941a4c4fd0c01cddef61b8be963bf4c1e2b0811c037ce3f1835fddf6ef6c223` | `sunshine` |
| `203b70b5ae883932161bbd0bded9357e763e63afce98b16230be33f0b94c2cc5` | `trustno1` |
| `a9c43be948c5cabd56ef2bacffb77cdaa5eec49dd5eb0cc4129cf3eda5f0e74c` | `dragon` |
| `e4ad93ca07acb8d908a3aa41e920ea4f4ef4f26e7f86cf8291c5db289780a5ae` | `iloveyou` |
| `65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5` | `qwerty` |
| `000c285457fc971f862a79b786476c78812c8897063c6fa9c045f579a3b2d63f` | `monkey` |
| `1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032` | `letmein` |

Two users with the password `123456` produce the same database row:

```text
Hash: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

Using SHA256(salt || password), the same password produces different
hashes when different salts are used.

Database row 1:

```text
Salt: a3f1c0d94e2b7865
Hash: 3982dc6b270d4efa6654080c616e7001ee31148d48a44a79129ea1ec47052caa
```

Database row 2:

```text
Salt: 7b2e4f81cc09a512
Hash: 4cfd6301e91c2f90dc044561097abc13a1d5a7d9d7c8534cc5538cd65ce7f887
```

### Question
*How many hashes would an attacker need against a database of 500 users with a per-user salt, compared with the number actually computed? Which attack does salting prevent, and which does it not prevent?*

### Explanation

Without salts, each password candidate is hashed only once, and the
resulting lookup table can be reused for every user.

With a unique salt for each user, the attacker must compute a separate
hash for every password candidate and every user.

| Password storage method | Hashes required |
|---|---:|
| Without salt | 200,000 |
| With individual salts (500 users) | 100,000,000 |
| Cost multiplier | 500 |

The computational cost of an exhaustive dictionary attack is therefore
500 times higher.

Salting prevents the reuse of precomputed hash tables across users,
but does not prevent individual dictionary or brute-force attacks.

## 8. Secure Primitive vs. Secure Construction

### Question
*Part A built a hash that passes every test in the handout. Part C broke a MAC built from it without finding a single collision. Explain what this says about the difference between a secure primitive and a secure construction.*

### Explanation
A secure cryptographic primitive does not guarantee a secure construction. SHA-256 can provide collision resistance while a naive MAC built as `SHA256(key || message)` remains vulnerable to length extension. The attack exploits the way the hash is used rather than finding a collision. HMAC uses the same primitive in a construction designed for message authentication, preventing this attack. Security therefore depends on both the primitive and the construction.

## 9. Limitations and Observations

All 18 discovered unit tests passed in the final revision (0.516 seconds in the ChatGPT execution environment). Execution times vary by machine. The 500-user salted cost is an exhaustive-search estimate, not a measured attack. The C1 forgery was tested locally with a chosen key; acceptance by the actual challenge server was not independently verified.

## 10. AI Assistance

OpenAI ChatGPT was used throughout this practice as a supporting tool
for understanding cryptographic concepts, implementing and reviewing
the code, debugging errors, developing unit tests, interpreting
experimental results and improving the documentation.

The suggestions were reviewed and adapted to the requirements of the
practice and the structure of the project. The implementations were
validated through automated tests, and the reported experimental
measurements were obtained from actual code executions.