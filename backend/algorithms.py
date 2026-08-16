# ==========================================
# TASKFLOW ALGORITHMS
# ==========================================


# ------------------------------------------
# INSERTION SORT
# ------------------------------------------

def insertion_sort_tasks(tasks):
    """
    Sort tasks by priority using insertion sort.

    Priority order:
    high -> medium -> low

    Time Complexity:
        Best:    O(n)
        Average: O(n^2)
        Worst:   O(n^2)

    Space Complexity:
        O(1) auxiliary space
    """

    priority_rank = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    sorted_tasks = tasks.copy()

    for i in range(1, len(sorted_tasks)):

        current_task = sorted_tasks[i]
        current_priority = priority_rank.get(
            current_task.priority,
            4
        )

        j = i - 1

        while j >= 0:

            previous_priority = priority_rank.get(
                sorted_tasks[j].priority,
                4
            )

            if previous_priority <= current_priority:
                break

            sorted_tasks[j + 1] = sorted_tasks[j]
            j -= 1

        sorted_tasks[j + 1] = current_task

    return sorted_tasks


# ------------------------------------------
# LINEAR SEARCH
# ------------------------------------------

def linear_search_tasks(tasks, title):
    """
    Search for a task by title using linear search.

    Time Complexity:
        Best:    O(1)
        Average: O(n)
        Worst:   O(n)

    Space Complexity:
        O(1) auxiliary space
    """

    search_title = title.strip().lower()

    for task in tasks:

        if task.title.lower() == search_title:
            return task

    return None


# ------------------------------------------
# BINARY SEARCH
# ------------------------------------------

def binary_search_tasks(tasks, title):
    """
    Search for a task by title using binary search.

    IMPORTANT:
    Binary search requires the data to be sorted.

    The function first creates a list sorted by title,
    then performs binary search.

    Time Complexity:
        Sorting: O(n log n)
        Search:  O(log n)

    Space Complexity:
        O(n) because a sorted copy is created.
    """

    search_title = title.strip().lower()

    sorted_tasks = sorted(
        tasks,
        key=lambda task: task.title.lower()
    )

    left = 0
    right = len(sorted_tasks) - 1

    while left <= right:

        middle = (left + right) // 2

        current_title = sorted_tasks[middle].title.lower()

        if current_title == search_title:
            return sorted_tasks[middle]

        if current_title < search_title:
            left = middle + 1
        else:
            right = middle - 1

    return None