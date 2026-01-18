const listEl = document.getElementById('todo-list');
const inputEl = document.getElementById('new-todo');

async function fetchTodos() {
    const res = await fetch('/todos');
    const todos = await res.json();
    listEl.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = todo.done ? 'done' : '';

        li.innerHTML = `
      <div class="todo-text">
        <input type="checkbox" ${todo.done ? 'checked' : ''} onchange="toggleDone(${todo.id}, this.checked)">
        <span>${todo.title}</span>
      </div>
      <div>
        <button class="edit" onclick="editTodo(${todo.id}, '${todo.title}')">Edit</button>
        <button class="delete" onclick="deleteTodo(${todo.id})">Delete</button>
      </div>
    `;

        listEl.appendChild(li);
    });
}

async function addTodo() {
    const title = inputEl.value.trim();
    if (!title) return;
    await fetch('/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });
    inputEl.value = '';
    fetchTodos();
}

async function editTodo(id, oldTitle) {
    const title = prompt("Edit todo:", oldTitle);
    if (title === null) return;
    await fetch(`/todos/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });
    fetchTodos();
}

async function deleteTodo(id) {
    if (!confirm("Delete this todo?")) return;
    await fetch(`/todos/${id}`, { method: 'DELETE' });
    fetchTodos();
}

async function toggleDone(id, done) {
    await fetch(`/todos/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done })
    });
    fetchTodos();
}

// Initial load
fetchTodos();