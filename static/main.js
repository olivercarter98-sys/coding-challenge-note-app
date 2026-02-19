function toggleEdit(id) {
  const view = document.getElementById("view-" + id);
  const edit = document.getElementById("edit-" + id);
  const isEditing = edit.style.display !== "none";
  view.style.display = isEditing ? "block" : "none";
  edit.style.display = isEditing ? "none" : "block";
}

const textarea = document.getElementById("notes");
const counter  = document.getElementById("char-count");
const MAX      = 1000;

function updateCount() {
  const n = textarea.value.length;
  counter.textContent = n + " / " + MAX;
  counter.classList.toggle("warn", n > MAX * 0.85);
}

textarea.addEventListener("input", updateCount);
updateCount();