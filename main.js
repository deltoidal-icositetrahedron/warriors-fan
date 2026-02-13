let pyodideReadyPromise = null;

function appendMessage(role, text) {
  const chat = document.getElementById("chat");

  const row = document.createElement("div");
  row.className = `msg ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  row.appendChild(bubble);
  chat.appendChild(row);

  // autoscroll to bottom (like chat apps)
  chat.scrollTop = chat.scrollHeight;
}

async function initPyodide() {
  const pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/"
  });

  pyodide.runPython(`
def answer(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Type a question first."
    return f"You asked: {q}"
`);
  return pyodide;
}

window.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("askForm");
  const input = document.getElementById("askInput");
  const sendBtn = document.getElementById("sendBtn");
  const chat = document.getElementById("chat");

  // Replace initial "Loading Python…" bubble with nicer flow
  chat.innerHTML = "";
  appendMessage("bot", "Loading Python…");

  input.addEventListener("input", () => {
    sendBtn.disabled = input.value.trim().length === 0;
  });

  pyodideReadyPromise = initPyodide();

  try {
    await pyodideReadyPromise;
    // remove loading and add ready message
    chat.innerHTML = "";
    appendMessage("bot", "Python ready. Ask a question 👇");
    sendBtn.disabled = input.value.trim().length === 0;
  } catch (e) {
    console.error(e);
    chat.innerHTML = "";
    appendMessage("bot", "Failed to load Python (Pyodide). Check console.");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    appendMessage("user", question);
    input.value = "";
    sendBtn.disabled = true;

    // Optional: a “thinking…” bot bubble
    const thinkingId = crypto.randomUUID?.() ?? String(Date.now());
    const chatEl = document.getElementById("chat");
    const thinkingRow = document.createElement("div");
    thinkingRow.className = "msg bot";
    thinkingRow.dataset.id = thinkingId;

    const thinkingBubble = document.createElement("div");
    thinkingBubble.className = "bubble";
    thinkingBubble.textContent = "Thinking…";
    thinkingRow.appendChild(thinkingBubble);
    chatEl.appendChild(thinkingRow);
    chatEl.scrollTop = chatEl.scrollHeight;

    try {
      const pyodide = await pyodideReadyPromise;

      pyodide.globals.set("question_from_js", question);
      const result = pyodide.runPython(`answer(question_from_js)`);
      pyodide.globals.delete("question_from_js");

      // Replace “Thinking…” bubble with real answer
      thinkingBubble.textContent = String(result);
      chatEl.scrollTop = chatEl.scrollHeight;
    } catch (err) {
      console.error(err);
      thinkingBubble.textContent = "Python error. Check console.";
      chatEl.scrollTop = chatEl.scrollHeight;
    }
  });
});