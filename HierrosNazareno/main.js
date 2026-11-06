// Tablas de medidas y pesos teóricos por metro (kg/m)
const specsData = {
  tubo: [
    { label: '40 x 40 x 1.6 mm', weight: 1.85 },
    { label: '50 x 50 x 2.0 mm', weight: 2.95 },
    { label: '80 x 40 x 2.0 mm', weight: 3.65 },
    { label: '100 x 100 x 3.2 mm', weight: 9.20 }
  ],
  ipn: [
    { label: 'IPN 80 (80 mm) - 5.95 kg/m', weight: 5.95 },
    { label: 'IPN 100 (100 mm) - 8.32 kg/m', weight: 8.32 },
    { label: 'IPN 140 (140 mm) - 14.40 kg/m', weight: 14.40 },
    { label: 'IPN 200 (200 mm) - 26.30 kg/m', weight: 26.30 }
  ],
  upn: [
    { label: 'UPN 80 (80 mm) - 8.64 kg/m', weight: 8.64 },
    { label: 'UPN 100 (100 mm) - 10.60 kg/m', weight: 10.60 },
    { label: 'UPN 140 (140 mm) - 16.00 kg/m', weight: 16.00 }
  ],
  chapa: [
    { label: 'Chapa C-25 Cincalum (4.85 kg/m lineal)', weight: 4.85 },
    { label: 'Chapa C-22 Cincalum (6.20 kg/m lineal)', weight: 6.20 },
    { label: 'Chapa Negra Lisa 1/8" (25.0 kg/m²)', weight: 25.00 }
  ],
  hierro: [
    { label: 'Hierro Construcción Ø 8 mm (0.395 kg/m)', weight: 0.395 },
    { label: 'Hierro Construcción Ø 10 mm (0.617 kg/m)', weight: 0.617 },
    { label: 'Hierro Construcción Ø 12 mm (0.888 kg/m)', weight: 0.888 },
    { label: 'Hierro Construcción Ø 16 mm (1.580 kg/m)', weight: 1.580 }
  ]
};

function updateCalcSpecs() {
  const mat = document.getElementById('calc-material').value;
  const sizeSelect = document.getElementById('calc-size');
  sizeSelect.innerHTML = '';
  
  const items = specsData[mat] || specsData.tubo;
  items.forEach((item, index) => {
    const opt = document.createElement('option');
    opt.value = item.weight;
    opt.textContent = `${item.label} (${item.weight} kg/m)`;
    if (index === 0) opt.selected = true;
    sizeSelect.appendChild(opt);
  });

  calculateWeight();
}

function calculateWeight() {
  const weightPerMeter = parseFloat(document.getElementById('calc-size').value) || 0;
  const length = parseFloat(document.getElementById('calc-length').value) || 0;
  const qty = parseFloat(document.getElementById('calc-qty').value) || 0;

  const totalKg = (weightPerMeter * length * qty);
  const totalTn = totalKg / 1000;

  document.getElementById('calc-result-kg').textContent = totalKg.toLocaleString('es-AR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  document.getElementById('calc-result-tn').textContent = `(${totalTn.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} Tn)`;
}

let cartCount = 3;

function addToCart(productName, price) {
  cartCount++;
  const counter = document.getElementById('cart-counter');
  if (counter) counter.textContent = cartCount;
  showToast(`¡Agregado!: ${productName}`);
}

function addCalculatedToCart() {
  const matSelect = document.getElementById('calc-material');
  const mat = matSelect.options[matSelect.selectedIndex].text;
  const kg = document.getElementById('calc-result-kg').textContent;
  addToCart(`${mat} (${kg} kg cotizados)`, 0);
}

function toggleAdminDrawer() {
  const drawer = document.getElementById('admin-drawer');
  drawer.classList.toggle('-translate-x-full');
}

function openCartPreview() {
  document.getElementById('cart-modal').classList.remove('hidden');
}

function closeCartPreview() {
  document.getElementById('cart-modal').classList.add('hidden');
}

function showToast(msg) {
  const toast = document.createElement('div');
  toast.className = 'fixed top-16 right-4 z-50 bg-[#16A34A] text-white text-xs font-bold px-4 py-2.5 rounded-lg shadow-lg flex items-center gap-2 transform transition-all duration-300 translate-y-0 opacity-100';
  toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${msg}</span>`;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// Inicializar cálculo cuando el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById('calc-size')) {
    calculateWeight();
  }
});