/* Squarespace edition helper — Built by Truly Digital Solutions, LLC (TruTech) */
(() => {
  // In the Squarespace editor the page runs inside an iframe; leave blocks where they are there.
  if (window.top !== window.self) return;
  const slots = [...document.querySelectorAll('[data-sq-form-slot]')];
  if (!slots.length) return;
  const blocks = [...document.querySelectorAll('.sqs-block-form, .form-block')]
    .filter((b) => !b.closest('.rr-site') && !b.parentElement.closest('.sqs-block-form, .form-block'));
  slots.forEach((slot, i) => {
    const block = blocks[i];
    if (!block) return;
    const section = block.closest('.page-section, section');
    slot.innerHTML = '';
    slot.appendChild(block);
    if (section && !section.querySelector('.rr-site')) section.style.display = 'none';
  });
})();
