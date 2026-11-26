import random
import matplotlib.pyplot as plt
from sha256 import sha256


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

if __name__ == "__main__":

    results = avalanche(2000, 32, 20357)

    print("B1 - The avalanche effect")
    print("Trials:", len(results))
    print("Mean:", sum(results) / len(results))
    print("Min:", min(results))
    print("Max:", max(results))

    print("\nHistogram (8-bit bins):")
    print_histogram(results)

    plot_histogram(results, "images/b1_avalanche_histogram.png")
    print("\nSaved plot to images/b1_avalanche_histogram.png")