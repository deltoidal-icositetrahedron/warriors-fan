const form = document.getElementById("askForm");
const input = document.getElementById("askInput");
const sendBtn = document.getElementById("sendBtn");
const chat = document.getElementById("chat");

// Hard fail early if IDs don't match
if (!form || !input || !sendBtn || !chat) {
  console.error({ form, input, sendBtn, chat });
  throw new Error("Missing required elements. Check IDs: askForm, askInput, sendBtn, chat.");
}

function appendMessage(role, text) {

  const row = document.createElement("div");
  row.className = `msg ${role}`; // role: "user" or "bot"

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  row.appendChild(bubble);
  chat.appendChild(row);

  // autoscroll
  chat.scrollTop = chat.scrollHeight;

  // return the bubble so we can update its text later (e.g., Thinking... -> final)
  return bubble;
}

function setSendEnabled(enabled) {
  const btn = document.getElementById("sendBtn");
  btn.disabled = !enabled;
}

async function postToBackend(message) {
  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  // Try to parse JSON even on errors, but handle gracefully
  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    // ignore JSON parse failure
  }

  if (!res.ok) {
    const serverMsg =
      (data && (data.error || data.message)) ||
      `Request failed (HTTP ${res.status})`;
    throw new Error(serverMsg);
  }

  if (!data || typeof data.reply !== "string") {
    throw new Error("Bad response from server: expected { reply: string }");
  }

  return data.reply;
}

// Initial bot message
chat.innerHTML = "";
appendMessage("bot", "Ask me anything about the Golden State Warriors 👇");

// Enable/disable Send button based on whether user has netered anything
const refreshSendState = () => setSendEnabled(input.value.trim().length > 0);
input.addEventListener("input", refreshSendState);
refreshSendState();

// Detects form submission then awaits response from Claude

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = input.value.trim();
  if (!question) return;

  // UI: show user message
  appendMessage("user", question);

  // Reset input
  input.value = "";
  refreshSendState();

  // bot thinking bubble
  const thinkingBubble = appendMessage("bot", "Thinking…");

  try {
    // call flask
    const reply = await postToBackend(question);

    // replace thinking bubbles with answer
    thinkingBubble.textContent = reply;
    chat.scrollTop = chat.scrollHeight;
  } catch (err) {
    console.error(err);
    thinkingBubble.textContent = `Error: ${err.message}`;
    chat.scrollTop = chat.scrollHeight;
  }
});
