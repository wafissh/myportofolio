
document.addEventListener('DOMContentLoaded', () => {
  // Parallax clouds
  window.addEventListener('scroll', () => {
    const scrollPos = window.pageYOffset;

    const cloudBack = document.getElementById('cloud-back');
    const cloudMid = document.getElementById('cloud-mid');
    const cloudFront = document.getElementById('cloud-front');
    const cloudFront2 = document.getElementById('cloud-front-2');
    const cloudbottom = document.getElementById('cloud-bottom')

    if (cloudBack) cloudBack.style.transform = `translateY(${scrollPos * -0.35}px)`;
    if (cloudMid) cloudMid.style.transform = `translateY(${scrollPos * -0.35}px)`;
    if (cloudFront) cloudFront.style.transform = `translateY(${scrollPos * -0.65}px)`;
    if (cloudFront2) cloudFront2.style.transform = `translateY(${scrollPos * -0.65}px)`;
    if (cloudbottom) cloudbottom.style.transform = `translateY(${scrollPos * -0.035}px)`;
  });

  // Dark Mode Toggle
  const themeToggle = document.getElementById('theme-toggle');
  const hero = document.querySelector('.hero');

  // Load saved theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateHeroBg(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateHeroBg(next);
    });
  }

  function updateHeroBg(theme) {
    if (hero) {
      if (theme === 'dark') {
        hero.style.backgroundImage = 'url("/static/img/malam.jpg")';
      } else {
        hero.style.backgroundImage = 'url("/static/img/siang.jpg")';
      }
    }
  }

  // Filter per section
  const sections = document.querySelectorAll('.category-buttons');
  sections.forEach(btnGroup => {
    const btns = btnGroup.querySelectorAll('.filter-btn');
    const parentSection = btnGroup.closest('section');
    const cards = parentSection.querySelectorAll('.tech-card, .timeline-item');
    const emptyState = parentSection.querySelector('.empty-experience-state');

    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        btns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const category = btn.getAttribute('data-category');
        let visibleCount = 0;

        cards.forEach(card => {
          if (category === 'all' || card.getAttribute('data-category') === category) {
            card.classList.remove('hidden');
            visibleCount++;
          } else {
            card.classList.add('hidden');
          }
        });

        // Sembunyiin year header kalau ga ada visible experience
        const timeline = parentSection.querySelector('.timeline');
        if (timeline) {
          const yearHeaders = timeline.querySelectorAll('.timeline-year');
          yearHeaders.forEach(yearEl => {
            let next = yearEl.nextElementSibling;
            let hasVisible = false;
            while (next && !next.classList.contains('timeline-year')) {
              if (next.classList.contains('timeline-item') && !next.classList.contains('hidden')) {
                hasVisible = true;
                break;
              }
              next = next.nextElementSibling;
            }
            yearEl.style.display = hasVisible ? '' : 'none';
          });

          // Tampilin / sembunyiin empty state
          if (emptyState) {
            emptyState.style.display = visibleCount === 0 ? '' : 'none';
          }
        }
      });
    });
  });
});
