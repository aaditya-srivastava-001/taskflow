const API_URL = "http://127.0.0.1:8000";


// ==========================================
// DOM ELEMENTS
// ==========================================

const taskTableBody = document.getElementById("taskTableBody");
const emptyState = document.getElementById("emptyState");
const taskCount = document.getElementById("taskCount");

const totalTasks = document.getElementById("totalTasks");
const todoTasks = document.getElementById("todoTasks");
const progressTasks = document.getElementById("progressTasks");
const doneTasks = document.getElementById("doneTasks");

const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");
const priorityFilter = document.getElementById("priorityFilter");
const refreshBtn = document.getElementById("refreshBtn");

const taskModal = document.getElementById("taskModal");
const openTaskModal = document.getElementById("openTaskModal");
const closeModal = document.getElementById("closeModal");

const taskForm = document.getElementById("taskForm");


// ==========================================
// QUICK-ADD ELEMENTS
// ==========================================

const quickAddInput =
    document.getElementById("quickAddInput");

const quickAddProjectId =
    document.getElementById("quickAddProjectId");

const quickAddBtn =
    document.getElementById("quickAddBtn");

const quickAddStatus =
    document.getElementById("quickAddStatus");


// ==========================================
// APPLICATION STATE
// ==========================================

let tasks = [];


// ==========================================
// FETCH TASKS
// ==========================================

async function fetchTasks() {

    try {

        const response =
            await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }

        tasks = await response.json();

        renderTasks();
        updateStatistics();

    } catch (error) {

        console.error(
            "Error fetching tasks:",
            error
        );

        showError(
            "Could not connect to the TaskFlow backend."
        );
    }
}


// ==========================================
// RENDER TASKS
// ==========================================

function renderTasks() {

    const searchTerm =
        searchInput.value
            .trim()
            .toLowerCase();

    const selectedStatus =
        statusFilter.value;

    const selectedPriority =
        priorityFilter.value;


    const filteredTasks =
        tasks.filter(task => {

            const matchesSearch =
                task.title
                    .toLowerCase()
                    .includes(searchTerm);


            const matchesStatus =
                !selectedStatus ||
                task.status === selectedStatus;


            const matchesPriority =
                !selectedPriority ||
                task.priority === selectedPriority;


            return (
                matchesSearch &&
                matchesStatus &&
                matchesPriority
            );
        });


    taskTableBody.innerHTML = "";


    taskCount.textContent =
        `${filteredTasks.length} ${
            filteredTasks.length === 1
                ? "task"
                : "tasks"
        }`;


    if (filteredTasks.length === 0) {

        emptyState.style.display = "block";

        return;

    } else {

        emptyState.style.display = "none";
    }


    filteredTasks.forEach(task => {

        const row =
            document.createElement("tr");


        // ------------------------------
        // TASK CELL
        // ------------------------------

        const taskCell =
            document.createElement("td");

        const title =
            document.createElement("strong");

        title.textContent =
            task.title;

        taskCell.appendChild(title);


        if (task.description) {

            const description =
                document.createElement("div");

            description.className =
                "task-description";

            description.textContent =
                task.description;

            taskCell.appendChild(description);
        }


        // ------------------------------
        // PRIORITY CELL
        // ------------------------------

        const priorityCell =
            document.createElement("td");

        const priorityBadge =
            document.createElement("span");

        priorityBadge.className =
            `badge priority-${task.priority}`;

        priorityBadge.textContent =
            formatPriority(task.priority);

        priorityCell.appendChild(
            priorityBadge
        );


        // ------------------------------
        // STATUS CELL
        // ------------------------------

        const statusCell =
            document.createElement("td");

        const statusBadge =
            document.createElement("span");

        statusBadge.className =
            `badge status-${task.status}`;

        statusBadge.textContent =
            formatStatus(task.status);

        statusCell.appendChild(
            statusBadge
        );


        // ------------------------------
        // DUE DATE CELL
        // ------------------------------

        const dueDateCell =
            document.createElement("td");

        dueDateCell.textContent =
            task.due_date || "—";


        // ------------------------------
        // ACTION CELL
        // ------------------------------

        const actionCell =
            document.createElement("td");

        const deleteButton =
            document.createElement("button");

        deleteButton.className =
            "action-btn delete-btn";

        deleteButton.textContent =
            "Delete";

        deleteButton.addEventListener(
            "click",
            () => deleteTask(task.id)
        );

        actionCell.appendChild(
            deleteButton
        );


        // ------------------------------
        // ADD CELLS
        // ------------------------------

        row.appendChild(taskCell);
        row.appendChild(priorityCell);
        row.appendChild(statusCell);
        row.appendChild(dueDateCell);
        row.appendChild(actionCell);

        taskTableBody.appendChild(row);

    });
}


