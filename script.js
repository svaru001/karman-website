/* ─────────────────────────────────────────────
   KARMAN — Corporate Services Singapore
   script.js
───────────────────────────────────────────── */

// === GA4 CTA CLICK TRACKING ===
// Tracks every click on key conversion CTAs across the entire site.
document.addEventListener('click', (e) => {
  if (typeof gtag !== 'function') return;
  const a = e.target.closest('a, button');
  if (!a) return;

  const href = (a.getAttribute('href') || '').trim();
  const label = (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);

  // High-intent CTAs
  if (href === '/onboarding' || href.startsWith('/onboarding?') || href.startsWith('/onboarding#')) {
    gtag('event', 'cta_click', { cta: 'get_started', destination: href, label, page_path: location.pathname });
  } else if (href === '#contact' || href.startsWith('#contact')) {
    gtag('event', 'cta_click', { cta: 'contact_us', destination: href, label, page_path: location.pathname });
  } else if (href.includes('mailto:') || href.includes('tel:')) {
    gtag('event', 'cta_click', { cta: href.startsWith('mailto:') ? 'email_click' : 'phone_click', destination: href, label, page_path: location.pathname });
  } else if (href.startsWith('/tools/')) {
    gtag('event', 'cta_click', { cta: 'tool_open', destination: href, label, page_path: location.pathname });
  } else if (href === '/ask' || href.startsWith('/ask?') || href.startsWith('/ask#')) {
    gtag('event', 'cta_click', { cta: 'ask_ai', destination: href, label, page_path: location.pathname });
  }
}, { capture: true, passive: true });


// === HEADER SCROLL EFFECT ===
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
}, { passive: true });


// === MOBILE NAV TOGGLE ===
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

hamburger.addEventListener('click', () => {
  const isOpen = navMenu.classList.toggle('open');
  hamburger.setAttribute('aria-expanded', isOpen);

  // Animate hamburger to X
  const spans = hamburger.querySelectorAll('span');
  if (isOpen) {
    spans[0].style.cssText = 'transform: translateY(7px) rotate(45deg)';
    spans[1].style.cssText = 'opacity: 0';
    spans[2].style.cssText = 'transform: translateY(-7px) rotate(-45deg)';
  } else {
    spans.forEach(s => s.style.cssText = '');
  }
});

// Close mobile nav on link click
navMenu.querySelectorAll('.nav__link').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('open');
    hamburger.querySelectorAll('span').forEach(s => s.style.cssText = '');
  });
});

// Close on outside click
document.addEventListener('click', (e) => {
  if (!header.contains(e.target) && navMenu.classList.contains('open')) {
    navMenu.classList.remove('open');
    hamburger.querySelectorAll('span').forEach(s => s.style.cssText = '');
  }
});


// === DROPDOWN CLICK TOGGLE ===
const hasDropdown = document.querySelector('.has-dropdown');
if (hasDropdown) {
  const trigger = hasDropdown.querySelector('.nav__link');

  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    hasDropdown.classList.toggle('is-open');
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (!hasDropdown.contains(e.target)) {
      hasDropdown.classList.remove('is-open');
    }
  });
}


// === SCROLL REVEAL ANIMATIONS ===
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger sibling reveals
      const siblings = entry.target.parentElement.querySelectorAll('.reveal');
      siblings.forEach((el, idx) => {
        if (el === entry.target) {
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, idx * 80);
        }
      });
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.12,
  rootMargin: '0px 0px -40px 0px'
});

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));


// === PRICING TABS ===
const pricingTabs = document.querySelectorAll('.pricing-tab');
const pricingPlans = document.querySelectorAll('.pricing__plans');

pricingTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.tab;

    pricingTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    pricingPlans.forEach(plan => {
      plan.classList.add('hidden');
      plan.classList.remove('visible');
    });

    const targetPlan = document.getElementById(`tab-${target}`);
    if (targetPlan) {
      targetPlan.classList.remove('hidden');
      // Re-trigger reveal animations on newly shown cards
      setTimeout(() => {
        targetPlan.querySelectorAll('.reveal').forEach((el, i) => {
          setTimeout(() => el.classList.add('visible'), i * 80);
        });
      }, 10);
    }
  });
});

