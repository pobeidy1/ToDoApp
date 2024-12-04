const apiBaseUrl = "http://localhost:5000";

async function fetchTasks() {
    const response = await fetch(`${apiBaseUrl}/tasks`);
    const tasks = await response.json();
    return tasks;
}

async function addTask() {
    const title = prompt("Enter task title:");
    if (title) {
        const response = await fetch(`${apiBaseUrl}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, date_created: getCurrentDate() }),
        });
        if (response.ok) renderTasks();
    }
}

async function addSubtask(taskId) {
    const title = prompt("Enter subtask title:");
    if (title) {
        await fetch(`${apiBaseUrl}/subtasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task_id: taskId, title, date_created: getCurrentDate() }),
        });
        renderTasks();
    }
}

async function renderTasks() {
    const tasks = await fetchTasks();
    // Convert SQL data into the expected format and render
}
