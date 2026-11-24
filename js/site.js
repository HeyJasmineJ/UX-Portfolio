(function () {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", () => {
      const open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  const CONTACT = "jasminejwilson1@gmail.com";
  const form = document.querySelector("form[data-contact]");
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("name") || "").trim();
      const email = String(data.get("email") || "").trim();
      const message = String(data.get("message") || "").trim();
      const subject = name ? `Portfolio — ${name}` : "Portfolio";
      const lines = [];
      if (message) lines.push(message);
      if (name || email) lines.push("", "—", [name, email].filter(Boolean).join(" · "));
      window.location.href =
        `mailto:${CONTACT}?subject=${encodeURIComponent(subject)}` +
        `&body=${encodeURIComponent(lines.join("\n"))}`;
    });
  }

  const figures = [...document.querySelectorAll(".gallery img")];
  if (!figures.length) return;

  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = '<button type="button" aria-label="Close">Close</button><img alt="">';
  document.body.appendChild(overlay);
  const picture = overlay.querySelector("img");
  const close = overlay.querySelector("button");

  function hide() {
    overlay.classList.remove("is-open");
  }

  figures.forEach((img) => {
    img.addEventListener("click", () => {
      picture.src = img.currentSrc || img.src;
      picture.alt = img.alt || "";
      overlay.classList.add("is-open");
    });
  });
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) hide();
  });
  close.addEventListener("click", hide);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") hide();
  });
})();
