import random
import time

from algorithms import (
    insertion_sort_tasks,
    linear_search_tasks,
    binary_search_tasks
)


class BenchmarkTask:
    def __init__(self, title, priority="medium"):
        self.title = title
        self.priority = priority


def generate_tasks(size):
    priorities = ["low", "medium", "high"]

    return [
        BenchmarkTask(
            title=f"Task {i}",
            priority=random.choice(priorities)
        )
        for i in range(size)
    ]


def benchmark_insertion_sort(tasks):
    start = time.perf_counter()

    insertion_sort_tasks(tasks)

    end = time.perf_counter()

    return end - start


def benchmark_linear_search(tasks, target):
    start = time.perf_counter()

    linear_search_tasks(tasks, target)

    end = time.perf_counter()

    return end - start


def benchmark_binary_search(tasks, target):
    start = time.perf_counter()

    binary_search_tasks(tasks, target)

    end = time.perf_counter()

    return end - start


def run_benchmark():

    dataset_sizes = [100, 500, 1000, 5000]

    print("\nTaskFlow Algorithm Benchmark")
    print("=" * 60)

    for size in dataset_sizes:

        tasks = generate_tasks(size)

        target = f"Task {size - 1}"

        insertion_time = benchmark_insertion_sort(tasks)

        linear_time = benchmark_linear_search(
            tasks,
            target
        )

        binary_time = benchmark_binary_search(
            tasks,
            target
        )

        print(f"\nDataset size: {size}")
        print(f"Insertion Sort : {insertion_time:.8f} seconds")
        print(f"Linear Search  : {linear_time:.8f} seconds")
        print(f"Binary Search  : {binary_time:.8f} seconds")


if __name__ == "__main__":
    run_benchmark()

    