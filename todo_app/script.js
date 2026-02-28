document.getElementById("add-todo").addEventListener("click", function() {
  const todoInput = document.getElementById("todo-input");
  const todoText = todoInput.value.trim();
  if (todoText !== "") {
    const li = document.createElement("li");
    li.textContent = todoText;
    li.addEventListener("click", function() {
      li.remove();
    });
    document.getElementById("todo-list").appendChild(li);
    todoInput.value = "";
  }
});
document.getElementById("theme-toggle").addEventListener("click", function() {
  document.body.classList.toggle("dark-theme");
});
