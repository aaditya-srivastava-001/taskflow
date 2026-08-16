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
// APPLICATION STATE
// ==========================================

let tasks = [];


// ==========================================
// FETCH TASKS
// ==========================================

async function fetchTasks() {

    try {

        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }

        tasks = await response.json();

        renderTasks();
        updateStatistics();

    } catch (error) {

        console.error("Error fetching tasks:", error);

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
        searchInput.value.trim().toLowerCase();

    const selectedStatus =
        statusFilter.value;

    const selectedPriority =
        priorityFilter.value;


    const filteredTasks = tasks.filter(task => {

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


        row.innerHTML = `

            <td>
                <strong>
                    ${escapeHtml(task.title)}
                </strong>

                ${
                    task.description
                        ? `
                            <div class="task-description">
                                ${escapeHtml(
                                    task.description
                                )}
                            </div>
                          `
                        : ""
                }
            </td>


            <td>

                <span class="badge priority-${task.priority}">
                    ${formatPriority(task.priority)}
                </span>

            </td>


            <td>

                <span class="badge status-${task.status}">
                    ${formatStatus(task.status)}
                </span>

            </td>


            <td>
                ${task.due_date || "—"}
            </td>


            <td>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteTask(${task.id})"
                >
                    Delete
                </button>

            </td>
        `;


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
// CREATE TASK
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

            const response = await fetch(
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


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
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