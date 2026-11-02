// ============================================================
// PADEL ALMAGRO — main.js
//
// Interactividad del sitio. Este archivo maneja:
//   1. Año dinámico en el footer
//   2. Navbar: transparente → verde oscuro al scrollear
//   3. Botón "volver arriba"
//   4. Cerrar el menú mobile al elegir una sección
//   5. Sección activa en el nav (IntersectionObserver)
//   6. Demo de reserva
//   7. Formulario de contacto con validación
//
// Nota: el colapso del menú hamburguesa en mobile está
// manejado por Bootstrap JS (bootstrap.bundle.min.js).
// ============================================================

"use strict";


// ─── 0. PREFERENCIA DE MOVIMIENTO REDUCIDO ──────────────────
//
// Si el sistema operativo pide menos animaciones, el scroll
// suave se desactiva (igual que hace el CSS con las
// transiciones en @media prefers-reduced-motion).

const prefersReducedMotion =
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const scrollBehavior = prefersReducedMotion ? 'auto' : 'smooth';


// ─── 1. AÑO DINÁMICO EN EL FOOTER ───────────────────────────
//
// Con ?. — sin el optional chaining, si el <span id="year">
// no existiera este error cortaría la ejecución de TODO el
// archivo y ninguna de las funciones de abajo se registraría.

const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());






// ─── 3. ACCESO FLOTANTE A WHATSAPP (cancha / clase) ──────────
//
// Reemplaza al botón "volver arriba". El botón verde abre un
// menú con dos opciones y cada una arma su propio link a
// wa.me con un mensaje distinto según el tipo de consulta.
//
// El tipo se define en el HTML con data-wa-tipo="cancha|clase".

const WA_NUMERO = '5491159232537'; // 54 + 9 + código de área (sin 0) + número (sin 15)

const WA_MENSAJES = {
  cancha: 'Hola! Quiero consultar disponibilidad y precios para alquilar una cancha en Padel Almagro.',
  clase:  'Hola! Quiero consultar por las clases de pádel en Padel Almagro (niveles, horarios y precios).'
};

const waFloat  = document.getElementById('waFloat');
const waToggle = document.getElementById('waToggle');
const waMenu   = document.getElementById('waMenu');

function setWaMenu(abierto) {
  waMenu.hidden = !abierto;
  waToggle.setAttribute('aria-expanded', String(abierto));
}

if (waFloat && waToggle && waMenu) {

  // Armar el link de cada opción según su tipo de consulta
  waMenu.querySelectorAll('[data-wa-tipo]').forEach(opcion => {
    const mensaje = WA_MENSAJES[opcion.dataset.waTipo];
    opcion.href = `https://wa.me/${WA_NUMERO}?text=${encodeURIComponent(mensaje)}`;
  });

  waToggle.addEventListener('click', () => setWaMenu(waMenu.hidden));

  // Cerrar al hacer click afuera o con Escape
  document.addEventListener('click', (e) => {
    if (!waFloat.contains(e.target)) setWaMenu(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setWaMenu(false);
  });
}


// ─── 4. CERRAR EL MENÚ MOBILE AL ELEGIR UNA SECCIÓN ─────────
//
// Bootstrap abre el collapse pero no lo cierra al tocar un
// link: el menú quedaba tapando la sección recién elegida.
// Sólo cerramos si el collapse está efectivamente abierto,
// es decir en mobile (en desktop nunca tiene la clase .show).

const navCollapse = document.getElementById('navLinks');

navCollapse?.addEventListener('click', (event) => {
  if (!event.target.closest('a')) return;
  if (!navCollapse.classList.contains('show')) return;

  // bootstrap.Collapse existe porque el bundle se carga antes
  // que este archivo. El getOrCreateInstance evita crear dos.
  window.bootstrap?.Collapse
    ?.getOrCreateInstance(navCollapse, { toggle: false })
    ?.hide();
});


// ─── 5. SECCIÓN ACTIVA EN EL NAV (IntersectionObserver) ──────
//
// Resalta automáticamente el link del nav que corresponde
// a la sección visible en pantalla.
//
// data-section en cada <a> del nav debe coincidir con el id
// de la sección correspondiente.
//
// OJO: sólo observamos las secciones que TIENEN un link en el
// nav. Antes se observaban todas las <section id>, así que al
// pasar por #reservas (que no está en el menú) se borraban
// todos los .active y el nav se quedaba sin nada resaltado.

const navLinks = document.querySelectorAll('.pa-nav-link[data-section]');

const linkBySection = new Map();
navLinks.forEach(link => linkBySection.set(link.dataset.section, link));

const observedSections = [...linkBySection.keys()]
  .map(id => document.getElementById(id))
  .filter(Boolean);

const observerOptions = {
  root: null,
  rootMargin: '-25% 0px -65% 0px',
  // Una sección se "activa" cuando su parte superior
  // está entre el 25% y el 35% del viewport.
  threshold: 0
};

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;

    const activeLink = linkBySection.get(entry.target.id);
    if (!activeLink) return;

    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
    // .active dispara el subrayado verde animado (::after en CSS)
  });
}, observerOptions);

