async function fetchEvents() {
  const res = await fetch("/events");
  const data = await res.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  data.forEach(event => {
    const li = document.createElement("li");
    li.textContent = event.message;
    list.appendChild(li);
  });
}

setInterval(fetchEvents, 15000);
fetchEvents();
