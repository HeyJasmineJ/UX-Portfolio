(function () {
  function revealStuck() {
    const nodes = document.querySelectorAll("#main [style], [data-framer-appear-id]");
    for (const el of nodes) {
      const style = el.getAttribute("style") || "";
      if (el.closest('[data-framer-name="Overlay"]')) continue;
      if (!/opacity\s*:\s*0(\.0+1)?/i.test(style) && !el.hasAttribute("data-framer-appear-id")) {
        continue;
      }
      const opacity = parseFloat(getComputedStyle(el).opacity);
      if (opacity >= 0.05) continue;
      const hasContent =
        (el.innerText && el.innerText.trim().length > 0) ||
        el.querySelector("img, video, svg, p, h1, h2, h3, h4, h5, h6");
      if (!hasContent) continue;
      el.style.setProperty("opacity", "1", "important");
      el.style.setProperty("transform", "none", "important");
      el.style.setProperty("filter", "none", "important");
    }
  }

  window.__framer_disable_appear_effects_optimization__ = true;
  revealStuck();
  document.addEventListener("scroll", revealStuck, { passive: true, capture: true });
  window.addEventListener("load", revealStuck);
  setTimeout(revealStuck, 200);
  setTimeout(revealStuck, 800);
  setTimeout(revealStuck, 2000);

  const CONTACT_EMAIL = "jasminejwilson1@gmail.com";

  function fieldValue(form, names) {
    for (const name of names) {
      const field = form.querySelector(`[name="${name}"]`);
      if (field && field.value.trim()) return field.value.trim();
    }
    return "";
  }

  function setupContactMailto() {
    document.querySelectorAll("form.framer-xe58m4").forEach((form) => {
      form.setAttribute("action", `mailto:${CONTACT_EMAIL}`);
      form.setAttribute("method", "get");
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const name = fieldValue(form, ["Name", "name"]);
        const email = fieldValue(form, ["Email", "email"]);
        const message = fieldValue(form, ["Message", "message"]);
        const subject = name ? `Portfolio — ${name}` : "Portfolio";
        const lines = [];
        if (message) lines.push(message);
        if (name || email) lines.push("", "—", [name, email].filter(Boolean).join(" · "));
        const href =
          `mailto:${CONTACT_EMAIL}` +
          `?subject=${encodeURIComponent(subject)}` +
          `&body=${encodeURIComponent(lines.join("\n"))}`;
        window.location.href = href;
      });
    });

    document.querySelectorAll('a[href^="mailto:"]').forEach((link) => {
      link.href = link.href.replace(/^mailto:\s+/, "mailto:");
    });

    document.querySelectorAll("form[method='POST']").forEach((form) => {
      if (form.classList.contains("framer-xe58m4")) return;
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const email = fieldValue(form, ["email", "Email"]);
        const subject = "Portfolio notes";
        const body = email
          ? `Please add ${email} to occasional notes.`
          : "Please add me to occasional notes.";
        window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      });
    });
  }

  function isProjectCaseStudy() {
    return /\/project\/[^/]+/.test(location.pathname);
  }

  function visibleImages() {
    return [...document.querySelectorAll("#main img")].filter((img) => {
      if (img.closest(".jw-lightbox")) return false;
      const width = img.naturalWidth || Number(img.getAttribute("width") || 0);
      const height = img.naturalHeight || Number(img.getAttribute("height") || 0);
      if (width < 200 || height < 140) return false;
      const rects = img.getClientRects();
      return rects.length > 0 && rects[0].width > 80 && rects[0].height > 80;
    });
  }

  function uniqueGallery(images) {
    const seen = new Set();
    const gallery = [];
    for (const img of images) {
      const key = (img.currentSrc || img.src).split("?")[0];
      if (seen.has(key)) continue;
      seen.add(key);
      gallery.push(img);
    }
    return gallery;
  }

  function setupLightbox() {
    if (!isProjectCaseStudy()) return;

    const overlay = document.createElement("div");
    overlay.className = "jw-lightbox";
    overlay.setAttribute("hidden", "");
    overlay.innerHTML = `
      <button type="button" class="jw-lightbox-close" aria-label="Close">×</button>
      <button type="button" class="jw-lightbox-prev" aria-label="Previous image">‹</button>
      <img alt="">
      <button type="button" class="jw-lightbox-next" aria-label="Next image">›</button>
    `;
    document.body.appendChild(overlay);

    const picture = overlay.querySelector("img");
    const closeBtn = overlay.querySelector(".jw-lightbox-close");
    const prevBtn = overlay.querySelector(".jw-lightbox-prev");
    const nextBtn = overlay.querySelector(".jw-lightbox-next");
    let gallery = [];
    let index = 0;

    function show(nextIndex) {
      gallery = uniqueGallery(visibleImages());
      if (!gallery.length) return;
      index = (nextIndex + gallery.length) % gallery.length;
      const source = gallery[index];
      picture.src = source.currentSrc || source.src;
      picture.alt = source.alt || "Project image";
      overlay.classList.add("is-open");
      overlay.removeAttribute("hidden");
      document.body.style.overflow = "hidden";
    }

    function hide() {
      overlay.classList.remove("is-open");
      overlay.setAttribute("hidden", "");
      document.body.style.overflow = "";
    }

    function markHits() {
      visibleImages().forEach((img) => img.classList.add("jw-lightbox-hit"));
    }

    document.addEventListener("click", (event) => {
      const img = event.target.closest("#main img");
      if (!img || img.closest(".jw-lightbox")) return;
      const images = uniqueGallery(visibleImages());
      const key = (img.currentSrc || img.src).split("?")[0];
      const nextIndex = images.findIndex((item) => (item.currentSrc || item.src).split("?")[0] === key);
      if (nextIndex === -1) return;
      event.preventDefault();
      event.stopPropagation();
      show(nextIndex);
    }, true);

    markHits();
    window.addEventListener("load", markHits);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) hide();
    });
    closeBtn.addEventListener("click", hide);
    prevBtn.addEventListener("click", () => show(index - 1));
    nextBtn.addEventListener("click", () => show(index + 1));
    document.addEventListener("keydown", (event) => {
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") hide();
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      setupContactMailto();
      setupLightbox();
    });
  } else {
    setupContactMailto();
    setupLightbox();
  }
})();
