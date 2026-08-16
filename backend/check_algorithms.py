from algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def check_insertion_sort():
    records = [
        {"value": 5},
        {"value": 2},
        {"value": 4},
        {"value": 1},
        {"value": 3}
    ]

    insertion_sort(records, "value")

    values = [record["value"] for record in records]

    return values == [1, 2, 3, 4, 5]


def check_linear_search():
    records = [
        {"value": "A"},
        {"value": "B"},
        {"value": "C"},
        {"value": "D"}
    ]

    index = linear_search(
        records,
        "C",
        "value"
    )

    missing = linear_search(
        records,
        "Z",
        "value"
    )

    return index == 2 and missing == -1


def check_binary_search():
    records = [
        {"value": 1},
        {"value": 3},
        {"value": 5},
        {"value": 7},
        {"value": 9}
    ]

    index = binary_search(
        records,
        7,
        "value"
    )

    missing = binary_search(
        records,
        8,
        "value"
    )

    return index == 3 and missing == -1


def check_comparison_counts():

    records = [
        {"value": i}
        for i in range(100)
    ]

    insertion_data = list(records)

    insertion_count = insertion_sort_count(
        insertion_data,
        "value"
    )

    linear_result = linear_search_count(
        records,
        99,
        "value"
    )

    binary_result = binary_search_count(
        records,
        99,
        "value"
    )

    return (
        insertion_count > 0
        and linear_result["comparison_count"] > 0
        and binary_result["comparison_count"] > 0
        and linear_result["index"] == 99
        and binary_result["index"] == 99
    )


def check_binary_is_more_efficient():

    records = [
        {"value": i}
        for i in range(1000)
    ]

    linear_result = linear_search_count(
        records,
        999,
        "value"
    )

    binary_result = binary_search_count(
        records,
        999,
        "value"
    )

    return (
        binary_result["comparison_count"]
        < linear_result["comparison_count"]
    )


def run_checks():

    checks = {
        "Insertion Sort": check_insertion_sort(),
        "Linear Search": check_linear_search(),
        "Binary Search": check_binary_search(),
        "Comparison Counting": check_comparison_counts(),
        "Binary Search Efficiency": check_binary_is_more_efficient()
    }

    print("=" * 60)
    print("TASKFLOW ALGORITHM CHECKER")
    print("=" * 60)

    all_passed = True

    for name, passed in checks.items():

        status = "PASS" if passed else "FAIL"

        print(
            f"{name:<30} {status}"
        )

        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("OVERALL: PASS")
    else:
        print("OVERALL: FAIL")

    print("=" * 60)

    return all_passed


if __name__ == "__main__":

    success = run_checks()

    raise SystemExit(
        0 if success else 1
    )