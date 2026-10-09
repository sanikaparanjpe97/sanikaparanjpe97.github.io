// Header border on scroll + a small lightbox for portfolio plates and photos.
(() => {
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const links = [...document.querySelectorAll("a[data-lightbox]")];
  if (!links.length || typeof HTMLDialogElement !== "function") return;

  const dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.setAttribute("aria-label", "Image viewer");
  dlg.innerHTML = `
    <div class="lb-bar">
      <span class="lb-count" aria-live="polite"></span>
      <div class="lb-tools">
        <button class="lb-btn lb-zoom" type="button" aria-label="Zoom to full size" title="Zoom (Z)">+</button>
        <button class="lb-btn lb-close" type="button" aria-label="Close" title="Close (Esc)">✕</button>
      </div>
    </div>
    <div class="lb-stage">
      <button class="lb-btn lb-prev" type="button" aria-label="Previous image">←</button>
      <img alt="">
      <button class="lb-btn lb-next" type="button" aria-label="Next image">→</button>
    </div>
    <p class="lb-caption"></p>`;
  document.body.append(dlg);

  const img = dlg.querySelector("img");
  const stage = dlg.querySelector(".lb-stage");
  const count = dlg.querySelector(".lb-count");
  const caption = dlg.querySelector(".lb-caption");
  const zoomBtn = dlg.querySelector(".lb-zoom");
  let index = 0;
  let opener = null;

  const setZoom = (on, clientX, clientY) => {
    const rect = img.getBoundingClientRect();
    const fx = clientX != null ? (clientX - rect.left) / rect.width : 0.5;
    const fy = clientY != null ? (clientY - rect.top) / rect.height : 0.5;
    dlg.classList.toggle("zoomed", on);
    zoomBtn.textContent = on ? "−" : "+";
    zoomBtn.setAttribute("aria-label", on ? "Fit to screen" : "Zoom to full size");
    if (on) {
      stage.scrollLeft = img.offsetWidth * fx - stage.clientWidth / 2;
      stage.scrollTop = img.offsetHeight * fy - stage.clientHeight / 2;
    }
  };

  const preload = (i) => {
    const l = links[(i + links.length) % links.length];
    if (l) new Image().src = l.href;
  };

  const show = (i) => {
    index = (i + links.length) % links.length;
    const link = links[index];
    const thumb = link.querySelector("img");
    setZoom(false);
    img.src = link.href;
    img.alt = thumb ? thumb.alt : "";
    caption.textContent = link.dataset.caption || "";
    count.textContent = `${index + 1} / ${links.length}`;
    preload(index + 1);
    preload(index - 1);
  };

  links.forEach((link, i) => {
    link.addEventListener("click", (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      opener = link;
      show(i);
      dlg.showModal();
      document.documentElement.style.overflow = "hidden";
    });
  });

  dlg.addEventListener("close", () => {
    document.documentElement.style.overflow = "";
    img.removeAttribute("src");
    if (opener) opener.focus({ preventScroll: true });
  });

  dlg.querySelector(".lb-close").addEventListener("click", () => dlg.close());
  dlg.querySelector(".lb-prev").addEventListener("click", () => show(index - 1));
  dlg.querySelector(".lb-next").addEventListener("click", () => show(index + 1));
  zoomBtn.addEventListener("click", () => setZoom(!dlg.classList.contains("zoomed")));
  img.addEventListener("click", (e) => setZoom(!dlg.classList.contains("zoomed"), e.clientX, e.clientY));
  stage.addEventListener("click", (e) => { if (e.target === stage) dlg.close(); });

  dlg.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") show(index + 1);
    else if (e.key === "ArrowLeft") show(index - 1);
    else if (e.key === "z" || e.key === "Z") setZoom(!dlg.classList.contains("zoomed"));
  });

  // Swipe between images when not zoomed.
  let startX = null;
  stage.addEventListener("touchstart", (e) => { startX = e.touches.length === 1 ? e.touches[0].clientX : null; }, { passive: true });
  stage.addEventListener("touchend", (e) => {
    if (startX == null || dlg.classList.contains("zoomed")) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    startX = null;
  });
})();
