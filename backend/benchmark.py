import random

from algorithms import (
    insertion_sort_count,
    linear_search_count,
    binary_search_count
)


def make_records(size):
    records = [
        {
            "id": i,
            "title": f"Task {i:06d}"
        }
        for i in range(size)
    ]

    random.shuffle(records)

    return records


def run_benchmark():

    sizes = [100, 1000, 5000]

    print("=" * 60)
    print("TASKFLOW ALGORITHM COMPARISON BENCHMARK")
    print("=" * 60)

    for size in sizes:

        print(f"\nDataset size: {size}")

        # -------------------------
        # INSERTION SORT
        # -------------------------

        insertion_data = make_records(size)

        insertion_comparisons = insertion_sort_count(
            insertion_data,
            "title"
        )

        print(
            f"Insertion Sort comparisons: "
            f"{insertion_comparisons}"
        )

        # -------------------------
        # LINEAR SEARCH
        # -------------------------

        linear_data = make_records(size)

        target = f"Task {size - 1:06d}"

        linear_result = linear_search_count(
            linear_data,
            target,
            "title"
        )

        print(
            f"Linear Search comparisons: "
            f"{linear_result['comparison_count']}"
        )

        # -------------------------
        # BINARY SEARCH
        # -------------------------

        binary_data = make_records(size)

        # Binary search requires sorted data.
        # We use our own insertion sort.
        insertion_sort_count(
            binary_data,
            "title"
        )

        binary_result = binary_search_count(
            binary_data,
            target,
            "title"
        )

        print(
            f"Binary Search comparisons: "
            f"{binary_result['comparison_count']}"
        )

        print(
            f"Linear result index: "
            f"{linear_result['index']}"
        )

        print(
            f"Binary result index: "
            f"{binary_result['index']}"
        )

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()