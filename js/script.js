/* =========================================================
   Ha Giang With Matt — script.js
   Vanilla only. Every feature degrades to working HTML.
   ========================================================= */

(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var isReduced = function () { return reduced.matches; };


  /* ---------- 1. Sticky header ---------- */

  var header = document.querySelector('[data-nav]');

  if (header) {
    var lastState = false;
    var onScroll = function () {
      var scrolled = window.scrollY > 40;
      if (scrolled !== lastState) {
        header.toggleAttribute('data-scrolled', scrolled);
        lastState = scrolled;
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }


  /* ---------- 2. Mobile navigation ---------- */

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');

  if (toggle && nav) {
    var setNav = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.toggleAttribute('data-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };

    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setNav(false);
        toggle.focus();
      }
    });

    // Leaving the mobile breakpoint should never strand the menu open
    var wide = window.matchMedia('(min-width: 62em)');
    var onBreak = function (e) { if (e.matches) setNav(false); };
    wide.addEventListener ? wide.addEventListener('change', onBreak) : wide.addListener(onBreak);
  }


  /* ---------- 2b. Hero entrance sequence ---------- */

  var heroEl = document.querySelector('.hero');

  if (heroEl) {
    // Split the lede into words so they can arrive one after another.
    // Done in JS so the HTML stays a clean, readable paragraph for crawlers.
    var typeset = heroEl.querySelector('[data-typeset]');
    var wordCount = 0;

    if (typeset && !isReduced()) {
      var words = typeset.textContent.trim().split(/\s+/);
      wordCount = words.length;
      typeset.textContent = '';
      words.forEach(function (w, i) {
        var span = document.createElement('span');
        span.className = 'word';
        span.textContent = w;
        span.style.setProperty('--wd', (780 + i * 34) + 'ms');
        typeset.appendChild(span);
        if (i < words.length - 1) typeset.appendChild(document.createTextNode(' '));
      });
    }

    // The buttons wait until the sentence has finished writing itself
    var afterWords = 780 + wordCount * 34 + 200;

    var beats = [
      ['.hero__eyebrow', 100],
      ['.hero__line:nth-child(1) > span', 220],
      ['.hero__line:nth-child(2) > span', 400],
      ['.hero__body', afterWords - 300],
      ['.hero__actions', afterWords],
      ['.sound', afterWords + 140],
      ['.hero__scroll', afterWords + 260]
    ];

    beats.forEach(function (pair) {
      var el = heroEl.querySelector(pair[0]);
      if (el) el.style.setProperty('--hd', (isReduced() ? 0 : pair[1]) + 'ms');
    });

    // Wait a frame so the delays are applied before the class lands
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { heroEl.classList.add('is-lit'); });
    });
  }


  /* ---------- 3. Motion: tag every element, animate section by section ---------- */

  // Anything in this list becomes its own animated step.
  var ANIMATABLE = [
    '.eyebrow', 'h1', 'h2', 'h3', 'h4',
    'p', 'blockquote', 'figure', 'img',
    'li', 'tr', 'caption',
    '.btn', '.channel', '.stat', '.price-cell',
    '.review', '.dayblock', '.reason', '.shot',
    '.field', '.note', '.pending'
  ].join(',');

  // Display headings get the mask wipe instead of the lift.
  var WIPE = ['.hero__title', '.page-hero__title', '.section-head__title',
              '.who__title', '.contact__title', '.trip__title', '.story__head'].join(',');

  var sectionList = document.querySelectorAll('main > section:not(.hero), main > nav, .contact, .site-footer');
  var sections = [];
  Array.prototype.forEach.call(sectionList, function (sec) {
    if (sections.indexOf(sec) === -1) sections.push(sec);
  });

  var tagSection = function (sec) {
    var found = sec.querySelectorAll(ANIMATABLE);
    var items = [];

    Array.prototype.forEach.call(found, function (el) {
      // Skip anything that sits inside an element we have already tagged,
      // otherwise the same text animates twice and looks broken.
      var parent = el.parentElement;
      while (parent && parent !== sec) {
        if (parent.hasAttribute('data-anim')) return;
        parent = parent.parentElement;
      }
      if (el.closest('[hidden]') || el.closest('[data-stream]') || el.closest('.tcard')) return;

      el.setAttribute('data-anim', el.matches(WIPE) ? 'wipe' : '');
      items.push(el);
    });

    // Sweep headings inherit the delay of the block they sit in
    Array.prototype.forEach.call(sec.querySelectorAll('[data-sweep]'), function (el) {
      var host = el.closest('[data-anim]');
      if (host) el.style.setProperty('--d', '260ms');
    });

    items.forEach(function (el, i) {
      // Ramp the gap down as the list grows so long sections do not crawl
      var step = i < 6 ? 70 : (i < 12 ? 45 : 28);
      el.style.setProperty('--d', Math.min(i * step, 900) + 'ms');
    });

    return items;
  };

  var showAll = function (items) {
    items.forEach(function (el) {
      var sec = el.closest('section');
      if (sec) sec.classList.add('is-open');
      el.classList.add('in');
      el.addEventListener('transitionend', function once(e) {
        if (e.propertyName !== 'transform' && e.propertyName !== 'clip-path') return;
        el.classList.add('settled');
        el.removeEventListener('transitionend', once);
      });
    });
  };

  if (isReduced() || !('IntersectionObserver' in window)) {
    sections.forEach(function (sec) { showAll(tagSection(sec)); });
  } else {
    var motion = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        showAll(entry.target._animItems || []);
        motion.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -4% 0px', threshold: 0.02 });

    sections.forEach(function (sec) {
      sec._animItems = tagSection(sec);
      motion.observe(sec);
    });
  }


  /* ---------- 3y. Tour cards: reveal, then count the price up ---------- */

  var cards = document.querySelectorAll('.tcard');

  if (cards.length) {
    var countUp = function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      var out = el.querySelector('span');
      if (!target || !out) return;

      if (isReduced()) { out.textContent = target; return; }

      var t0 = null;
      var dur = 900;
      var tick = function (now) {
        if (t0 === null) t0 = now;
        var p = Math.min((now - t0) / dur, 1);
        // Ease out so it slows into the real figure like a dial settling
        var eased = 1 - Math.pow(1 - p, 3);
        out.textContent = Math.round(target * eased);
        if (p < 1) requestAnimationFrame(tick);
        else out.textContent = target;
      };
      out.textContent = '0';
      requestAnimationFrame(tick);
    };

    var openCard = function (card) {
      card.classList.add('in');
      var prices = card.querySelectorAll('[data-count]');
      setTimeout(function () {
        Array.prototype.forEach.call(prices, countUp);
      }, isReduced() ? 0 : 260);
    };

    if (isReduced() || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(cards, openCard);
    } else {
      var cardObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry, i) {
          if (!entry.isIntersecting) return;
          setTimeout(function () { openCard(entry.target); }, i * 120);
          cardObs.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.15 });
      Array.prototype.forEach.call(cards, function (c) { cardObs.observe(c); });
    }
  }


  /* ---------- 3z. Long passages stream in paragraph by paragraph ---------- */

  var streams = document.querySelectorAll('[data-stream]');

  Array.prototype.forEach.call(streams, function (box) {
    var kids = box.children;
    Array.prototype.forEach.call(kids, function (el, i) {
      el.setAttribute('data-anim', el.matches('h1,h2,h3') ? 'wipe' : '');
      el.style.setProperty('--d', (i * 110) + 'ms');
    });
    if (isReduced() || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(kids, function (el) { el.classList.add('in'); });
      return;
    }
    new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        Array.prototype.forEach.call(kids, function (el) { el.classList.add('in'); });
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 }).observe(box);
  });


  /* ---------- 3a. Sub-navigation shadow once stuck ---------- */

  var subnav = document.querySelector('.subnav');
  if (subnav && 'IntersectionObserver' in window) {
    var sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;height:1px;width:1px;';
    subnav.parentNode.insertBefore(sentinel, subnav);
    new IntersectionObserver(function (entries) {
      subnav.toggleAttribute('data-stuck', !entries[0].isIntersecting);
    }, { rootMargin: '-70px 0px 0px 0px' }).observe(sentinel);
  }


  /* ---------- 3b. Reading progress ---------- */

  if (!isReduced()) {
    var bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);

    var barTick = false;
    var drawBar = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.scale = (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ' 1';
      barTick = false;
    };
    window.addEventListener('scroll', function () {
      if (!barTick) { barTick = true; requestAnimationFrame(drawBar); }
    }, { passive: true });
    drawBar();
  }


  /* ---------- 3c. Sub-navigation follows the scroll ---------- */

  var subLinks = document.querySelectorAll('.subnav a[href^="#"]');

  if (subLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    Array.prototype.forEach.call(subLinks, function (a) {
      byId[a.getAttribute('href').slice(1)] = a;
    });

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          Array.prototype.forEach.call(subLinks, function (a) { a.classList.remove('is-current'); });
          link.classList.add('is-current');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });

    Object.keys(byId).forEach(function (id) {
      var target = document.getElementById(id);
      if (target) spy.observe(target);
    });
  }


  /* ---------- 4. FAQ ---------- */

  // Nothing to wire: the FAQ is built on <details> with name="faq", so the
  // browser handles state, keyboard access and the exclusive-open behaviour.
  // The open/close animation is pure CSS on grid-template-rows.


  /* ---------- 4b. Gallery depth ---------- */

  var driftShots = document.querySelectorAll('.gallery-grid__item img');

  if (driftShots.length && !isReduced() && window.matchMedia('(min-width: 48em)').matches) {
    var driftTick = false;
    var drift = function () {
      Array.prototype.forEach.call(driftShots, function (img, i) {
        var box = img.parentElement.getBoundingClientRect();
        if (box.bottom < 0 || box.top > window.innerHeight) return;
        var p = (window.innerHeight / 2 - (box.top + box.height / 2)) / window.innerHeight;
        // Alternate the direction so the grid breathes instead of sliding as one
        var dir = i % 2 ? -1 : 1;
        img.style.transform = 'scale(1.08) translate3d(0,' + (p * 4 * dir).toFixed(2) + '%,0)';
      });
      driftTick = false;
    };
    window.addEventListener('scroll', function () {
      if (!driftTick) { driftTick = true; requestAnimationFrame(drift); }
    }, { passive: true });
    drift();
  }


  /* ---------- 5. Parallax ---------- */

  var parallax = document.querySelectorAll('[data-parallax] img');

  if (parallax.length && !isReduced() && window.matchMedia('(min-width: 62em)').matches) {
    Array.prototype.forEach.call(parallax, function (img) {
      img.style.willChange = 'transform';
      img.style.transform = 'scale(1.12)';
    });

    var ticking = false;

    var frame = function () {
      Array.prototype.forEach.call(parallax, function (img) {
        var box = img.parentElement.getBoundingClientRect();
        if (box.bottom < 0 || box.top > window.innerHeight) return;
        // -1 at the bottom of the screen, +1 at the top
        var progress = (window.innerHeight / 2 - (box.top + box.height / 2)) / window.innerHeight;
        img.style.transform = 'scale(1.12) translate3d(0,' + (progress * 5).toFixed(2) + '%,0)';
      });
      ticking = false;
    };

    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }, { passive: true });

    frame();
  }


  /* ---------- 6. Mobile CTA bar ---------- */

  var cta = document.querySelector('[data-mobile-cta]');
  var hero = document.querySelector('.hero');

  if (cta && hero && 'IntersectionObserver' in window) {
    cta.hidden = false;
    new IntersectionObserver(function (entries) {
      cta.toggleAttribute('data-visible', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(hero);
  } else if (cta) {
    cta.hidden = false;
    cta.setAttribute('data-visible', '');
  }


  /* ---------- 6b. Floating contact dock ---------- */

  var dock = document.querySelector('[data-dock]');
  var toTop = document.querySelector('[data-to-top]');

  if (dock) {
    var dockOn = false;
    var dockScroll = function () {
      var past = window.scrollY > window.innerHeight * 0.5;
      if (past !== dockOn) {
        dock.toggleAttribute('data-ready', past);
        dockOn = past;
      }
      if (toTop) toTop.hidden = window.scrollY < window.innerHeight * 1.5;
    };
    dockScroll();
    window.addEventListener('scroll', dockScroll, { passive: true });
  }

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: isReduced() ? 'auto' : 'smooth' });
      var skip = document.querySelector('.skip-link');
      if (skip) skip.focus({ preventScroll: true });
    });
  }


  /* ---------- 7. Images fade in as they decode ---------- */

  // Images are handled by the motion layer above; this only covers the rare
  // case of a photo that finishes decoding after its section already fired.
  Array.prototype.forEach.call(document.querySelectorAll('main img'), function (img) {
    if (isReduced() || (img.complete && img.naturalWidth)) return;
    img.addEventListener('load', function () {
      var box = img.closest('[data-anim]');
      if (box && !box.classList.contains('in')) box.classList.add('in');
    }, { once: true });
  });


  /* ---------- 8. Hero video and its sound toggle ---------- */

  var video = document.querySelector('[data-hero-video]');
  var soundBtn = document.querySelector('[data-sound]');

  if (video) {
    var conn = navigator.connection || {};
    var thrifty = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || '');
    var narrow = window.matchMedia('(max-width: 899px)').matches;

    // The video is content here, not decoration, so it is never removed —
    // on a slow line, with reduced motion, or on a narrow (likely mobile,
    // likely metered) connection we simply leave the poster showing and
    // never call play(), so preload="none" actually holds and nothing
    // downloads below 900px.
    if (thrifty || isReduced() || narrow) {
      video.removeAttribute('autoplay');
      video.preload = 'none';
    } else {
      var start = function () {
        var played = video.play();
        if (played && played.catch) {
          played.catch(function () { /* autoplay refused; poster stays, no error */ });
        }
      };
      if (video.readyState >= 2) start();
      else video.addEventListener('loadeddata', start, { once: true });
    }

    // Pause once it scrolls away so it is not decoding off-screen
    if ('IntersectionObserver' in window && !isReduced() && !thrifty && !narrow) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var played = video.play();
            if (played && played.catch) played.catch(function () {});
          } else if (!video.paused) {
            video.pause();
          }
        });
      }, { threshold: 0.15 }).observe(video);
    }

    if (soundBtn) {
      var hasAudio = false;

      var revealButton = function () {
        // Only offer the control if there is really a soundtrack to unmute
        hasAudio = video.mozHasAudio === true ||
                   Boolean(video.webkitAudioDecodedByteCount) ||
                   Boolean(video.audioTracks && video.audioTracks.length);
        // Not every browser exposes those, so fall back to showing it once
        // the file has actually loaded some data.
        if (hasAudio || video.readyState >= 2) soundBtn.hidden = false;
      };

      video.addEventListener('loadeddata', revealButton, { once: true });
      video.addEventListener('error', function () { soundBtn.hidden = true; });
      if (video.readyState >= 2) revealButton();

      soundBtn.addEventListener('click', function () {
        var turningOn = video.muted;
        video.muted = !turningOn;

        // Unmuting counts as a user gesture, so this play() will be allowed
        if (turningOn) {
          var played = video.play();
          if (played && played.catch) played.catch(function () {});
        }

        soundBtn.setAttribute('aria-pressed', String(turningOn));
        soundBtn.querySelector('.sound__label').textContent = turningOn ? 'Sound on' : 'Sound off';
      });
    }
  }


  /* ---------- 9. Anchor scrolling that respects reduced motion ---------- */

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;

    var id = link.getAttribute('href');
    if (id === '#' || id.length < 2) return;

    var target = document.querySelector(id);
    if (!target) return;

    e.preventDefault();
    target.scrollIntoView({ behavior: isReduced() ? 'auto' : 'smooth', block: 'start' });

    // Keyboard users must land on the section, not stay on the link
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    history.replaceState(null, '', id);
  });


  /* ---------- 10. Gallery lightbox ---------- */

  var lb = document.querySelector('[data-lightbox]');

  if (lb) {
    var lbImg = lb.querySelector('[data-lb-img]');
    var lbCap = lb.querySelector('[data-lb-cap]');
    var opener = null;

    var closeLb = function () {
      lb.hidden = true;
      document.body.style.overflow = '';
      if (opener) opener.focus();
    };

    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.shot__btn');
      if (btn) {
        opener = btn;
        lbImg.src = btn.getAttribute('data-full');
        lbImg.alt = btn.querySelector('img').alt;
        lbCap.textContent = btn.getAttribute('data-caption') || '';
        lb.hidden = false;
        document.body.style.overflow = 'hidden';
        lb.querySelector('[data-lb-close]').focus();
        return;
      }
      if (e.target.closest('[data-lb-close]') || e.target === lb) closeLb();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !lb.hidden) closeLb();
    });
  }


  /* ---------- 11. Enquiry form → WhatsApp ---------- */

  var enquiry = document.querySelector('[data-enquiry]');

  if (enquiry) {
    var status = enquiry.querySelector('[data-form-status]');

    enquiry.addEventListener('submit', function (e) {
      e.preventDefault();

      var val = function (n) { return (enquiry.elements[n].value || '').trim(); };
      var name = val('name');
      var dates = val('dates');
      var people = val('people');
      var note = val('note');

      if (!name || !dates || !people) {
        status.textContent = 'Name, dates and group size, then I can answer properly.';
        var firstEmpty = !name ? 'name' : (!dates ? 'dates' : 'people');
        enquiry.elements[firstEmpty].focus();
        return;
      }

      var lines = [
        'Hi Matt, this is ' + name + '.',
        'Dates: ' + dates,
        'Group size: ' + people
      ];
      if (note) lines.push('Note: ' + note);

      status.textContent = 'Opening WhatsApp…';
      window.open('https://wa.me/84983648362?text=' + encodeURIComponent(lines.join('\n')),
        '_blank', 'noopener');
    });
  }


  /* ---------- 12. Footer year ---------- */

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

})();
