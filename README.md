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
To run the avalanche effect experiment from B1, run:
```bash
python measure.py
```
This experiment performs 2,000 trials using random messages of 32 bytes and a fixed seed of 20357 to ensure reproducibility. It displays the mean, minimum, maximum and a histogram with bins of 8 bits.

[TO DO - Explain mac.py, forge.py and crack.py]

## 2. A3 - Resuming from a known state

### Question
*State in two lines why the second and third bullets agree, and what that tells you about what a SHA-256 digest reveals.*

### Explanation
Both results agree because the SHA-256 digest contains the internal state after processing the original message and its padding, allowing the algorithm to continue from that state. 

This means that knowing a SHA-256 digest makes it possible to extend the hashed message without knowing its original contents.

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
[TO DO - Extended message in hexadecimal]
[TO DO - Forged tag]
[TO DO - Number of glue padding bytes and total extended message length]

### Question
*What would you do if the key length had not been given to you?*

### Explanation
[TO DO]

## 6. C2 - HMAC

### Results
[TO DO - HMAC test vectors and verification that the
length-extension attack fails against HMAC]

### Question
*Explain why the outer hash in HMAC prevents the length-extension attack.*

### Explanation
[TO DO]

## 7. D1 - Password Storage

### Measurements
[TO DO - Eight recovered passwords]
[TO DO - Dictionary size, total number of hashes computed and execution time]
[TO DO - Database row for password 123456 without salt]
[TO DO - Database rows for password 123456 with salts a3f1c0d94e2b7865 and 7b2e4f81cc09a512]

### Question
*How many hashes would an attacker need against a database of 500 users with a per-user salt, compared with the number actually computed? Which attack does salting prevent, and which does it not prevent?*

### Explanation
[TO DO]

## 8. Secure Primitive vs. Secure Construction

### Question
*Part A built a hash that passes every test in the handout. Part C broke a MAC built from it without finding a single collision. Explain what this says about the difference between a secure primitive and a secure construction.*

### Explanation
[TO DO]

## 9. Limitations and Observations
[TO DO]

## 10. AI Assistance
[TO DO]