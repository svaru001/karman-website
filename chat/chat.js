/* ─────────────────────────────────────────────
   KARMAN — Chat Widget JS
───────────────────────────────────────────── */

(function () {
  const API_URL = "https://karman-rag-production.up.railway.app";

  // State
  let isOpen = false;
  let isLoading = false;

  // DOM refs (set after inject)
  let panel, messages, input, sendBtn, toggleBtn;

  // ── Inject HTML ──
  function inject() {
    const widget = document.createElement("div");
    widget.className = "chat-widget";
    widget.innerHTML = `
      <div class="chat-panel" id="chatPanel">
        <div class="chat-header">
          <div class="chat-header__icon">K</div>
          <div class="chat-header__text">
            <h3>Karman Compliance Assistant</h3>
            <p>Ask about Singapore regulations</p>
          </div>
        </div>
        <div class="chat-messages" id="chatMessages">
          <div class="chat-msg chat-msg--bot">
            Hi! I can help you with questions about Singapore company compliance, ACRA requirements, tax obligations, and VCC regulations. What would you like to know?
          </div>
        </div>
        <form class="chat-input" id="chatForm">
          <input type="text" id="chatInput" placeholder="e.g. When must I file Annual Return?" autocomplete="off" />
          <button type="submit" id="chatSend">
            <svg viewBox="0 0 24 24"><path d="M22 2L11 13"/><path d="M22 2L15 22L11 13L2 9L22 2Z"/></svg>
          </button>
        </form>
        <div class="chat-disclaimer">General information only — not legal advice</div>
      </div>
      <button class="chat-toggle" id="chatToggle">
        <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
      </button>
    `;
    document.body.appendChild(widget);

    panel = document.getElementById("chatPanel");
    messages = document.getElementById("chatMessages");
    input = document.getElementById("chatInput");
    sendBtn = document.getElementById("chatSend");
    toggleBtn = document.getElementById("chatToggle");

    toggleBtn.addEventListener("click", toggle);
    document.getElementById("chatForm").addEventListener("submit", onSubmit);
  }

  // ── Toggle ──
  function toggle() {
    isOpen = !isOpen;
    panel.classList.toggle("chat-panel--open", isOpen);

    if (isOpen) {
      toggleBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>';
      toggleBtn.classList.add("chat-toggle--close");
      input.focus();
    } else {
      toggleBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>';
      toggleBtn.classList.remove("chat-toggle--close");
    }
  }

  // ── Submit ──
  function onSubmit(e) {
    e.preventDefault();
    const question = input.value.trim();
    if (!question || isLoading) return;

    addMessage(question, "user");
    input.value = "";
    sendQuestion(question);
  }

  // ── Add message bubble ──
  function addMessage(text, role) {
    const div = document.createElement("div");
    div.className = `chat-msg chat-msg--${role}`;
    if (role === "bot") {
      div.innerHTML = formatMarkdown(text);
    } else {
      div.textContent = text;
    }
    messages.appendChild(div);
    scrollToBottom();
    return div;
  }

  // ── Typing indicator ──
  function showTyping() {
    const div = document.createElement("div");
    div.className = "chat-typing";
    div.id = "chatTyping";
    div.innerHTML = "<span></span><span></span><span></span>";
    messages.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    const el = document.getElementById("chatTyping");
    if (el) el.remove();
  }

  // ── Send question via SSE ──
  async function sendQuestion(question) {
    isLoading = true;
    sendBtn.disabled = true;
    showTyping();

    let botMsg = null;
    let fullText = "";
    let sources = [];

    try {
      const resp = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!resp.ok) {
        throw new Error(`Server error: ${resp.status}`);
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop(); // keep incomplete line in buffer

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;

          const data = JSON.parse(line.slice(6));

          if (data.type === "chunk") {
            hideTyping();
            fullText += data.text;
            if (!botMsg) {
              botMsg = addMessage(fullText, "bot");
            } else {
              botMsg.innerHTML = formatMarkdown(fullText);
            }
            scrollToBottom();
          }

          if (data.type === "sources") {
            sources = data.sources || [];
          }

          if (data.type === "done" && sources.length > 0 && botMsg) {
            appendSources(botMsg, sources);
          }
        }
      }
    } catch (err) {
      hideTyping();
      addMessage("Sorry, something went wrong. Please try again.", "bot");
      console.error("Chat error:", err);
    } finally {
      isLoading = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  // ── Append sources to a message ──
  function appendSources(msgEl, sources) {
    const div = document.createElement("div");
    div.className = "chat-sources";
    div.innerHTML = `<div class="chat-sources__label">Sources</div>` +
      sources.map(s => `<div class="chat-sources__item">${s.name}</div>`).join("");
    msgEl.appendChild(div);
    scrollToBottom();
  }

  // ── Simple markdown formatting ──
  function formatMarkdown(text) {
    return text
      // Bold
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      // Inline code
      .replace(/`(.*?)`/g, "<code>$1</code>")
      // Bullet lists
      .replace(/^[-*] (.+)$/gm, "<li>$1</li>")
      .replace(/(<li>.*<\/li>\n?)+/gs, "<ul>$&</ul>")
      // Numbered lists
      .replace(/^\d+\. (.+)$/gm, "<li>$1</li>")
      // Paragraphs (double newline)
      .replace(/\n\n/g, "</p><p>")
      // Single newlines within paragraphs
      .replace(/\n/g, "<br>")
      // Wrap in paragraph
      .replace(/^(.+)$/s, "<p>$1</p>")
      // Clean up empty paragraphs
      .replace(/<p>\s*<\/p>/g, "");
  }

  // ── Scroll ──
  function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  // ── Init ──
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
