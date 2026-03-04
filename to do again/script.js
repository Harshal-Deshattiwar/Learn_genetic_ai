document.getElementById('add-btn').addEventListener('click', function() {
  const input = document.getElementById('todo-input');
  const value = input.value.trim();
  if (value) {
    addTodo(value);
    input.value = '';
  }
});

document.getElementById('todo-input').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    document.getElementById('add-btn').click();
  }
});

function addTodo(text) {
  const li = document.createElement('li');
  li.textContent = text;
  const delBtn = document.createElement('button');
  delBtn.textContent = 'Delete';
  delBtn.onclick = function() {
    li.remove();
  };
  li.appendChild(delBtn);
  document.getElementById('todo-list').appendChild(li);
}