// Initialize first tab cards as visible
document.querySelectorAll('#tab-incorporation .reveal').forEach((el, i) => {
  setTimeout(() => el.classList.add('visible'), 200 + i * 80);
});


// === FAQ ACCORDION ===
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const isExpanded = btn.getAttribute('aria-expanded') === 'true';
    const answer = btn.nextElementSibling;

    // Close all
    document.querySelectorAll('.faq-question').forEach(b => {
      b.setAttribute('aria-expanded', 'false');
      b.nextElementSibling.classList.remove('open');
    });

    // Open clicked if it was closed
    if (!isExpanded) {
      btn.setAttribute('aria-expanded', 'true');
      answer.classList.add('open');
    }
  });
});


// === SMOOTH SCROLL FOR ANCHOR LINKS ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (href === '#') return;
    // Skip dropdown triggers — they open the menu, not scroll
    if (anchor.closest('.has-dropdown') && anchor.classList.contains('nav__link')) return;

    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      const offset = 80; // header height
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});


// === CONTACT FORM ===
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const btn = contactForm.querySelector('button[type="submit"]');
    const originalText = btn.textContent;

    // Validate fields
    const name = contactForm.querySelector('#name').value.trim();
    const email = contactForm.querySelector('#email').value.trim();
    const phone = (contactForm.querySelector('#phone') || {}).value?.trim() || '';

    if (!name) {
      showFormMessage(contactForm, 'Please fill in your name.', 'error');
      return;
    }

    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showFormMessage(contactForm, 'Please enter a valid email address.', 'error');
      return;
    }

    const service = (contactForm.querySelector('#service') || {}).value || '';
    const message = (contactForm.querySelector('#message') || {}).value || '';

    btn.textContent = 'Sending…';
    btn.disabled = true;

    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, service, message })
    })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(() => {
        if (typeof gtag === 'function') {
          gtag('event', 'generate_lead', {
            form_name: 'contact',
            service: service || 'unspecified',
            page_path: location.pathname
          });
        }
        btn.textContent = '✓ Message sent!';
        btn.style.background = 'var(--teal)';
        showFormMessage(contactForm, "Thanks! We'll be in touch within 1 business day. Check your inbox for a confirmation.", 'success');
        setTimeout(() => {
          btn.textContent = originalText;
          btn.disabled = false;
          btn.style.background = '';
          contactForm.reset();
          removeFormMessage(contactForm);
        }, 5000);
      })
      .catch(() => {
        btn.textContent = originalText;
        btn.disabled = false;
        showFormMessage(contactForm, 'Something went wrong. Please email us directly at team@karman.com.sg', 'error');
      });
  });
}

function showFormMessage(form, text, type) {
  removeFormMessage(form);
  const msg = document.createElement('p');
  msg.className = `form-message form-message--${type}`;
  msg.textContent = text;
  msg.style.cssText = `
    text-align: center;
    font-size: 14px;
    font-weight: 500;
    padding: 12px 16px;
    border-radius: 8px;
    margin-top: 12px;
    background: ${type === 'success' ? 'rgba(0,201,167,.1)' : 'rgba(239,68,68,.1)'};
    color: ${type === 'success' ? '#047857' : '#dc2626'};
    border: 1px solid ${type === 'success' ? 'rgba(0,201,167,.3)' : 'rgba(239,68,68,.3)'};
  `;
  form.appendChild(msg);
}

function removeFormMessage(form) {
  const existing = form.querySelector('.form-message');
  if (existing) existing.remove();
}


// === ACTIVE NAV LINK HIGHLIGHT ===
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__link[href^="#"]');

const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(link => link.classList.remove('active'));
      const active = document.querySelector(`.nav__link[href="#${entry.target.id}"]`);
      if (active) active.classList.add('active');
    }
  });
}, { threshold: 0.4 });

sections.forEach(section => navObserver.observe(section));


