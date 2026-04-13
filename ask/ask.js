/* ─────────────────────────────────────────────
   KARMAN — Ask AI  (full-page chat)
───────────────────────────────────────────── */

(function () {
  const API_URL = "https://karman-rag-production.up.railway.app";
  const MAX_FREE_QUERIES = 5;
  const STORAGE_KEY = "karman_ask_queries";
  const UNLOCKED_KEY = "karman_ask_unlocked";

  // DOM
  const main      = document.getElementById("askMain");
  const empty     = document.getElementById("askEmpty");
  const msgWrap   = document.getElementById("askMessages");
  const form      = document.getElementById("askForm");
  const input     = document.getElementById("askInput");
  const sendBtn   = document.getElementById("askSend");
  const newBtn    = document.getElementById("newChatBtn");
  const suggestions = document.getElementById("suggestions");

  let isLoading = false;

  // ── Query counter ──
  function getQueryCount() {
    return parseInt(localStorage.getItem(STORAGE_KEY) || "0", 10);
  }

  function incrementQueryCount() {
    const count = getQueryCount() + 1;
    localStorage.setItem(STORAGE_KEY, count);
    return count;
  }

  function isUnlocked() {
    return localStorage.getItem(UNLOCKED_KEY) === "true";
  }

  function hasReachedLimit() {
    return !isUnlocked() && getQueryCount() >= MAX_FREE_QUERIES;
  }

  // ── Lead capture modal ──
  function showLeadModal() {
    if (document.getElementById("askLeadModal")) return;

    const overlay = document.createElement("div");
    overlay.id = "askLeadModal";
    overlay.className = "ask-modal-overlay";
    overlay.innerHTML = `
      <div class="ask-modal">
        <div class="ask-modal__icon">K</div>
        <h2>You've used all 5 free queries</h2>
        <p>Share your details and we'll unlock unlimited access to the Compliance Assistant.</p>
        <form class="ask-modal__form" id="leadForm">
          <div class="ask-modal__row">
            <div class="ask-modal__field">
              <label>Name <span>*</span></label>
              <input type="text" name="name" placeholder="Jane Smith" required />
            </div>
            <div class="ask-modal__field">
              <label>Company name</label>
              <input type="text" name="company" placeholder="Acme Pte. Ltd." />
            </div>
          </div>
          <div class="ask-modal__field">
            <label>Email <span>*</span></label>
            <input type="email" name="email" placeholder="jane@company.com" required />
          </div>
          <div class="ask-modal__field">
            <label>Phone</label>
            <input type="tel" name="phone" placeholder="+65 9123 4567" />
          </div>
          <button type="submit" class="ask-modal__submit">Unlock unlimited access</button>
        </form>
        <button class="ask-modal__close" id="closeModal">&times;</button>
      </div>
    `;
    document.body.appendChild(overlay);

    document.getElementById("closeModal").addEventListener("click", () => overlay.remove());
    overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });

    document.getElementById("leadForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = Object.fromEntries(formData);
      const submitBtn = e.target.querySelector("button[type=submit]");
      submitBtn.textContent = "Submitting...";
      submitBtn.disabled = true;

      try {
        await fetch(`${API_URL}/api/feedback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ type: "lead", ...data }),
        });
      } catch (err) {
        // Still unlock even if API fails
      }

      localStorage.setItem(UNLOCKED_KEY, "true");
      overlay.remove();
      input.focus();
    });
  }

  // ── Auto-resize textarea ──
  input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 150) + "px";
    sendBtn.disabled = !input.value.trim();
  });

  // ── Submit on Enter (Shift+Enter for newline) ──
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.value.trim() && !isLoading) form.dispatchEvent(new Event("submit"));
    }
  });

  // ── Form submit ──
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q || isLoading) return;

    if (hasReachedLimit()) {
      showLeadModal();
      return;
    }

    ask(q);
  });

  // ── Suggestion clicks ──
  suggestions.addEventListener("click", (e) => {
    const btn = e.target.closest(".ask-suggestion");
    if (!btn) return;

    if (hasReachedLimit()) {
      showLeadModal();
      return;
    }

    ask(btn.dataset.q);
  });

  // ── New chat ──
  newBtn.addEventListener("click", () => {
    msgWrap.innerHTML = "";
    msgWrap.style.display = "none";
    empty.style.display = "";
    input.value = "";
    input.style.height = "auto";
    sendBtn.disabled = true;
    input.focus();
  });

  // ── Ask ──
  function ask(question) {
    empty.style.display = "none";
    msgWrap.style.display = "flex";

    addRow(question, "user");
    input.value = "";
    input.style.height = "auto";
    sendBtn.disabled = true;

    incrementQueryCount();
    sendQuestion(question);
  }

  // ── Add a message row ──
  function addRow(text, role) {
    const row = document.createElement("div");
    row.className = `ask-row ask-row--${role}`;

    const avatarLabel = role === "user" ? "Y" : "K";
    row.innerHTML = `
      <div class="ask-row__inner">
        <div class="ask-avatar ask-avatar--${role}">${avatarLabel}</div>
        <div class="ask-content">${role === "user" ? escapeHtml(text) : text}</div>
      </div>
    `;
    msgWrap.appendChild(row);
    scrollToBottom();
    return row;
  }

  // ── Streaming request ──
  async function sendQuestion(question) {
    isLoading = true;
    sendBtn.disabled = true;

    const botRow = addRow("", "bot");
    const content = botRow.querySelector(".ask-content");
    content.innerHTML = '<div class="ask-typing"><span></span><span></span><span></span></div>';

    let fullText = "";
    let sources = [];

    try {
      const resp = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!resp.ok) throw new Error(`Server error: ${resp.status}`);

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let firstChunk = true;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;

          let data;
          try { data = JSON.parse(line.slice(6)); }
          catch { continue; }

          if (data.type === "chunk") {
            if (firstChunk) {
              content.innerHTML = "";
              firstChunk = false;
            }
            fullText += data.text;
            content.innerHTML = formatMarkdown(fullText);
            content.classList.add("ask-cursor");
            scrollToBottom();
          }

          if (data.type === "sources") {
            sources = data.sources || [];
          }

          if (data.type === "done") {
            content.classList.remove("ask-cursor");
            if (sources.length > 0) {
              appendSources(content, sources);
            }
          }
        }
      }
    } catch (err) {
      content.innerHTML = '<p>Sorry, something went wrong. Please try again.</p>';
      console.error("Chat error:", err);
    } finally {
      isLoading = false;
      sendBtn.disabled = !input.value.trim();
      input.focus();
    }
  }

  // ── Append sources with clickable links ──
  function appendSources(el, sources) {
    const div = document.createElement("div");
    div.className = "ask-sources";
    const items = sources.map(s => {
      const label = s.name.replace(".md", "").replace(/-/g, " ");
      if (s.url) {
        return `<a href="${escapeHtml(s.url)}" target="_blank" rel="noopener" class="ask-sources__item">${escapeHtml(label)}</a>`;
      }
      return `<span class="ask-sources__item">${escapeHtml(label)}</span>`;
    }).join("");
    div.innerHTML = '<div class="ask-sources__label">Sources</div>' + items;
    el.appendChild(div);
    scrollToBottom();
  }

  // ── Markdown formatting ──
  function formatMarkdown(text) {
    return text
      .replace(/^#### (.+)$/gm, "<h4>$1</h4>")
      .replace(/^### (.+)$/gm, "<h3>$1</h3>")
      .replace(/^## (.+)$/gm, "<h2>$1</h2>")
      .replace(/^---$/gm, "<hr>")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/`(.*?)`/g, "<code>$1</code>")
      .replace(/^> (.+)$/gm, "<blockquote>$1</blockquote>")
      .replace(/^\|(.+)\|$/gm, (match) => {
        const cells = match.split("|").filter(c => c.trim());
        if (cells.every(c => /^[\s-:]+$/.test(c))) return "<!--sep-->";
        return cells.map(c => `<td>${c.trim()}</td>`).join("");
      })
      .replace(/((<td>.*<\/td>\n?)+)/g, (match) => {
        const rows = match.trim().split("\n").filter(r => r && !r.includes("<!--sep-->"));
        if (rows.length === 0) return "";
        const header = `<tr>${rows[0].replace(/<td>/g, "<th>").replace(/<\/td>/g, "</th>")}</tr>`;
        const body = rows.slice(1).map(r => `<tr>${r}</tr>`).join("");
        return `<table><thead>${header}</thead><tbody>${body}</tbody></table>`;
      })
      .replace(/^[-*] (.+)$/gm, "<li>$1</li>")
      .replace(/(<li>.*<\/li>\n?)+/gs, "<ul>$&</ul>")
      .replace(/^\d+\. (.+)$/gm, "<li>$1</li>")
      .replace(/\n\n/g, "</p><p>")
      .replace(/\n/g, "<br>")
      .replace(/^(.+)$/s, "<p>$1</p>")
      .replace(/<p>\s*<\/p>/g, "")
      .replace(/<p><(h[234]|ul|ol|table|blockquote|hr)/g, "<$1")
      .replace(/<\/(h[234]|ul|ol|table|blockquote)><\/p>/g, "</$1>")
      .replace(/<hr><\/p>/g, "<hr>")
      .replace(/<!--sep-->/g, "");
  }

  // ── Helpers ──
  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function scrollToBottom() {
    main.scrollTop = main.scrollHeight;
  }

  // ── Init ──
  msgWrap.style.display = "none";
  input.focus();
})();
