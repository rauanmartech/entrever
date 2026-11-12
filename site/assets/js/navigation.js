const navLinks = document.querySelector('.nav-links');
const sectionLinks = [...navLinks.querySelectorAll('a[href^="#"]')];
const sections = sectionLinks.map((link) => ({ link, id: link.hash.slice(1) }));
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let pendingId = null;
let settleTimer = null;
let scrollFrame = null;

function headerOffset() {
  return Math.ceil(document.querySelector('.site-header').getBoundingClientRect().bottom + 22);
}

function targetElement(id) {
  const targets = {
    experiencias: '.service-grid',
    trabalhos: '.portfolio-heading',
    diferenciais: '.advantages-heading',
  };
  return document.querySelector(targets[id] || `#${id}`);
}

function destination(id) {
  if (id === 'inicio' || id === 'conteudo') return 0;
  const element = targetElement(id);
  if (!element) return null;
  return Math.max(0, Math.round(element.getBoundingClientRect().top + window.scrollY - headerOffset()));
}

function jumpTo(top) {
  document.documentElement.style.scrollBehavior = 'auto';
  window.scrollTo(0, top);
  document.documentElement.style.scrollBehavior = '';
}

function setActive(id) {
  const active = sections.find((section) => section.id === id);
  if (!active) return;

  sections.forEach(({ link }) => {
    if (link === active.link) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });

  const navRect = navLinks.getBoundingClientRect();
  const linkRect = active.link.getBoundingClientRect();
  navLinks.style.setProperty('--indicator-x', `${linkRect.left - navRect.left}px`);
  navLinks.style.setProperty('--indicator-width', `${linkRect.width}px`);
  navLinks.classList.add('is-enhanced');
}

function activeFromScroll() {
  if (pendingId) return;
  let current = 'inicio';
  const position = window.scrollY + 28;
  for (const { id } of sections) {
    const top = destination(id);
    if (top !== null && position >= top) current = id;
  }
  setActive(current);
}

document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href^="#"]');
  if (!link) return;

  const id = link.hash.slice(1);
  const top = destination(id);
  if (top === null) return;

  event.preventDefault();
  if (window.location.hash !== link.hash) history.pushState(null, '', link.hash);
  if (sections.some((section) => section.id === id)) {
    pendingId = id;
    setActive(id);
  }
  if (reducedMotion.matches) jumpTo(top);
  else window.scrollTo({ top, behavior: 'smooth' });
  clearTimeout(settleTimer);
  settleTimer = setTimeout(() => {
    pendingId = null;
    activeFromScroll();
  }, 180);
});

window.addEventListener('scroll', () => {
  if (!scrollFrame) {
    scrollFrame = requestAnimationFrame(() => {
      activeFromScroll();
      scrollFrame = null;
    });
  }
  if (pendingId) {
    clearTimeout(settleTimer);
    settleTimer = setTimeout(() => {
      pendingId = null;
      activeFromScroll();
    }, 180);
  }
}, { passive: true });

window.addEventListener('resize', activeFromScroll);
window.addEventListener('popstate', () => {
  const id = window.location.hash.slice(1);
  const top = destination(id);
  if (top !== null) jumpTo(top);
  activeFromScroll();
});
window.addEventListener('load', () => {
  const id = window.location.hash.slice(1);
  const top = destination(id);
  if (top !== null) jumpTo(top);
  activeFromScroll();
});

document.querySelector('#footer-year').textContent = new Date().getFullYear();
activeFromScroll();
