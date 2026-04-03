/* ─────────────────────────────────────────────
   KARMAN — Corporate Services Singapore
   script.js
───────────────────────────────────────────── */

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


// Dropdown is handled entirely by CSS :hover — no JS needed.

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

    if (!name || !email) {
      showFormMessage(contactForm, 'Please fill in your name and email address.', 'error');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
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
      body: JSON.stringify({ name, email, service, message })
    })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(() => {
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
