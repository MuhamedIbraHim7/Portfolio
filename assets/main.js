(() => {
  const root = document.documentElement;
  const theme = document.querySelector('#theme-toggle');
  const preference = window.matchMedia('(prefers-color-scheme: dark)');

  function currentTheme() {
    return root.dataset.theme || (preference.matches ? 'dark' : 'light');
  }

  function syncTheme() {
    const current = currentTheme();
    theme.dataset.current = current;
    theme.setAttribute('aria-label', `Switch to ${current === 'dark' ? 'light' : 'dark'} theme`);
  }

  theme.hidden = false;
  syncTheme();
  preference.addEventListener('change', syncTheme);
  theme.addEventListener('click', () => {
    root.dataset.theme = currentTheme() === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch {}
    syncTheme();
  });

  const menu = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#primary-nav');
  const narrow = window.matchMedia('(max-width: 54rem)');
  function setMenu(open) {
    menu.hidden = !narrow.matches;
    nav.hidden = narrow.matches && !open;
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  }
  setMenu(false);
  narrow.addEventListener('change', () => setMenu(false));
  menu.addEventListener('click', () => setMenu(nav.hidden));
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menu.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.masthead') && !menu.hidden && !nav.hidden) setMenu(false);
  });
  document.addEventListener('focusin', (event) => {
    if (!event.target.closest('.masthead') && !menu.hidden && !nav.hidden) setMenu(false);
  });

  const filters = document.querySelector('.filter-bar');
  if (!filters) return;
  const cards = Array.from(document.querySelectorAll('.catalog .project-card'));
  const buttons = Array.from(filters.querySelectorAll('[data-filter]'));
  const result = filters.querySelector('.result-count');
  function applyFilter(category) {
    if (!buttons.some(button => button.dataset.filter === category)) category = '';
    let count = 0;
    for (const card of cards) {
      card.hidden = Boolean(category) && card.dataset.category !== category;
      if (!card.hidden) count++;
    }
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.dataset.filter === category));
    }
    result.textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
  }
  const linkedCategory = () => new URL(location.href).searchParams.get('category') || '';
  filters.hidden = false;
  applyFilter(linkedCategory());
  filters.addEventListener('click', event => {
    const button = event.target.closest('[data-filter]');
    if (!button || button.getAttribute('aria-pressed') === 'true') return;
    const url = new URL(location.href);
    const category = button.dataset.filter;
    if (category) url.searchParams.set('category', category);
    else url.searchParams.delete('category');
    history.pushState(null, '', url);
    applyFilter(category);
  });
  window.addEventListener('popstate', () => applyFilter(linkedCategory()));
})();
