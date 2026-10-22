/* Squarespace edition helper — Built by Truly Digital Solutions, LLC (TruTech) */
(() => {
  // In the Squarespace editor the page runs inside an iframe; leave blocks where they are there.
  if (window.top !== window.self) return;
  const slots = [...document.querySelectorAll('[data-sq-form-slot]')];
  if (!slots.length) return;
  const blocks = [...document.querySelectorAll('form')]
    .filter((f) => !f.closest('.rr-site') && !f.closest('[data-sq-form-slot]'))
    .map((f) => f.closest('.sqs-block') || f.closest('.form-wrapper') || f);
  slots.forEach((slot, i) => {
    const block = blocks[i];
    if (!block) return;
    const section = block.closest('.page-section, section');
    slot.innerHTML = '';
    slot.appendChild(block);
    if (section && !section.querySelector('.rr-site')) section.style.display = 'none';
  });
})();
