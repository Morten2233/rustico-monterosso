(function () {
  var bar = document.getElementById("bar");
  function onScroll() { bar.classList.toggle("solid", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Hintergrund-Video: hochkant auf Handy, quer auf breiten Bildschirmen
  var bg = document.getElementById("bgvideo");
  var tallMq = window.matchMedia("(max-aspect-ratio: 1/1)");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function videoSrc() { return tallMq.matches ? bg.dataset.tall : bg.dataset.wide; }
  function loadBg() {
    bg.poster = bg.poster.replace(/poster-(quer|hoch)/, tallMq.matches ? "poster-hoch" : "poster-quer");
    if (reduce) return;
    bg.src = videoSrc();
    bg.play().catch(function () {});
  }
  loadBg();
  tallMq.addEventListener("change", loadBg);

  // Modals
  var openModal = null;
  function show(m) { m.hidden = false; openModal = m; document.body.style.overflow = "hidden"; }
  function hide() {
    if (!openModal) return;
    var v = openModal.querySelector("video");
    if (v) v.pause();
    openModal.hidden = true; openModal = null; document.body.style.overflow = "";
  }
  document.querySelectorAll(".modal").forEach(function (m) {
    m.addEventListener("click", function (e) {
      if (e.target === m || e.target.hasAttribute("data-close")) hide();
    });
  });

  var vm = document.getElementById("videoModal");
  var mv = document.getElementById("modalVideo");
  document.getElementById("soundBtn").addEventListener("click", function () {
    mv.src = tallMq.matches ? bg.dataset.soundTall : bg.dataset.soundWide;
    show(vm);
    mv.play().catch(function () {});
  });

  // Lightbox
  var lb = document.getElementById("lightbox");
  var lbImg = document.getElementById("lbImg");
  var lbCap = document.getElementById("lbCap");
  var idx = 0;
  function render() {
    var p = window.PHOTOS[idx];
    lbImg.src = p.src; lbImg.alt = p.alt;
    lbCap.textContent = (idx + 1) + " / " + window.PHOTOS.length + " · " + p.alt;
  }
  function go(d) { idx = (idx + d + window.PHOTOS.length) % window.PHOTOS.length; render(); }
  document.querySelectorAll(".tile").forEach(function (t) {
    t.addEventListener("click", function () { idx = Number(t.dataset.i); render(); show(lb); });
  });
  lb.querySelector(".prev").addEventListener("click", function (e) { e.stopPropagation(); go(-1); });
  lb.querySelector(".next").addEventListener("click", function (e) { e.stopPropagation(); go(1); });
  lbImg.addEventListener("click", function (e) { e.stopPropagation(); });
  var sx = null;
  lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1);
  });
  document.addEventListener("keydown", function (e) {
    if (!openModal) return;
    if (e.key === "Escape") hide();
    if (openModal === lb && e.key === "ArrowRight") go(1);
    if (openModal === lb && e.key === "ArrowLeft") go(-1);
  });

  // Anfrageformular
  var form = document.getElementById("form");
  var err = document.getElementById("formErr");
  var ok = document.getElementById("formOk");
  var lbl = form.querySelector(".lbl");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    err.hidden = true;
    if (!form.checkValidity()) { err.hidden = false; form.reportValidity(); return; }
    var f = new FormData(form);
    if (f.get("_honey")) return;
    form.classList.add("sending");
    lbl.textContent = lbl.dataset.sending;
    fetch(window.FORM_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        _subject: "Anfrage Rustico Monterosso von " + f.get("name"),
        _template: "table",
        _captcha: "false",
        _replyto: f.get("email"),
        Name: f.get("name"),
        email: f.get("email"),
        Telefon: f.get("phone"),
        Nachricht: f.get("message"),
        Sprache: window.LANG
      })
    })
      .then(function (r) { return r.json().then(function (j) { return r.ok && String(j.success) === "true"; }); })
      .then(function (good) {
        form.classList.remove("sending");
        if (good) { form.classList.add("done"); ok.hidden = false; }
        else { err.hidden = false; lbl.textContent = lbl.dataset.send; }
      })
      .catch(function () {
        form.classList.remove("sending");
        err.hidden = false; lbl.textContent = lbl.dataset.send;
      });
  });
})();