// === STATS COUNTER ANIMATION ===
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.stat strong').forEach(el => {
        const text = el.textContent;
        const match = text.match(/[\d,]+/);
        if (!match) return;

        const end = parseInt(match[0].replace(/,/g, ''));
        const suffix = text.replace(/[\d,]+/, '');
        const duration = 1200;
        const start = performance.now();

        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3); // ease out cubic
          const current = Math.round(eased * end);
          el.textContent = current.toLocaleString() + suffix;
          if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
      });
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero__stats');
if (heroStats) counterObserver.observe(heroStats);



// === AUTO-TOC FOR BLOG POSTS ===
// Builds a Table of Contents from <article class="article-body"> H2 headings.
// Only runs if (a) we're on a blog page, (b) there are 3+ H2s, (c) no existing TOC.
(function() {
  const article = document.querySelector('.article-body');
  if (!article) return;

  const sidebar = document.querySelector('.article-sidebar');
  if (!sidebar) return;

  // Skip if a manual TOC already exists ("In this article" or class="toc")
  const sidebarText = sidebar.textContent || '';
  if (/in\s+this\s+article/i.test(sidebarText)) return;
  if (sidebar.querySelector('.toc')) return;

  const h2s = article.querySelectorAll('h2');
  if (h2s.length < 3) return;

  function slugify(text) {
    return text.trim().toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
      .slice(0, 60);
  }

  // Assign IDs and collect TOC items
  const items = [];
  const usedIds = new Set();
  h2s.forEach(h2 => {
    let id = h2.id || slugify(h2.textContent);
    if (!id) return;
    let unique = id;
    let suffix = 2;
    while (usedIds.has(unique)) unique = id + '-' + suffix++;
    h2.id = unique;
    usedIds.add(unique);
    items.push({ id: unique, text: h2.textContent.trim() });
  });

  if (!items.length) return;

  // Build TOC card and insert as the FIRST sidebar item
  const card = document.createElement('div');
  card.className = 'sidebar-card sidebar-card--toc';
  card.innerHTML = '<h3>In this article</h3><ul>' +
    items.map(i => '<li><a href="#' + i.id + '" data-toc-link>' + i.text.replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'})[c]) + '</a></li>').join('') +
    '</ul>';
  sidebar.insertBefore(card, sidebar.firstChild);

  // Smooth-scroll on click with header offset
  card.querySelectorAll('a[data-toc-link]').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const offset = 88; // sticky header
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
      history.replaceState(null, '', href);
    });
  });

  // Active section highlighting via IntersectionObserver
  const tocLinks = card.querySelectorAll('a[data-toc-link]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tocLinks.forEach(l => l.classList.remove('is-active'));
        const active = card.querySelector('a[href="#' + entry.target.id + '"]');
        if (active) active.classList.add('is-active');
      }
    });
  }, { rootMargin: '-100px 0px -70% 0px', threshold: 0 });

  h2s.forEach(h2 => observer.observe(h2));
})();


// === WHATSAPP FLOATING BUTTON ===
// Uses inline styles to bypass Vercel's CSS cache (max-age:86400).
(function () {
  if (document.getElementById('wa-fab')) return;
  var wa = document.createElement('a');
  wa.id = 'wa-fab';
  wa.href = 'https://wa.me/6580743630?text=Hi!%20I%27d%20like%20to%20incorporate%20a%20company%20in%20Singapore.%20Can%20we%20have%20a%20quick%20chat%3F';
  wa.target = '_blank';
  wa.rel = 'noopener noreferrer';
  wa.setAttribute('aria-label', 'Chat on WhatsApp');
  wa.style.cssText = 'position:fixed;bottom:24px;right:24px;width:56px;height:56px;background:#25D366;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(37,211,102,.45);z-index:1050;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease;';
  wa.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413A11.815 11.815 0 0 0 12.05 0zm0 21.785h-.004a9.86 9.86 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.861 9.861 0 0 1-1.51-5.26c.002-5.45 4.436-9.884 9.889-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.892 6.993c-.002 5.451-4.437 9.885-9.885 9.885z"/></svg>';
  wa.addEventListener('mouseenter', function () {
    wa.style.transform = 'scale(1.12)';
    wa.style.boxShadow = '0 6px 28px rgba(37,211,102,.65)';
  });
  wa.addEventListener('mouseleave', function () {
    wa.style.transform = 'scale(1)';
    wa.style.boxShadow = '0 4px 20px rgba(37,211,102,.45)';
  });
  wa.addEventListener('click', function () {
    if (typeof gtag === 'function') {
      gtag('event', 'whatsapp_click', { page_path: location.pathname });
    }
  });
  document.body.appendChild(wa);
})();

