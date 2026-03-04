document.getElementById('add-btn').addEventListener('click', function() {
  const input = document.getElementById('todo-input');
  const task = input.value.trim();
  if (task !== '') {
    addTask(task);
    input.value = '';
  }
});

function addTask(task) {
  const ul = document.getElementById('todo-list');
  const li = document.createElement('li');
  li.textContent = task;

  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = 'Delete';
  deleteBtn.className = 'delete-btn';
  deleteBtn.addEventListener('click', function() {
    ul.removeChild(li);
  });

  li.addEventListener('click', function() {
    li.classList.toggle('completed');
  });

  li.appendChild(deleteBtn);
  ul.appendChild(li);
}