// ==========================================
// STATISTICS
// ==========================================

function updateStatistics() {

    const total = tasks.length;

    const todo =
        tasks.filter(
            task => task.status === "todo"
        ).length;

    const progress =
        tasks.filter(
            task => task.status === "in_progress"
        ).length;

    const done =
        tasks.filter(
            task => task.status === "done"
        ).length;


    totalTasks.textContent = total;
    todoTasks.textContent = todo;
    progressTasks.textContent = progress;
    doneTasks.textContent = done;
}


// ==========================================
// CREATE NORMAL TASK
// ==========================================

taskForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const taskData = {

            title:
                document.getElementById(
                    "taskTitle"
                ).value.trim(),

            description:
                document.getElementById(
                    "taskDescription"
                ).value.trim() || null,

            priority:
                document.getElementById(
                    "taskPriority"
                ).value,

            status:
                document.getElementById(
                    "taskStatus"
                ).value,

            due_date:
                document.getElementById(
                    "taskDueDate"
                ).value || null,

            project_id:
                Number(
                    document.getElementById(
                        "projectId"
                    ).value
                )
        };


        try {

            const response =
                await fetch(
                    `${API_URL}/tasks`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(taskData)
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to create task"
                );
            }


            taskForm.reset();


            document.getElementById(
                "projectId"
            ).value = 1;


            closeTaskModal();


            await fetchTasks();


            alert(
                "Task created successfully!"
            );


        } catch (error) {

            console.error(
                "Error creating task:",
                error
            );

            alert(error.message);
        }

    }
);


// ==========================================
// AI QUICK-ADD
// ==========================================

async function quickAddTask() {

    const text =
        quickAddInput.value.trim();

    const projectId =
        Number(
            quickAddProjectId.value
        );


    if (!text) {

        quickAddStatus.textContent =
            "Please describe the task.";

        return;
    }


    if (!projectId || projectId < 1) {

        quickAddStatus.textContent =
            "Please enter a valid project ID.";

        return;
    }


    quickAddBtn.disabled = true;

    quickAddStatus.textContent =
        "Processing task...";


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/quick-add`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            text: text,
                            project_id: projectId
                        })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Quick-Add failed"
            );
        }


        quickAddStatus.textContent =
            `Created: ${data.title} | ` +
            `Priority: ${formatPriority(data.priority)}` +
            `${
                data.due_date
                    ? ` | Due: ${data.due_date}`
                    : ""
            }`;


        quickAddInput.value = "";


        await fetchTasks();


    } catch (error) {

        console.error(
            "Quick-Add error:",
            error
        );

        quickAddStatus.textContent =
            error.message;

    } finally {

        quickAddBtn.disabled = false;
    }
}


quickAddBtn.addEventListener(
    "click",
    quickAddTask
);


quickAddInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {

            event.preventDefault();

            quickAddTask();
        }
    }
);


// ==========================================
// DELETE TASK
// ==========================================

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to delete task"
            );
        }


        await fetchTasks();


    } catch (error) {

        console.error(
            "Error deleting task:",
            error
        );

        alert(error.message);
    }
}


// ==========================================
// SEARCH
// ==========================================

searchInput.addEventListener(
    "input",
    renderTasks
);


// ==========================================
// FILTERS
// ==========================================

statusFilter.addEventListener(
    "change",
    renderTasks
);

priorityFilter.addEventListener(
    "change",
    renderTasks
);


// ==========================================
// REFRESH
// ==========================================

refreshBtn.addEventListener(
    "click",
    fetchTasks
);


// ==========================================
// MODAL
// ==========================================

openTaskModal.addEventListener(
    "click",
    () => {

        taskModal.classList.remove(
            "hidden"
        );

    }
);


closeModal.addEventListener(
    "click",
    closeTaskModal
);


taskModal.addEventListener(
    "click",
    function (event) {

        if (event.target === taskModal) {
            closeTaskModal();
        }

    }
);


function closeTaskModal() {

    taskModal.classList.add(
        "hidden"
    );
}


// ==========================================
// HELPERS
// ==========================================

function formatPriority(priority) {

    return priority
        .charAt(0)
        .toUpperCase() +
        priority.slice(1);
}


function formatStatus(status) {

    if (status === "in_progress") {
        return "In Progress";
    }

    return status
        .charAt(0)
        .toUpperCase() +
        status.slice(1);
}


function showError(message) {

    taskTableBody.innerHTML = "";

    emptyState.style.display = "block";

    emptyState.textContent = message;

    taskCount.textContent = "0 tasks";
}


// ==========================================
// INITIAL LOAD
// ==========================================

fetchTasks();