// === BLOG MOBILE CONTACT CTA ===
// Injects a message icon next to the hamburger on blog post pages.
// Tapping it opens a bottom-sheet contact form.
(function () {
  if (!document.querySelector('.article-body')) return;

  const hamburger = document.getElementById('hamburger');
  if (!hamburger) return;

  // Inject button after logo (left side of nav)
  const msgBtn = document.createElement('button');
  msgBtn.className = 'nav__msg-btn';
  msgBtn.setAttribute('aria-label', 'Contact us');
  msgBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>Talk to us</span>';
  const navMenu = hamburger.parentNode.querySelector('.nav__menu');
  hamburger.parentNode.insertBefore(msgBtn, navMenu || hamburger);

  // Inject bottom-sheet modal
  const overlay = document.createElement('div');
  overlay.id = 'blogContactOverlay';
  overlay.className = 'contact-modal-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'bcfTitle');
  overlay.innerHTML =
    '<div class="contact-modal">' +
      '<div class="contact-modal__header">' +
        '<span class="contact-modal__title" id="bcfTitle">Get in touch</span>' +
        '<button class="contact-modal__close" id="blogContactClose" aria-label="Close">✕</button>' +
      '</div>' +
      '<p class="contact-modal__sub">We typically respond within 1 business day.</p>' +
      '<form class="contact-modal__form" id="blogContactForm" novalidate>' +
        '<div class="form-group"><label for="bcfName">Your name</label><input type="text" id="bcfName" name="name" placeholder="Jane Smith" autocomplete="name" /></div>' +
        '<div class="form-group"><label for="bcfEmail">Email address</label><input type="email" id="bcfEmail" name="email" placeholder="jane@company.com" autocomplete="email" /></div>' +
        '<div class="form-group"><label for="bcfMsg">How can we help?</label><textarea id="bcfMsg" name="message" rows="3" placeholder="Tell us about your needs…"></textarea></div>' +
        '<button type="submit" class="btn btn--primary btn--full">Send message</button>' +
      '</form>' +
    '</div>';
  document.body.appendChild(overlay);

  function openModal() {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => { var el = overlay.querySelector('#bcfName'); if (el) el.focus(); }, 300);
  }
  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  msgBtn.addEventListener('click', openModal);
  document.getElementById('blogContactClose').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && overlay.classList.contains('open')) closeModal(); });

  document.getElementById('blogContactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var form = e.target;
    var btn = form.querySelector('button[type="submit"]');
    var name = form.querySelector('#bcfName').value.trim();
    var email = form.querySelector('#bcfEmail').value.trim();
    var message = form.querySelector('#bcfMsg').value.trim();

    if (!name) { alert('Please enter your name.'); return; }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { alert('Please enter a valid email address.'); return; }

    btn.disabled = true;
    btn.textContent = 'Sending…';

    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, email: email, message: message, form_name: 'blog_cta', page: window.location.pathname })
    })
    .then(function (r) { return r.json(); })
    .then(function () {
      form.innerHTML = '<p class="contact-modal__success">✓ Thanks! We’ll be in touch shortly.</p>';
      setTimeout(closeModal, 2500);
    })
    .catch(function () {
      btn.disabled = false;
      btn.textContent = 'Send message';
      alert('Something went wrong. Please email us at team@karman.com.sg');
    });
  });
})();
