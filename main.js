(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- NAV: scrolled state ---------- */
  var nav = document.querySelector(".nav");
  var lastY = -1;
  function onScrollNav() {
    var y = window.scrollY || window.pageYOffset;
    if (y === lastY) return;
    lastY = y;
    if (nav) nav.classList.toggle("is-scrolled", y > 12);
  }
  window.addEventListener("scroll", onScrollNav, { passive: true });
  onScrollNav();

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector(".nav-burger");
  var menu = document.querySelector(".mobile-menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = burger.classList.toggle("is-open");
      menu.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        burger.classList.remove("is-open");
        menu.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".rv, .rv-stagger");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  function clamp01(v) { return Math.min(Math.max(v, 0), 1); }
  function easeOut(t) { return 1 - Math.pow(1 - t, 2); }

  /* ---------- HERO SEQUENCE: scroll-pinned transition (typography + data viz) ---------- */
  var heroSeq = document.querySelector("[data-hero-sequence]");
  var heroCopy = document.querySelector("[data-hero-copy]");
  var heroViz = document.querySelector("[data-hero-viz]");
  var heroTicking = false;

  if (heroSeq && !reduceMotion) {
    function updateHero() {
      var rect = heroSeq.getBoundingClientRect();
      var extra = rect.height - window.innerHeight;
      var progress = extra > 0 ? clamp01(-rect.top / extra) : 0;
      var eased = easeOut(progress);

      if (heroCopy) {
        heroCopy.style.transform = "translateY(" + (-30 * eased) + "px)";
        heroCopy.style.opacity = String(1 - clamp01(progress * 1.3));
      }
      if (heroViz) {
        var scale = 1 - 0.22 * eased;
        var rotate = 8 * eased;
        heroViz.style.transform = "scale(" + scale + ") rotate(" + rotate + "deg)";
        heroViz.style.opacity = String(1 - clamp01(progress * 1.1));
      }
      heroTicking = false;
    }
    window.addEventListener("scroll", function () {
      if (!heroTicking) { requestAnimationFrame(updateHero); heroTicking = true; }
    }, { passive: true });
    window.addEventListener("resize", function () {
      if (!heroTicking) { requestAnimationFrame(updateHero); heroTicking = true; }
    });
    updateHero();
  }

  /* ---------- Flow-chain: scroll-reactive line fill ---------- */
  var flowFills = document.querySelectorAll("[data-flow-fill]");
  var flowTicking = false;
  if (flowFills.length && !reduceMotion) {
    function updateFlows() {
      flowFills.forEach(function (el) {
        var rect = el.getBoundingClientRect();
        var vh = window.innerHeight;
        // progress: 0 when element bottom hits 78% viewport height, 1 when element top hits 32% viewport height
        var start = vh * 0.82;
        var end = vh * 0.32;
        var t = (start - rect.top) / (start - end);
        el.style.setProperty("--fill", String(clamp01(t)));
      });
      flowTicking = false;
    }
    window.addEventListener("scroll", function () {
      if (!flowTicking) { requestAnimationFrame(updateFlows); flowTicking = true; }
    }, { passive: true });
    window.addEventListener("resize", function () {
      if (!flowTicking) { requestAnimationFrame(updateFlows); flowTicking = true; }
    });
    updateFlows();
  } else if (flowFills.length) {
    flowFills.forEach(function (el) { el.style.setProperty("--fill", "1"); });
  }

  /* ---------- Draggable exploration canvas (project 02) with inertia ---------- */
  document.querySelectorAll("[data-drag-canvas]").forEach(function (wrap) {
    var isDown = false;
    var startX = 0;
    var startScroll = 0;
    var moved = false;
    var lastX = 0;
    var lastT = 0;
    var velocity = 0;
    var momentumId = null;

    function stopMomentum() {
      if (momentumId) { cancelAnimationFrame(momentumId); momentumId = null; }
    }
    function down(x) {
      stopMomentum();
      isDown = true; moved = false;
      wrap.classList.add("is-dragging");
      startX = x; startScroll = wrap.scrollLeft;
      lastX = x; lastT = performance.now(); velocity = 0;
    }
    function move(x) {
      if (!isDown) return;
      var dx = x - startX;
      if (Math.abs(dx) > 4) moved = true;
      wrap.scrollLeft = startScroll - dx;
      var now = performance.now();
      var dt = now - lastT;
      if (dt > 0) { velocity = (x - lastX) / dt; lastX = x; lastT = now; }
    }
    function up() {
      if (!isDown) return;
      isDown = false;
      wrap.classList.remove("is-dragging");
      var v = -velocity * 16;
      function step() {
        if (Math.abs(v) < 0.5) { momentumId = null; return; }
        wrap.scrollLeft += v;
        v *= 0.92;
        momentumId = requestAnimationFrame(step);
      }
      if (Math.abs(v) > 0.5) momentumId = requestAnimationFrame(step);
    }

    wrap.addEventListener("mousedown", function (e) { down(e.pageX); });
    window.addEventListener("mouseup", up);
    window.addEventListener("mousemove", function (e) {
      if (!isDown) return;
      e.preventDefault();
      move(e.pageX);
    });
    wrap.addEventListener("touchstart", function (e) { down(e.touches[0].pageX); }, { passive: true });
    wrap.addEventListener("touchmove", function (e) { move(e.touches[0].pageX); }, { passive: true });
    wrap.addEventListener("touchend", up);
    wrap.addEventListener("click", function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); }
    }, true);
  });
})();
