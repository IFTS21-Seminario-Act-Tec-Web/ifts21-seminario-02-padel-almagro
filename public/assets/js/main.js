// ============================================================
// PADEL ALMAGRO — main.js
//
// Interactividad del sitio. Este archivo maneja:
//   1. Año dinámico en el footer
//   2. Navbar: transparente → verde oscuro al scrollear
//   3. Botón "volver arriba"
//   4. Sección activa en el nav (IntersectionObserver)
//   5. Demo de reserva
//   6. Formulario de contacto con validación
//
// Nota: el colapso del menú hamburguesa en mobile está
// manejado por Bootstrap JS (bootstrap.bundle.min.js).
// ============================================================

"use strict";


// ─── 1. AÑO DINÁMICO EN EL FOOTER ───────────────────────────

document.getElementById('year').textContent = new Date().getFullYear();


// ─── 2. NAVBAR: TRANSPARENTE → OSCURO AL SCROLLEAR ──────────
//
// El navbar arranca sin background (transparente sobre la foto).
// Al bajar 30px, el JS agrega .scrolled que activa el fondo
// verde oscuro con blur (definido en styles.css).

const siteNav   = document.getElementById('siteNav');
const backToTop = document.getElementById('backToTop');

function updateScrollState() {
  siteNav?.classList.toggle('scrolled', window.scrollY > 30);
  backToTop?.classList.toggle('visible', window.scrollY > 450);
}

window.addEventListener('scroll', updateScrollState, { passive: true });

// Ejecutar al inicio para setear el estado correcto en carga
updateScrollState();


// ─── 3. BOTÓN "VOLVER ARRIBA" ────────────────────────────────

backToTop?.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


// ─── 4. SECCIÓN ACTIVA EN EL NAV (IntersectionObserver) ──────
//
// Resalta automáticamente el link del nav que corresponde
// a la sección visible en pantalla.
//
// data-section en cada <a> del nav debe coincidir con el id
// de la sección correspondiente.

const navLinks = document.querySelectorAll('.pa-nav-link[data-section]');
const sections = document.querySelectorAll('section[id]');

const observerOptions = {
  root: null,
  rootMargin: '-25% 0px -65% 0px',
  // Una sección se "activa" cuando su parte superior
  // está entre el 25% y el 35% del viewport.
  threshold: 0
};

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {

      navLinks.forEach(link => link.classList.remove('active'));

      const activeLink = document.querySelector(
        `.pa-nav-link[data-section="${entry.target.id}"]`
      );

      if (activeLink) {
        activeLink.classList.add('active');
        // .active dispara el subrayado verde animado (::after en CSS)
      }
    }
  });
}, observerOptions);

sections.forEach(section => sectionObserver.observe(section));


// ─── 5. DEMO DE RESERVA ──────────────────────────────────────
//
// Simula una reserva con feedback visual y reset automático.
// En la etapa de backend enviará a POST /api/reservas (FastAPI).

const reservationDemo = document.getElementById('reservationDemo');
const demoMessage     = document.getElementById('demoMessage');

reservationDemo?.addEventListener('click', () => {

  demoMessage.textContent = '¡Perfecto! Esta es una demo. En la próxima etapa este botón podrá consultar FastAPI y guardar la reserva en la base de datos.';

  reservationDemo.innerHTML = '<i class="bi bi-check2-circle"></i> Demo realizada';

  setTimeout(() => {
    reservationDemo.innerHTML = '<i class="bi bi-calendar-plus"></i> Probar reserva';
    demoMessage.textContent   = '';
  }, 4500);
});


// ─── 6. FORMULARIO DE CONTACTO ───────────────────────────────
//
// Validación nativa HTML5. Sin librerías externas.
//
// PRÓXIMO PASO (etapa backend):
//   const data = Object.fromEntries(new FormData(contactForm));
//   const res  = await fetch('/api/contact', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data)
//   });
//
// Ver: src/routes/contact.py (FastAPI router)

const contactForm = document.getElementById('contactForm');
const formMessage  = document.getElementById('formMessage');

contactForm?.addEventListener('submit', (event) => {
  event.preventDefault();

  if (!contactForm.checkValidity()) {
    contactForm.reportValidity();
    return;
  }

  formMessage.textContent = '✓ Mensaje preparado correctamente. En la etapa de backend se enviará a FastAPI.';

  contactForm.reset();
});