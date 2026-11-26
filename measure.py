import random
import math
from sha256 import sha256
import matplotlib.pyplot as plt
from statistics import linear_regression


# B1: The avalanche effect

def avalanche(trials: int, msglen: int, seed: int) -> list[int]:

    if trials <= 0 or msglen <= 0:
        raise ValueError("Invalid number of trials or message length.")

    rng = random.Random(seed)
    results = []

    for _ in range(trials):

        # Generate a random message
        message = rng.randbytes(msglen)

        # Select a random bit
        bit = rng.randrange(msglen * 8)

        # Flip the selected bit
        modified = bytearray(message)
        modified[bit // 8] ^= 1 << (bit % 8)

        # Compute both hashes
        original_hash = sha256(message)
        modified_hash = sha256(bytes(modified))

        # Count the different output bits
        differences = 0

        for a, b in zip(original_hash, modified_hash):
            differences += (a ^ b).bit_count()

        results.append(differences)

    return results

def print_histogram(results: list[int]) -> None:

    # Group the results into bins of 8 bits
    histogram = {}

    for value in results:
        lower = (value // 8) * 8

        if lower not in histogram:
            histogram[lower] = 0

        histogram[lower] += 1

    for lower in sorted(histogram):
        upper = lower + 7
        count = histogram[lower]

        bar = "*" * (count // 10)

        print(f"{lower:3d}-{upper:3d}: {count:4d} {bar}")

def plot_histogram(results: list[int], output_path: str) -> None:

    # Count values in 8-bit bins
    histogram = {}

    for value in results:
        lower = (value // 8) * 8
        histogram[lower] = histogram.get(lower, 0) + 1

    bins = sorted(histogram.keys())
    labels = [f"{lower}-{lower + 7}" for lower in bins]
    counts = [histogram[lower] for lower in bins]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts)
    plt.xlabel("Changed output bits")
    plt.ylabel("Frequency")
    plt.title("B1 - Avalanche effect histogram")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# B2: The birthday bound

def truncate(digest: bytes, nbits: int) -> int:

    if nbits <= 0 or nbits > len(digest) * 8:
        raise ValueError("Invalid number of bits.")

    # Convert the digest into an integer
    value = int.from_bytes(digest, "big")

    # Keep only the first nbits
    return value >> (len(digest) * 8 - nbits)

def find_collision(nbits: int) -> tuple[str, str, int]:

    # Store previously computed truncated digests
    seen = {}
    counter = 0

    while True:

        # Generate the next decimal string
        message = str(counter)

        # Compute and truncate its SHA-256 digest
        digest = sha256(message.encode("ascii"))
        truncated = truncate(digest, nbits)

        # Check whether a collision has been found
        if truncated in seen:
            return seen[truncated], message, counter + 1

        # Store the digest and its corresponding message
        seen[truncated] = message

        counter += 1

def plot_birthday_bound(widths: list[int], counts: list[int],
                        output_path: str) -> float:

    # Compute the base-2 logarithm of the measured hashes
    log_hashes = [math.log2(count) for count in counts]

    # Fit a straight line
    slope, intercept = linear_regression(widths, log_hashes)

    fitted = [slope * n + intercept for n in widths]

    # Compute the theoretical prediction
    theoretical = [
        math.log2(math.sqrt(math.pi / 2) * 2 ** (n / 2))
        for n in widths
    ]

    # Plot measured results, fitted line and theoretical line
    plt.figure(figsize=(8, 5))

    plt.scatter(widths, log_hashes, label="Measured results")
    plt.plot(widths, fitted, label=f"Linear fit (slope={slope:.4f})")
    plt.plot(widths, theoretical, "--", label="Theoretical prediction")

    plt.xlabel("Truncated output bits (n)")
    plt.ylabel("log2(hashes computed)")
    plt.title("B2 - Birthday bound")
    plt.xticks(widths)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return slope

if __name__ == "__main__":

    results = avalanche(2000, 32, 20357)

    # B1: The avalanche effect
    print("B1 - The avalanche effect")
    print("Trials:", len(results))
    print("Mean:", sum(results) / len(results))
    print("Min:", min(results))
    print("Max:", max(results))

    print("\nHistogram (8-bit bins):")
    print_histogram(results)

    plot_histogram(results, "images/b1_avalanche_histogram.png")
    print("\nSaved plot to images/b1_avalanche_histogram.png")

        # B2: Birthday bound experiment
    print("\nB2 - The birthday bound")

    widths = [16, 20, 24, 28, 32, 36]
    counts = []

    for nbits in widths:

        first, second, hashes = find_collision(nbits)

        prediction = math.sqrt(math.pi / 2) * 2 ** (nbits / 2)

        ratio = hashes / prediction

        counts.append(hashes)

        print(f"\nBits: {nbits}")
        print(f"Collision: {first}, {second}")
        print(f"Hashes computed: {hashes}")
        print(f"Theoretical prediction: {prediction:.2f}")
        print(f"Ratio: {ratio:.4f}")

    slope = plot_birthday_bound(
        widths, counts, "images/b2_birthday_bound.png"
    )

    print(f"\nMeasured slope: {slope:.6f}")
    print("Theoretical slope: 0.5")
    print("\nSaved plot to images/b2_birthday_bound.png")