observedSections.forEach(section => sectionObserver.observe(section));


// ─── 6. DEMO DE RESERVA ──────────────────────────────────────
//
// Simula una reserva con feedback visual y reset automático.
// En la etapa de backend enviará a POST /api/reservas (FastAPI).

const reservationDemo = document.getElementById('reservationDemo');
const demoMessage     = document.getElementById('demoMessage');

// Guardamos el id del timeout: si el usuario vuelve a apretar
// antes de que termine, se cancela el anterior. Sin esto los
// timeouts se acumulaban y el botón parpadeaba.
let demoTimeoutId = null;

const DEMO_LABEL_IDLE = '<i class="bi bi-calendar-plus" aria-hidden="true"></i> Probar reserva';
const DEMO_LABEL_DONE = '<i class="bi bi-check2-circle" aria-hidden="true"></i> Demo realizada';

reservationDemo?.addEventListener('click', () => {
  clearTimeout(demoTimeoutId);

  if (demoMessage) {
    demoMessage.textContent = '¡Perfecto! Esta es una demo. En la próxima etapa este botón podrá consultar FastAPI y guardar la reserva en la base de datos.';
  }

  reservationDemo.innerHTML = DEMO_LABEL_DONE;

  demoTimeoutId = setTimeout(() => {
    reservationDemo.innerHTML = DEMO_LABEL_IDLE;
    if (demoMessage) demoMessage.textContent = '';
  }, 4500);
});


// ─── 7. FORMULARIO DE CONTACTO ───────────────────────────────
//
// Valida, envía los datos a FastAPI (POST /api/contact) y, si la
// API responde bien, abre WhatsApp con el mensaje.
// Los nombres de los campos (name, email, subject, message)
// coinciden con el modelo Contacto de src/routes/contact.py.

const API_URL = '/api/contact';

const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

let formTimeoutId = null;

function mostrarAviso(texto, duracion = 6000) {
  if (!formMessage) return;
  clearTimeout(formTimeoutId);
  formMessage.textContent = texto;
  formTimeoutId = setTimeout(() => { formMessage.textContent = ''; }, duracion);
}

contactForm?.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!contactForm.checkValidity()) {
    contactForm.reportValidity();
    return;
  }

  const data = Object.fromEntries(new FormData(contactForm));

  // El <select> no es "required" en el HTML, así que lo validamos acá
  if (!data.subject) {
    mostrarAviso('Elegí un asunto para tu consulta.');
    return;
  }

  const boton = contactForm.querySelector('button[type="submit"]');
  boton.disabled = true;

  // Abrimos la pestaña ahora, dentro del click, porque si se abre
  // después del await el navegador puede bloquearla como pop-up.
  const ventanaWa = window.open('', '_blank');

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!res.ok) {
      ventanaWa?.close();
      mostrarAviso(
        res.status === 422
          ? 'Revisá los datos: hay campos con formato inválido.'
          : 'No pudimos enviar tu consulta. Probá de nuevo en un rato.'
      );
      return;
    }

    const texto = `Hola! Soy ${data.name}. Asunto: ${data.subject}. ${data.message}`;
    const urlWa = `https://wa.me/${WA_NUMERO}?text=${encodeURIComponent(texto)}`;

    if (ventanaWa) {
      ventanaWa.location.href = urlWa;
    } else {
      window.location.href = urlWa; // si el navegador bloqueó la pestaña
    }

    mostrarAviso('✓ Consulta enviada. Te abrimos WhatsApp para seguir la conversación.');
    contactForm.reset();

  } catch (error) {
    ventanaWa?.close();
    mostrarAviso('No se pudo conectar con el servidor. Verificá que la API esté encendida.');
  } finally {
    boton.disabled = false;
  }
});