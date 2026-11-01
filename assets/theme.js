(() => {
  const root = document.documentElement;
  let theme = 'light';
  try { if (localStorage.getItem('wonderworld-theme') === 'dark') theme = 'dark'; } catch (_) {}
  root.dataset.theme = theme;
  function update() {
    const dark = root.dataset.theme === 'dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.textContent = dark ? '☀ Light mode' : '☾ Dark mode';
      button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      button.setAttribute('aria-pressed', String(dark));
    });
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = dark ? '#101113' : '#fafaf7';
  }
  document.addEventListener('DOMContentLoaded', () => {
    update();
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.addEventListener('click', () => {
        root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('wonderworld-theme', root.dataset.theme); } catch (_) {}
        update();
      });
    });
  });
})();
