// --- CONFIGURACIÓN DE LA API ---
const API_BASE_URL = window.location.origin + '/api';

// --- ESTADO DE LA APLICACIÓN ---
const state = {
  cart: [], // Array de { productId, storeId, quantity, price }
  compareList: [], // Array de productIds (máximo 3)
  activeTab: 'catalog-view',
  filters: {
    category: 'all',
    searchQuery: '',
    priceMin: null,
    priceMax: null,
    stores: [] // IDs de tiendas seleccionadas
  },
  sortBy: 'default',
  selectedStoreId: 'construmax', // Tienda activa en el localizador
  theme: 'dark',
  currentUser: null, // Usuario registrado/logueado
  selectedDistrict: 'Chiclayo',
  calculatedMaterials: []
};

// Tabla de pesos reales de los productos en kg
const PRODUCT_WEIGHTS = {
  1: 1.3,      // Taladro DeWalt
  2: 2.0,      // Amoladora Bosch
  3: 42.5,     // Cemento Pacasmayo Antisalitre
  4: 2.0,      // Varilla de Fierro 6mm (9m)
  5: 12.0,     // Cable THW Indeco
  6: 0.3,      // Interruptor Bticino
  7: 2.5,      // Mezcladora Vainsa
  8: 2.0,      // Tubo PVC SAP Pavco
  9: 5.0,      // Pintura CPP (Galón)
  10: 25.0,    // Yeso Pacasmayo (25kg)
  11: 2.0,     // Pala Redonda
  12: 15.0,    // Carretilla Buggy
  13: 0.8,     // Martillo Stanley
  14: 0.4,     // Wincha Métrica Stanley
  15: 1.2,     // Nivel de Burbuja Stanley
  16: 1.5,     // Llave Stilson Ridgid
  17: 0.9,     // Juego Destornilladores Stanley
  18: 8.0,     // Escalera Tijera Nexstep
  19: 1.0,     // Clavos Arequipa 3" (1kg)
  20: 1.0,     // Alambre Nro 16 (1kg)
  21: 2.8,     // Ladrillo KK 18 Huecos Lark (Unidad)
  22: 40.0,    // Arena Fina Bolsa (40kg)
  23: 40.0,    // Piedra Chancada Bolsa (40kg)
  24: 1.2,     // Aditivo Plastificante Chema
  25: 25.0,    // Pegamento Celima (25kg)
  26: 0.3,     // Tubo Abasto Vainsa
  27: 35.0,    // Inodoro Trebol
  28: 4.0,     // Cable de red Dixon
  29: 0.1,     // Cinta Aislante 3M
  30: 0.1,     // Caja Octogonal Pavco
  31: 0.3,     // Llave Termomagnética Bticino
  32: 0.4,     // Silicona Tekno
  33: 0.3,     // Rodillo Tekno
  34: 0.1,     // Brocha CPP 3"
  // --- Obra Gruesa ---
  35: 42.5,    // Cemento Pacasmayo Extra Forte
  36: 42.5,    // Cemento Pacasmayo Tipo I
  37: 42.5,    // Cemento Sol
  38: 42.5,    // Cemento Inka
  39: 2800.0,  // Ladrillo KK 18 Huecos (Millar)
  40: 2.1,     // Ladrillo Pandereta (Unidad)
  41: 2100.0,  // Ladrillo Pandereta (Millar)
  42: 8.0,     // Ladrillo Techo Hueco 15
  43: 7.0,     // Ladrillo Techo Hueco 12
  44: 4.5,     // Ladrillo Techo Hueco 8
  45: 2.0,     // Aceros Arequipa 6mm (9m)
  46: 3.6,     // Aceros Arequipa 8mm (9m)
  47: 5.0,     // Aceros Arequipa 3/8" (9m)
  48: 9.0,     // Aceros Arequipa 1/2" (9m)
  49: 14.0,    // Aceros Arequipa 5/8" (9m)
  50: 20.0,    // Aceros Arequipa 3/4" (9m)
  51: 2.0,     // Siderperu 6mm (9m)
  52: 3.6,     // Siderperu 8mm (9m)
  53: 5.0,     // Siderperu 3/8" (9m)
  54: 9.0,     // Siderperu 1/2" (9m)
  55: 14.0,    // Siderperu 5/8" (9m)
  56: 20.0,    // Siderperu 3/4" (9m)
  57: 1600.0,  // Arena Gruesa (m³)
  58: 1500.0,  // Arena Fina (m³)
  59: 1550.0,  // Piedra Chancada 1/2" (m³)
  60: 1550.0,  // Piedra Chancada 3/4" (m³)
  61: 1700.0,  // Hormigón (m³)
  62: 1800.0   // Afirmado (m³)
};

// Matriz de distancias en km a distritos de la Zona Norte
const DISTANCES = {
  construmax: {
    Chiclayo: 5.0,
    Pimentel: 15.0,
    Lambayeque: 12.0,
    Trujillo: 200.0,
    "Víctor Larco": 205.0,
    "El Porvenir": 202.0
  },
  ferretodo: {
    Chiclayo: 12.0,
    Pimentel: 22.0,
    Lambayeque: 3.0,
    Trujillo: 212.0,
    "Víctor Larco": 217.0,
    "El Porvenir": 214.0
  },
  depositoinca: {
    Chiclayo: 200.0,
    Pimentel: 210.0,
    Lambayeque: 208.0,
    Trujillo: 6.0,
    "Víctor Larco": 4.0,
    "El Porvenir": 10.0
  }
};

// Variables dinámicas cargadas del servidor
let STORES = {};
let PRODUCTS = [];
const productCache = new Map(); // Cache local para mantener todos los productos disponibles

// --- ELEMENTOS DEL DOM ---
const DOM = {
  themeToggle: document.getElementById('theme-toggle'),
  tabButtons: document.querySelectorAll('.tab-btn'),
  viewPanels: document.querySelectorAll('.view-panel'),
  logoHome: document.getElementById('logo-home'),
  searchInput: document.getElementById('search-input'),
  categoryList: document.getElementById('category-filter-list'),
  priceMin: document.getElementById('price-min'),
  priceMax: document.getElementById('price-max'),
  storeCheckboxesContainer: document.getElementById('store-checkboxes-container'),
  clearFiltersBtn: document.getElementById('clear-filters-btn'),
  resultsCount: document.getElementById('results-count'),
  sortSelect: document.getElementById('sort-select'),
  productsGrid: document.getElementById('products-grid'),
  globalCartCount: document.getElementById('global-cart-count'),
  
  // Modal
  productDetailModal: document.getElementById('product-detail-modal'),
  closeModalBtn: document.getElementById('close-modal-btn'),
  modalProductIcon: document.getElementById('modal-product-icon'),
  modalProductBrand: document.getElementById('modal-product-brand'),
  modalProductName: document.getElementById('modal-product-name'),
  modalProductDesc: document.getElementById('modal-product-desc'),
  modalSpecsTable: document.getElementById('modal-specs-table'),
  modalComparisonTbody: document.getElementById('modal-comparison-tbody'),
  
  // Tiendas
  storesListContainer: document.getElementById('stores-list-container'),
  mapStorePinsContainer: document.getElementById('map-store-pins-container'),
  mapCanvas: document.getElementById('map-canvas'),
  
  // Comparador
  compareTableWrapper: document.getElementById('compare-table-wrapper'),
  clearCompareBtn: document.getElementById('clear-compare-btn'),
  
  // Carrito
  cartGroupsContainer: document.getElementById('cart-groups-container'),
  cartSummaryDetails: document.getElementById('cart-summary-details'),
  checkoutBtn: document.getElementById('checkout-btn'),
  btnDownloadProforma: document.getElementById('btn-download-proforma'),
  
  // Toast
  toastContainer: document.getElementById('toast-container'),

  // Auth
  btnAuth: document.getElementById('btn-auth'),
  authModal: document.getElementById('auth-modal'),
  closeAuthModalBtn: document.getElementById('close-auth-modal-btn'),
  registerForm: document.getElementById('register-form'),

  // Calculadora
  calcType: document.getElementById('calc-type'),
  calcVolume: document.getElementById('calc-volume'),
  calcWallArea: document.getElementById('calc-wall-area'),
  calcRoofArea: document.getElementById('calc-roof-area'),
  calcResultsList: document.getElementById('calc-results-list'),
  btnAddCalcToCart: document.getElementById('btn-add-calc-to-cart'),

  // Selector flete
  cartDistrict: document.getElementById('cart-district')
};

// --- INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

// --- FUNCIÓN DE INICIALIZACIÓN ---
async function initApp() {
  initTheme();
  loadCartFromStorage();
  loadUserFromStorage();
  setupEventListeners();
  updateAuthButton();

  try {
    // 1. Obtener Tiendas
    const storesRes = await fetch(`${API_BASE_URL}/stores`);
    if (!storesRes.ok) throw new Error("No se pudo conectar al servidor de tiendas.");
    const storesList = await storesRes.json();
    
    STORES = {};
    storesList.forEach(s => {
      STORES[s.id] = s;
    });

    // 2. Poblar la cache inicial cargando todos los productos
    const prodsRes = await fetch(`${API_BASE_URL}/products`);
    if (prodsRes.ok) {
      const allProds = await prodsRes.json();
      allProds.forEach(p => productCache.set(p.id, p));
    }

    // 3. Renderizar vista de filtros y catálogo
    renderStoreCheckboxes();
    await loadAndRenderCatalog();

    renderStoresView();
    renderCartView();
    renderCompareView();
    updateCartBadge();

  } catch (err) {
    console.error("Error al inicializar la aplicación:", err);
    showToast("Error de conexión. Asegúrate de que el Backend de FastAPI esté corriendo.", "warning");
  }
}

// --- TEMA CLARO/OSCURO ---
function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  state.theme = savedTheme;
  document.documentElement.setAttribute('data-theme', savedTheme);
  DOM.themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', state.theme);
  localStorage.setItem('theme', state.theme);
  DOM.themeToggle.textContent = state.theme === 'dark' ? '☀️' : '🌙';
  showToast(`Modo ${state.theme === 'dark' ? 'oscuro' : 'claro'} activado`, 'info');
}

// --- GESTIÓN DE NOTIFICACIONES TOAST ---
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let icon = '🔔';
  if (type === 'success') icon = '✅';
  if (type === 'info') icon = 'ℹ️';
  if (type === 'warning') icon = '⚠️';
  
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  DOM.toastContainer.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease reverse forwards';
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, 3000);
}

// --- UTILERÍAS ---
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// --- PERSISTENCIA LOCAL DEL CARRITO ---
function loadCartFromStorage() {
  const saved = localStorage.getItem('obraexpres_cart');
  if (saved) {
    try {
      state.cart = JSON.parse(saved);
    } catch (e) {
      state.cart = [];
    }
  }
}

function saveCartToStorage() {
  localStorage.setItem('obraexpres_cart', JSON.stringify(state.cart));
}

// --- CONFIGURACIÓN DE EVENT LISTENERS ---
function setupEventListeners() {
  // Theme Toggle
  DOM.themeToggle.addEventListener('click', toggleTheme);

  // SPA Router Tabs
  DOM.tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-target');
      switchTab(target);
    });
  });

  DOM.logoHome.addEventListener('click', (e) => {
    e.preventDefault();
    switchTab('catalog-view');
  });

  // Búsqueda en tiempo real con debounce
  DOM.searchInput.addEventListener('input', debounce((e) => {
    state.filters.searchQuery = e.target.value.toLowerCase().trim();
    loadAndRenderCatalog();
  }, 300));

  // Filtro de categorías
  DOM.categoryList.addEventListener('click', (e) => {
    const item = e.target.closest('.category-item');
    if (!item) return;

    document.querySelectorAll('.category-item').forEach(el => el.classList.remove('active'));
    item.classList.add('active');

    state.filters.category = item.getAttribute('data-category');
    loadAndRenderCatalog();
  });

  // Filtro de precios con debounce
  DOM.priceMin.addEventListener('input', debounce((e) => {
    state.filters.priceMin = e.target.value ? parseFloat(e.target.value) : null;
    loadAndRenderCatalog();
  }, 400));
  
  DOM.priceMax.addEventListener('input', debounce((e) => {
    state.filters.priceMax = e.target.value ? parseFloat(e.target.value) : null;
    loadAndRenderCatalog();
  }, 400));

  // Ordenación
  DOM.sortSelect.addEventListener('change', (e) => {
    state.sortBy = e.target.value;
    loadAndRenderCatalog();
  });

  // Limpiar filtros
  DOM.clearFiltersBtn.addEventListener('click', async () => {
    DOM.searchInput.value = '';
    DOM.priceMin.value = '';
    DOM.priceMax.value = '';
    DOM.sortSelect.value = 'default';
    state.filters.searchQuery = '';
    state.filters.priceMin = null;
    state.filters.priceMax = null;
    state.sortBy = 'default';
    
    // reset categories
    document.querySelectorAll('.category-item').forEach(el => el.classList.remove('active'));
    document.querySelector('[data-category="all"]').classList.add('active');
    state.filters.category = 'all';

    // reset checkboxes
    document.querySelectorAll('.store-filter-checkbox').forEach(cb => cb.checked = true);
    state.filters.stores = Object.keys(STORES);

    await loadAndRenderCatalog();
    showToast('Filtros restablecidos', 'info');
  });

  // Cerrar Modal
  DOM.closeModalBtn.addEventListener('click', () => {
    DOM.productDetailModal.classList.remove('active');
  });
  DOM.productDetailModal.addEventListener('click', (e) => {
    if (e.target === DOM.productDetailModal) {
      DOM.productDetailModal.classList.remove('active');
    }
  });

  // Comparador vaciar
  DOM.clearCompareBtn.addEventListener('click', () => {
    state.compareList = [];
    renderCompareView();
    showToast('Comparador vaciado', 'info');
  });

  // Checkout Simulación
  DOM.checkoutBtn.addEventListener('click', async () => {
    if (state.cart.length === 0) {
      showToast('El carrito está vacío', 'warning');
      return;
    }
    
    const checkoutData = {
      items: state.cart.map(item => ({
        productId: parseInt(item.productId),
        storeId: item.storeId,
        quantity: parseInt(item.quantity),
        price: parseFloat(item.price)
      })),
      district: state.selectedDistrict
    };

    try {
      DOM.checkoutBtn.disabled = true;
      DOM.checkoutBtn.textContent = 'Procesando Compra...';

      const res = await fetch(`${API_BASE_URL}/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(checkoutData)
      });

      if (!res.ok) {
        const errorDetails = await res.json();
        throw new Error(errorDetails.detail || 'Error en el checkout');
      }

      const order = await res.json();
      
      showToast(`¡Pedido #${order.id} procesado con éxito! Total: S/. ${order.total.toFixed(2)}`, 'success');
      
      // Limpiar carrito
      state.cart = [];
      saveCartToStorage();
      updateCartBadge();
      renderCartView();
      switchTab('catalog-view');

      // Volver a cargar el catálogo por si cambió el stock
      await loadAndRenderCatalog();

    } catch (err) {
      console.error(err);
      showToast(err.message, 'warning');
    } finally {
      DOM.checkoutBtn.disabled = false;
      DOM.checkoutBtn.innerHTML = '💳 Procesar Compra en ObraExpres';
    }
  });

  // Descargar Proforma PDF
  if (DOM.btnDownloadProforma) {
    DOM.btnDownloadProforma.addEventListener('click', () => {
      generateProformaPDF();
    });
  }

  // Auth Modal toggles
  if (DOM.btnAuth) {
    DOM.btnAuth.addEventListener('click', () => {
      if (state.currentUser) {
        state.currentUser = null;
        localStorage.removeItem('obraexpres_user');
        updateAuthButton();
        showToast('Sesión cerrada correctamente', 'info');
      } else {
        DOM.authModal.classList.add('active');
      }
    });
  }

  if (DOM.closeAuthModalBtn) {
    DOM.closeAuthModalBtn.addEventListener('click', () => {
      DOM.authModal.classList.remove('active');
    });
  }

  if (DOM.authModal) {
    DOM.authModal.addEventListener('click', (e) => {
      if (e.target === DOM.authModal) {
        DOM.authModal.classList.remove('active');
      }
    });
  }

  // Auth Form Submit
  if (DOM.registerForm) {
    DOM.registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const payload = {
        full_name: document.getElementById('reg-name').value,
        email: document.getElementById('reg-email').value,
        phone: document.getElementById('reg-phone').value,
        role: document.getElementById('reg-role').value,
        password: document.getElementById('reg-password').value
      };

      try {
        const res = await fetch(`${API_BASE_URL}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.detail || 'Error al registrarse');
        }

        const user = await res.json();
        state.currentUser = user;
        localStorage.setItem('obraexpres_user', JSON.stringify(user));
        
        showToast(`¡Registro exitoso! Bienvenido ${user.full_name}`, 'success');
        DOM.authModal.classList.remove('active');
        DOM.registerForm.reset();
        updateAuthButton();
        
      } catch (err) {
        console.error(err);
        showToast(err.message, 'warning');
      }
    });
  }

  // Calculator inputs change
  if (DOM.calcType) {
    DOM.calcType.addEventListener('change', renderCalculatorView);
  }
  if (DOM.calcVolume) {
    DOM.calcVolume.addEventListener('input', renderCalculatorView);
  }
  if (DOM.calcWallArea) {
    DOM.calcWallArea.addEventListener('input', renderCalculatorView);
  }
  if (DOM.calcRoofArea) {
    DOM.calcRoofArea.addEventListener('input', renderCalculatorView);
  }
  if (DOM.btnAddCalcToCart) {
    DOM.btnAddCalcToCart.addEventListener('click', addCalculatedMaterialsToCart);
  }

  // Cart district change
  if (DOM.cartDistrict) {
    DOM.cartDistrict.addEventListener('change', (e) => {
      state.selectedDistrict = e.target.value;
      renderCartView();
    });
  }
}

// --- SWITCH TAB (Navegación SPA) ---
function switchTab(targetViewId) {
  state.activeTab = targetViewId;

  // Actualizar botones de navegación
  DOM.tabButtons.forEach(btn => {
    if (btn.getAttribute('data-target') === targetViewId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  // Mostrar panel correcto
  DOM.viewPanels.forEach(panel => {
    if (panel.id === targetViewId) {
      panel.classList.add('active');
    } else {
      panel.classList.remove('active');
    }
  });

  // Cargar/renderizar datos específicos
  if (targetViewId === 'compare-view') {
    renderCompareView();
  } else if (targetViewId === 'cart-view') {
    renderCartView();
  } else if (targetViewId === 'stores-view') {
    renderStoresView();
  } else if (targetViewId === 'calculator-view') {
    renderCalculatorView();
  }
}

// --- RENDERIZADO DE FILTROS DE TIENDA (CHECKBOXES) ---
function renderStoreCheckboxes() {
  DOM.storeCheckboxesContainer.innerHTML = '';
  state.filters.stores = Object.keys(STORES);

  Object.values(STORES).forEach(store => {
    const label = document.createElement('label');
    label.className = 'checkbox-label';
    label.innerHTML = `
      <input type="checkbox" class="store-filter-checkbox" value="${store.id}" checked>
      <span class="store-badge">
        <span class="store-color-dot" style="background-color: ${store.color}"></span>
        ${store.name}
      </span>
    `;
    
    const checkbox = label.querySelector('input');
    checkbox.addEventListener('change', async () => {
      const activeCheckboxes = Array.from(document.querySelectorAll('.store-filter-checkbox'))
        .filter(cb => cb.checked)
        .map(cb => cb.value);
      state.filters.stores = activeCheckboxes;
      await loadAndRenderCatalog();
    });

    DOM.storeCheckboxesContainer.appendChild(label);
  });
}

// --- CARGAR PRODUCTOS DESDE EL BACKEND ---
async function fetchProducts() {
  const params = new URLSearchParams();
  if (state.filters.category && state.filters.category !== 'all') {
    params.append('category', state.filters.category);
  }
  if (state.filters.searchQuery) {
    params.append('search', state.filters.searchQuery);
  }
  if (state.filters.priceMin !== null) {
    params.append('min_price', state.filters.priceMin);
  }
  if (state.filters.priceMax !== null) {
    params.append('max_price', state.filters.priceMax);
  }
  if (state.filters.stores && state.filters.stores.length > 0) {
    params.append('store_ids', state.filters.stores.join(','));
  }
  if (state.sortBy) {
    params.append('sort_by', state.sortBy);
  }

  try {
    const res = await fetch(`${API_BASE_URL}/products?${params.toString()}`);
    if (!res.ok) throw new Error("Error en la llamada a productos.");
    PRODUCTS = await res.json();
    
    // Guardar en la cache local
    PRODUCTS.forEach(p => productCache.set(p.id, p));
  } catch (err) {
    console.error(err);
    showToast("Error al obtener catálogo del servidor", "warning");
  }
}

async function loadAndRenderCatalog() {
  await fetchProducts();
  renderCatalog();
}

// --- RENDERIZADO DEL CATÁLOGO DE PRODUCTOS ---
function renderCatalog() {
  DOM.productsGrid.innerHTML = '';
  DOM.resultsCount.textContent = `Mostrando ${PRODUCTS.length} productos`;

  if (PRODUCTS.length === 0) {
    DOM.productsGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="empty-state-icon">🔍</div>
        <h3>No se encontraron productos</h3>
        <p>Intenta cambiar los filtros o el término de búsqueda.</p>
      </div>
    `;
    return;
  }

  PRODUCTS.forEach(product => {
    // Ofertas válidas según los filtros de tienda seleccionados localmente
    const activeOffers = product.stores.filter(s => state.filters.stores.includes(s.storeId));
    if (activeOffers.length === 0) return;

    const prices = activeOffers.map(o => o.price);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    
    // Encontrar oferta barata
    const bestOffer = activeOffers.find(o => o.price === minPrice);
    const bestStore = STORES[bestOffer.storeId];

    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <div class="product-badge">${product.category}</div>
      <div class="product-card-icon">${product.icon}</div>
      <div class="product-info">
        <span class="product-brand">${product.brand}</span>
        <h3 class="product-title" data-id="${product.id}">${product.name}</h3>
        
        <div class="store-comparison-summary">
          <div class="summary-row">
            <span>Rango:</span>
            <span class="price-range">S/. ${minPrice.toFixed(2)} - S/. ${maxPrice.toFixed(2)}</span>
          </div>
          <div class="summary-row" style="margin-top: 0.25rem;">
            <span>Mejor opción:</span>
            <span class="cheapest-label">${bestStore.logo} ${bestStore.name} (S/. ${bestOffer.price.toFixed(2)})</span>
          </div>
        </div>
      </div>
      <div class="card-footer">
        <button class="btn btn-primary btn-compare" data-id="${product.id}">
          ⚖️ Ver Ofertas
        </button>
        <button class="btn btn-secondary btn-add-compare" data-id="${product.id}" title="Comparar con otros">
          ➕ Comparador
        </button>
      </div>
    `;

    // Click abre modal
    const triggerModal = () => openProductDetailModal(product.id);
    card.querySelector('.product-title').addEventListener('click', triggerModal);
    card.querySelector('.btn-compare').addEventListener('click', triggerModal);

    // Click añade a comparador
    card.querySelector('.btn-add-compare').addEventListener('click', () => {
      addToCompareList(product.id);
    });

    DOM.productsGrid.appendChild(card);
  });
}

// --- DETALLE DE PRODUCTO Y COMPARATIVA (MODAL) ---
function openProductDetailModal(productId) {
  const product = productCache.get(productId);
  if (!product) return;

  // Llenar datos básicos del modal
  DOM.modalProductIcon.textContent = product.icon;
  DOM.modalProductBrand.textContent = product.brand;
  DOM.modalProductName.textContent = product.name;
  DOM.modalProductDesc.textContent = product.description;

  // Llenar Ficha Técnica
  DOM.modalSpecsTable.innerHTML = '';
  Object.entries(product.specs).forEach(([specName, specVal]) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${specName}</td>
      <td>${specVal}</td>
    `;
    DOM.modalSpecsTable.appendChild(row);
  });

  // Llenar Comparativa de tiendas
  DOM.modalComparisonTbody.innerHTML = '';
  
  const sortedOffers = [...product.stores].sort((a, b) => a.price - b.price);
  const minPrice = sortedOffers.length > 0 ? sortedOffers[0].price : 0;

  sortedOffers.forEach(offer => {
    const store = STORES[offer.storeId];
    if (!store) return;
    const isBest = offer.price === minPrice;
    
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>
        <div class="store-badge">
          <span class="store-color-dot" style="background-color: ${store.color}"></span>
          <span style="font-size: 1.2rem;">${store.logo}</span>
          <span>${store.name}</span>
        </div>
      </td>
      <td>
        <span class="price-tag ${isBest ? 'best' : ''}">S/. ${offer.price.toFixed(2)}</span>
      </td>
      <td>
        <span class="stock-tag ${offer.stock > 5 ? 'in-stock' : 'low-stock'}">
          ${offer.stock > 0 ? `En stock (${offer.stock} uds)` : 'Agotado'}
        </span>
      </td>
      <td style="font-size: 0.9rem; color: var(--text-secondary);">
        🚗 ${offer.deliveryTime}
      </td>
      <td>
        <button class="btn btn-primary btn-add-cart" data-store="${offer.storeId}" ${offer.stock === 0 ? 'disabled' : ''} style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">
          🛒 Comprar
        </button>
      </td>
    `;

    // Evento comprar en esta tienda
    row.querySelector('.btn-add-cart').addEventListener('click', () => {
      addToCart(product.id, offer.storeId, offer.price);
      DOM.productDetailModal.classList.remove('active');
    });

    DOM.modalComparisonTbody.appendChild(row);
  });

  DOM.productDetailModal.classList.add('active');
}

// --- CARRITO DE COMPRAS ---
function addToCart(productId, storeId, price) {
  const existing = state.cart.find(item => item.productId === productId && item.storeId === storeId);
  
  if (existing) {
    existing.quantity += 1;
  } else {
    state.cart.push({ productId, storeId, quantity: 1, price });
  }

  const product = productCache.get(productId);
  const store = STORES[storeId];
  
  saveCartToStorage();
  updateCartBadge();
  showToast(`Añadido: ${product.name} en ${store.name}`, 'success');
}

function updateCartBadge() {
  const totalQty = state.cart.reduce((acc, curr) => acc + curr.quantity, 0);
  DOM.globalCartCount.textContent = totalQty;
}

function renderCartView() {
  DOM.cartGroupsContainer.innerHTML = '';
  DOM.cartSummaryDetails.innerHTML = '';

  if (state.cart.length === 0) {
    DOM.cartGroupsContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🛒</div>
        <h3>Tu carrito está vacío</h3>
        <p>Busca materiales en el catálogo y compáralos para añadirlos.</p>
        <button class="btn btn-primary" id="go-to-catalog-btn" style="margin-top: 1rem; display: inline-flex; width: auto;">
          Ir al Catálogo
        </button>
      </div>
    `;
    
    const goCatalogBtn = document.getElementById('go-to-catalog-btn');
    if (goCatalogBtn) {
      goCatalogBtn.addEventListener('click', () => switchTab('catalog-view'));
    }

    DOM.cartSummaryDetails.innerHTML = `
      <div class="summary-detail-row">
        <span>Subtotal (sin IGV)</span>
        <span>S/. 0.00</span>
      </div>
      <div class="summary-detail-row">
        <span>IGV (18%)</span>
        <span>S/. 0.00</span>
      </div>
      <div class="summary-detail-row">
        <span>Envío (0 Tiendas)</span>
        <span>S/. 0.00</span>
      </div>
      <div class="summary-detail-row total">
        <span>Total</span>
        <span>S/. 0.00</span>
      </div>
    `;
    
    DOM.checkoutBtn.disabled = true;
    return;
  }

  DOM.checkoutBtn.disabled = false;

  // Agrupar items por tienda
  const grouped = {};
  state.cart.forEach(item => {
    if (!grouped[item.storeId]) {
      grouped[item.storeId] = [];
    }
    grouped[item.storeId].push(item);
  });

  let subtotalGeneral = 0;
  let envioGeneral = 0;
  let pesoGeneral = 0;

  Object.entries(grouped).forEach(([storeId, items]) => {
    const store = STORES[storeId];
    if (!store) return;
    let subtotalTienda = 0;
    let pesoTienda = 0;

    items.forEach(item => {
      const itemWeight = (PRODUCT_WEIGHTS[item.productId] || 2.0) * item.quantity;
      pesoTienda += itemWeight;
    });

    const distancia = DISTANCES[storeId][state.selectedDistrict] || 10.0;
    let fleteTienda = 0;
    if (pesoTienda <= 500) {
      fleteTienda = distancia * 2.0;
      fleteTienda = Math.max(fleteTienda, 10.0);
    } else {
      fleteTienda = 50.0 + (distancia * 5.0);
    }

    const groupDiv = document.createElement('div');
    groupDiv.className = 'store-cart-group';
    
    const header = document.createElement('div');
    header.className = 'store-cart-header';
    header.innerHTML = `
      <h3>
        <span>${store.logo}</span>
        <span>${store.name}</span>
      </h3>
      <span style="font-size: 0.85rem; color: var(--text-secondary); text-align: right; line-height: 1.3;">
        Envío: S/. ${fleteTienda.toFixed(2)} | Distancia: ${distancia} km | Peso: ${pesoTienda.toFixed(1)} kg ${pesoTienda > 500 ? '🚛' : '🚗'}
      </span>
    `;
    groupDiv.appendChild(header);

    items.forEach(item => {
      const product = productCache.get(item.productId);
      if (!product) return;
      
      const totalItemPrice = item.price * item.quantity;
      subtotalTienda += totalItemPrice;

      const itemRow = document.createElement('div');
      itemRow.className = 'cart-item';
      itemRow.innerHTML = `
        <div class="cart-item-icon">${product.icon}</div>
        <div class="cart-item-info">
          <h4>${product.name}</h4>
          <p>${product.brand}</p>
        </div>
        <div class="cart-quantity">
          <button class="qty-btn dec-qty" data-prod="${item.productId}" data-store="${item.storeId}">-</button>
          <span style="font-weight:700; width:20px; text-align:center;">${item.quantity}</span>
          <button class="qty-btn inc-qty" data-prod="${item.productId}" data-store="${item.storeId}">+</button>
        </div>
        <div class="cart-item-price">S/. ${totalItemPrice.toFixed(2)}</div>
        <button class="remove-compare-btn remove-cart-item" data-prod="${item.productId}" data-store="${item.storeId}">
          ✕
        </button>
      `;

      // Eventos de cantidad
      itemRow.querySelector('.inc-qty').addEventListener('click', () => {
        changeCartQty(item.productId, item.storeId, 1);
      });
      itemRow.querySelector('.dec-qty').addEventListener('click', () => {
        changeCartQty(item.productId, item.storeId, -1);
      });
      itemRow.querySelector('.remove-cart-item').addEventListener('click', () => {
        removeCartItem(item.productId, item.storeId);
      });

      groupDiv.appendChild(itemRow);
    });

    const footer = document.createElement('div');
    footer.style.display = 'flex';
    footer.style.justifyContent = 'flex-end';
    footer.style.marginTop = '1rem';
    footer.style.fontSize = '0.95rem';
    footer.style.fontWeight = '700';
    footer.innerHTML = `Subtotal Tienda: S/. ${subtotalTienda.toFixed(2)}`;
    groupDiv.appendChild(footer);

    DOM.cartGroupsContainer.appendChild(groupDiv);

    subtotalGeneral += subtotalTienda;
    envioGeneral += fleteTienda;
    pesoGeneral += pesoTienda;
  });

  const numStores = Object.keys(grouped).length;
  const subtotalNeto = subtotalGeneral / 1.18;
  const igv = subtotalGeneral - subtotalNeto;
  const totalConEnvio = subtotalGeneral + envioGeneral;

  DOM.cartSummaryDetails.innerHTML = `
    <div class="summary-detail-row">
      <span>Subtotal (sin IGV)</span>
      <span>S/. ${subtotalNeto.toFixed(2)}</span>
    </div>
    <div class="summary-detail-row">
      <span>IGV (18%)</span>
      <span>S/. ${igv.toFixed(2)}</span>
    </div>
    <div class="summary-detail-row">
      <span>Cargos de Envío (${numStores} ${numStores === 1 ? 'tienda' : 'tiendas'})</span>
      <span>S/. ${envioGeneral.toFixed(2)}</span>
    </div>
    <div class="summary-detail-row" style="border-top: 1px dashed var(--border-color); padding-top: 0.5rem; margin-top: 0.5rem;">
      <span>Peso Total</span>
      <span style="font-weight: 700;">${pesoGeneral.toFixed(1)} kg ${pesoGeneral > 500 ? '<span style="color:var(--primary); font-size:0.85rem; display:block;">🚛 Carga Pesada (Camión)</span>' : ''}</span>
    </div>
    <div class="summary-detail-row total">
      <span>Total de Compra</span>
      <span>S/. ${totalConEnvio.toFixed(2)}</span>
    </div>
    <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.75rem; text-align: left; line-height: 1.35;">
      * Nota: Los precios mostrados incluyen el IGV (18%). El flete se calcula dinámicamente según la distancia a <strong>${state.selectedDistrict}</strong> y el peso total.
    </p>
  `;
}

function changeCartQty(productId, storeId, delta) {
  const item = state.cart.find(i => i.productId === productId && i.storeId === storeId);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    removeCartItem(productId, storeId);
  } else {
    saveCartToStorage();
    updateCartBadge();
    renderCartView();
  }
}

function removeCartItem(productId, storeId) {
  state.cart = state.cart.filter(i => !(i.productId === productId && i.storeId === storeId));
  saveCartToStorage();
  updateCartBadge();
  renderCartView();
  showToast('Producto removido del carrito', 'warning');
}

// --- COMPARADOR DIRECTO DE PRODUCTOS ---
function addToCompareList(productId) {
  if (state.compareList.includes(productId)) {
    showToast('Este producto ya está en el comparador', 'warning');
    return;
  }
  if (state.compareList.length >= 3) {
    showToast('Solo puedes comparar hasta 3 productos a la vez', 'warning');
    return;
  }

  state.compareList.push(productId);
  showToast('Producto añadido al comparador', 'success');
  renderCompareView();
}

function renderCompareView() {
  DOM.compareTableWrapper.innerHTML = '';

  if (state.compareList.length === 0) {
    DOM.compareTableWrapper.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">⚖️</div>
        <h3>El comparador está vacío</h3>
        <p>Añade productos desde el catálogo presionando el botón "➕ Comparador".</p>
      </div>
    `;
    return;
  }

  const comparedProds = state.compareList.map(id => productCache.get(id)).filter(Boolean);
  
  const grid = document.createElement('div');
  grid.className = 'compare-grid';
  grid.style.gridTemplateColumns = `200px repeat(${comparedProds.length}, 1fr)`;

  const labelCol = document.createElement('div');
  labelCol.className = 'compare-col';
  labelCol.innerHTML = `
    <div class="compare-cell header label">Ficha de Comparación</div>
    <div class="compare-cell label">Categoría</div>
    <div class="compare-cell label">Marca</div>
    <div class="compare-cell label">Detalles Técnicos</div>
    <div class="compare-cell label">Precio ConstruMax</div>
    <div class="compare-cell label">Precio Ferretodo Lambayeque</div>
    <div class="compare-cell label">Precio Depósito El Inca</div>
  `;
  grid.appendChild(labelCol);

  comparedProds.forEach(prod => {
    const col = document.createElement('div');
    col.className = 'compare-col';
    
    const getStorePrice = (sId) => {
      const offer = prod.stores.find(s => s.storeId === sId);
      return offer ? `S/. ${offer.price.toFixed(2)}` : '<span style="color:var(--text-muted)">No disponible</span>';
    };

    const specsList = Object.entries(prod.specs)
      .map(([k, v]) => `• <strong>${k}:</strong> ${v}`)
      .join('<br>');

    col.innerHTML = `
      <div class="compare-cell header product-card-cell">
        <span style="font-size: 2.2rem;">${prod.icon}</span>
        <h4 style="font-size: 0.95rem; margin: 0.35rem 0 0.15rem 0; font-family: var(--font-title); font-weight:800;">${prod.name}</h4>
        <button class="remove-compare-btn remove-compare-prod" data-id="${prod.id}">Eliminar</button>
      </div>
      <div class="compare-cell">${prod.category}</div>
      <div class="compare-cell" style="font-weight:700;">${prod.brand}</div>
      <div class="compare-cell" style="font-size: 0.8rem; line-height: 1.4; display:block; padding: 0.75rem;">${specsList}</div>
      <div class="compare-cell">${getStorePrice('construmax')}</div>
      <div class="compare-cell">${getStorePrice('ferretodo')}</div>
      <div class="compare-cell">${getStorePrice('depositoinca')}</div>
    `;

    col.querySelector('.remove-compare-prod').addEventListener('click', () => {
      state.compareList = state.compareList.filter(id => id !== prod.id);
      renderCompareView();
      showToast('Producto eliminado del comparador', 'warning');
    });

    grid.appendChild(col);
  });

  DOM.compareTableWrapper.appendChild(grid);
}

// --- TIENDAS Y MAPA INTERACTIVO ---
function renderStoresView() {
  DOM.storesListContainer.innerHTML = '';
  DOM.mapStorePinsContainer.innerHTML = '';

  Object.values(STORES).forEach(store => {
    // 1. Tarjeta de tienda
    const card = document.createElement('div');
    card.className = `store-card ${state.selectedStoreId === store.id ? 'selected' : ''}`;
    card.innerHTML = `
      <div class="store-card-icon">${store.logo}</div>
      <div class="store-card-info">
        <h3>${store.name}</h3>
        <div class="store-meta">
          <span class="rating-stars">★ ${store.rating}</span>
          <span>(${store.reviews} opiniones)</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">📍 ${store.address}</p>
        <p style="font-size: 0.85rem; color: var(--text-secondary); font-weight: 500;">⏰ ${store.hours}</p>
      </div>
    `;

    card.addEventListener('click', () => {
      selectStore(store.id);
    });

    DOM.storesListContainer.appendChild(card);

    // 2. Pin del mapa
    const pin = document.createElement('div');
    pin.className = `map-store-pin ${state.selectedStoreId === store.id ? 'active' : ''}`;
    pin.style.left = `${store.coords.x}%`;
    pin.style.top = `${store.coords.y}%`;
    pin.style.borderColor = store.color;
    pin.innerHTML = store.logo;
    pin.title = store.name;

    pin.addEventListener('click', () => {
      selectStore(store.id);
      showToast(`Ubicación seleccionada: ${store.name}`, 'info');
    });

    DOM.mapStorePinsContainer.appendChild(pin);
  });
}

function selectStore(storeId) {
  state.selectedStoreId = storeId;
  
  const cards = DOM.storesListContainer.querySelectorAll('.store-card');
  const storeIds = Object.keys(STORES);
  
  cards.forEach((card, idx) => {
    const sId = storeIds[idx];
    if (sId === storeId) {
      card.classList.add('selected');
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
      card.classList.remove('selected');
    }
  });

  const pins = DOM.mapStorePinsContainer.querySelectorAll('.map-store-pin');
  pins.forEach((pin, idx) => {
    const sId = storeIds[idx];
    if (sId === storeId) {
      pin.classList.add('active');
    } else {
      pin.classList.remove('active');
    }
  });
}

function loadUserFromStorage() {
  const saved = localStorage.getItem('obraexpres_user');
  if (saved) {
    try {
      state.currentUser = JSON.parse(saved);
    } catch (e) {
      state.currentUser = null;
    }
  }
}

function updateAuthButton() {
  if (!DOM.btnAuth) return;
  if (state.currentUser) {
    DOM.btnAuth.innerHTML = `👋 Hola, ${state.currentUser.full_name.split(' ')[0]} (${state.currentUser.role})`;
    DOM.btnAuth.title = "Hacer clic para cerrar sesión";
    DOM.btnAuth.classList.remove('btn-primary');
    DOM.btnAuth.classList.add('btn-secondary');
  } else {
    DOM.btnAuth.innerHTML = `👤 Iniciar Sesión`;
    DOM.btnAuth.title = "Hacer clic para registrarse o iniciar sesión";
    DOM.btnAuth.classList.remove('btn-secondary');
    DOM.btnAuth.classList.add('btn-primary');
  }
}

// --- LÓGICA DE LA CALCULADORA DE OBRA ---
function renderCalculatorView() {
  const type = DOM.calcType.value;
  
  // Mostrar/Ocultar campos correspondientes
  document.getElementById('input-concreto').style.display = type === 'concreto' ? 'block' : 'none';
  document.getElementById('input-muro').style.display = type === 'muro' ? 'block' : 'none';
  document.getElementById('input-techo').style.display = type === 'techo' ? 'block' : 'none';

  let estimation = [];

  if (type === 'concreto') {
    const vol = parseFloat(DOM.calcVolume.value) || 0;
    if (vol > 0) {
      estimation = [
        { productId: 36, name: "Cemento Pacasmayo Tipo I (Bolsa 42.5 kg)", quantity: Math.ceil(vol * 9.7), unit: "bolsas" },
        { productId: 57, name: "Arena Gruesa por Metro Cúbico (m³)", quantity: Math.ceil(vol * 0.52), unit: "m³" },
        { productId: 59, name: "Piedra Chancada de 1/2\" por Metro Cúbico (m³)", quantity: Math.ceil(vol * 0.53), unit: "m³" }
      ];
    }
  } else if (type === 'muro') {
    const area = parseFloat(DOM.calcWallArea.value) || 0;
    if (area > 0) {
      const brickQty = Math.ceil(area * 40);
      const millares = (brickQty / 1000).toFixed(2);
      estimation = [
        { productId: 21, name: `Ladrillo King Kong 18 Huecos Lark (Unidad) [${millares} millares]`, quantity: brickQty, unit: "unidades" },
        { productId: 36, name: "Cemento Pacasmayo Tipo I (Bolsa 42.5 kg)", quantity: Math.ceil(area * 0.15), unit: "bolsas" },
        { productId: 57, name: "Arena Gruesa por Metro Cúbico (m³)", quantity: Math.ceil(area * 0.025), unit: "m³" }
      ];
    }
  } else if (type === 'techo') {
    const area = parseFloat(DOM.calcRoofArea.value) || 0;
    if (area > 0) {
      estimation = [
        { productId: 42, name: "Ladrillo de Techo Hueco 15 Lark (Unidad)", quantity: Math.ceil(area * 8.33), unit: "unidades" },
        { productId: 36, name: "Cemento Pacasmayo Tipo I (Bolsa 42.5 kg)", quantity: Math.ceil(area * 0.28), unit: "bolsas" },
        { productId: 57, name: "Arena Gruesa por Metro Cúbico (m³)", quantity: Math.ceil(area * 0.04), unit: "m³" },
        { productId: 59, name: "Piedra Chancada de 1/2\" por Metro Cúbico (m³)", quantity: Math.ceil(area * 0.04), unit: "m³" },
        { productId: 48, name: "Varilla de Acero Corrugado Aceros Arequipa 1/2\" (9m)", quantity: Math.ceil(area * 1.5), unit: "varillas" },
        { productId: 45, name: "Varilla de Acero Corrugado Aceros Arequipa 6mm (9m)", quantity: Math.ceil(area * 0.2), unit: "varillas" }
      ];
    }
  }

  state.calculatedMaterials = estimation;

  DOM.calcResultsList.innerHTML = '';
  if (estimation.length === 0) {
    DOM.calcResultsList.innerHTML = `<p style="color:var(--text-muted); text-align:center;">Ingresa un valor válido para calcular.</p>`;
    DOM.btnAddCalcToCart.disabled = true;
    return;
  }

  DOM.btnAddCalcToCart.disabled = false;
  estimation.forEach(item => {
    const div = document.createElement('div');
    div.style.display = 'flex';
    div.style.justifyContent = 'space-between';
    div.style.padding = '0.5rem 0';
    div.style.borderBottom = '1px dashed var(--border-color)';
    div.innerHTML = `
      <span style="font-weight: 500; color: var(--text-primary); font-size: 0.95rem;">${item.name}</span>
      <span style="font-weight: 700; color: var(--primary);">${item.quantity} ${item.unit}</span>
    `;
    DOM.calcResultsList.appendChild(div);
  });
}

async function addCalculatedMaterialsToCart() {
  if (state.calculatedMaterials.length === 0) return;

  for (const item of state.calculatedMaterials) {
    let cachedProduct = productCache.get(item.productId);
    
    if (!cachedProduct) {
      try {
        const res = await fetch(`${API_BASE_URL}/products`);
        if (res.ok) {
          const prods = await res.json();
          prods.forEach(p => productCache.set(p.id, p));
          cachedProduct = productCache.get(item.productId);
        }
      } catch (e) {
        console.error(e);
      }
    }

    if (cachedProduct && cachedProduct.stores && cachedProduct.stores.length > 0) {
      const sortedOffers = [...cachedProduct.stores].sort((a, b) => a.price - b.price);
      const bestOffer = sortedOffers[0];
      
      addToCartWithQty(item.productId, bestOffer.storeId, bestOffer.price, item.quantity);
    }
  }

  showToast("Materiales estimados agregados al carrito (al mejor precio)", "success");
  switchTab('cart-view');
}

function addToCartWithQty(productId, storeId, price, quantity) {
  const existing = state.cart.find(item => item.productId === productId && item.storeId === storeId);
  
  if (existing) {
    existing.quantity += quantity;
  } else {
    state.cart.push({ productId, storeId, quantity, price });
  }
  saveCartToStorage();
  updateCartBadge();
}

// --- FUNCIONES GENERADORAS DE PDF (PROFORMA) ---

function addBusinessDays(date, days) {
  let result = new Date(date);
  let addedDays = 0;
  while (addedDays < days) {
    result.setDate(result.getDate() + 1);
    const dayOfWeek = result.getDay();
    if (dayOfWeek !== 0 && dayOfWeek !== 6) { // 0: Domingo, 6: Sábado
      addedDays++;
    }
  }
  return result;
}

function formatDate(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}

function getProductUnit(product) {
  if (!product) return 'Unidad';
  const name = product.name || '';
  const category = product.category || '';
  const specs = product.specs || {};

  // Deducir unidades según el nombre y la categoría
  if (name.includes('Bolsa') || (specs['Peso'] && specs['Peso'].includes('kg') && (name.includes('Cemento') || name.includes('Yeso') || name.includes('Pegamento') || name.includes('Arena') || name.includes('Piedra')))) {
    return 'Bolsa';
  }
  if (name.includes('(Millar)') || name.includes('Millar')) {
    return 'Millar';
  }
  if (name.includes('Varilla') || name.includes('Fierro Corrugado') || name.includes('Acero Corrugado')) {
    return 'Varilla';
  }
  if (name.includes('m³') || name.includes('Metro Cúbico') || (specs['Unidad'] && specs['Unidad'].includes('m³'))) {
    return 'm³';
  }
  if (name.includes('Rollo') || name.includes('100m')) {
    return 'Rollo';
  }
  if (name.includes('(1kg)') || name.includes('1kg')) {
    return 'kg';
  }
  if (name.includes('Tubo PVC') || name.includes('Tubo de PVC')) {
    return 'Tubo';
  }
  if (name.includes('Galón')) {
    return 'Galón';
  }
  if (name.includes('Litro') || name.includes('(1L)')) {
    return 'Litro';
  }

  // Fallbacks según categoría
  if (category === 'Materiales') {
    if (name.includes('Cemento')) return 'Bolsa';
    if (name.includes('Ladrillo')) return 'Unidad';
    if (name.includes('Fierro') || name.includes('Acero')) return 'Varilla';
    if (name.includes('Arena') || name.includes('Piedra') || name.includes('Hormigón') || name.includes('Afirmado')) return 'm³';
  }
  if (category === 'Plomería' && name.toLowerCase().includes('tubo') && !name.toLowerCase().includes('abasto')) {
    return 'Tubo';
  }
  
  return 'Unidad';
}

function generateProformaPDF() {
  if (state.cart.length === 0) {
    showToast('El carrito está vacío', 'warning');
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  const today = new Date();
  const validityDate = addBusinessDays(today, 3);

  const strToday = formatDate(today);
  const strValidity = formatDate(validityDate);

  const clientName = state.currentUser ? state.currentUser.full_name : "Cliente por Registrar";
  const projectName = state.currentUser ? `Proyecto - ${state.currentUser.role}` : "Mi Proyecto Obra";
  const district = state.selectedDistrict;

  // Encabezado
  doc.setFillColor(15, 23, 42); // #0f172a
  doc.rect(0, 0, 210, 35, 'F');

  // Línea decorativa naranja
  doc.setFillColor(255, 122, 0); // #ff7a00
  doc.rect(0, 35, 210, 2, 'F');

  // Texto Encabezado
  doc.setTextColor(255, 255, 255);
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(22);
  doc.text("ObraExpres", 15, 22);

  doc.setFontSize(10);
  doc.setFont("Helvetica", "normal");
  doc.text("La red inteligente de suministros de construcción", 15, 28);

  doc.setFont("Helvetica", "bold");
  doc.setFontSize(14);
  doc.text("PROFORMA DE COMPRA", 195, 20, { align: "right" });

  const proformaNum = `OE-${today.getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
  doc.setFont("Helvetica", "normal");
  doc.setFontSize(10);
  doc.text(`Documento N°: ${proformaNum}`, 195, 27, { align: "right" });

  // Datos del Cliente e Información General
  doc.setTextColor(15, 23, 42);
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(11);
  doc.text("DATOS DEL CLIENTE y PROYECTO", 15, 48);

  doc.setFont("Helvetica", "normal");
  doc.setFontSize(9);
  doc.text(`Cliente: ${clientName}`, 15, 55);
  doc.text(`Proyecto: ${projectName}`, 15, 61);
  doc.text(`Distrito de Despacho: ${district}`, 15, 67);

  doc.setFont("Helvetica", "bold");
  doc.text("INFORMACIÓN DE VALIDEZ", 120, 48);
  doc.setFont("Helvetica", "normal");
  doc.text(`Fecha de Emisión: ${strToday}`, 120, 55);
  doc.text(`Fecha de Validez: ${strValidity}`, 120, 61);
  doc.text(`Estado: VÁLIDO (3 Días Hábiles)`, 120, 67);

  // Línea divisoria
  doc.setDrawColor(226, 232, 240); // #e2e8f0
  doc.setLineWidth(0.5);
  doc.line(15, 73, 195, 73);

  // Generar tabla de productos agrupados por tienda para cálculo idéntico de fletes
  const tableRows = [];
  let subtotalGeneral = 0;
  let envioGeneral = 0;
  let pesoGeneral = 0;

  const grouped = {};
  state.cart.forEach(item => {
    if (!grouped[item.storeId]) {
      grouped[item.storeId] = [];
    }
    grouped[item.storeId].push(item);
  });

  Object.entries(grouped).forEach(([storeId, items]) => {
    const store = STORES[storeId];
    if (!store) return;

    let pesoTienda = 0;
    items.forEach(item => {
      const itemWeight = (PRODUCT_WEIGHTS[item.productId] || 2.0) * item.quantity;
      pesoTienda += itemWeight;
    });

    const distancia = DISTANCES[storeId][state.selectedDistrict] || 10.0;
    let fleteTienda = 0;
    if (pesoTienda <= 500) {
      fleteTienda = distancia * 2.0;
      fleteTienda = Math.max(fleteTienda, 10.0);
    } else {
      fleteTienda = 50.0 + (distancia * 5.0);
    }

    envioGeneral += fleteTienda;
    pesoGeneral += pesoTienda;

    items.forEach(item => {
      const product = productCache.get(item.productId);
      if (!product) return;

      const unit = getProductUnit(product);
      const totalItemPrice = item.price * item.quantity;
      subtotalGeneral += totalItemPrice;

      tableRows.push([
        item.quantity.toString(),
        unit,
        `${product.name} (Marca: ${product.brand}) - Prov: ${store.name}`,
        `S/. ${item.price.toFixed(2)}`,
        `S/. ${totalItemPrice.toFixed(2)}`
      ]);
    });
  });

  const subtotalNeto = subtotalGeneral / 1.18;
  const igv = subtotalGeneral - subtotalNeto;
  const totalConEnvio = subtotalGeneral + envioGeneral;

  doc.autoTable({
    startY: 78,
    head: [['Cant.', 'Unidad', 'Descripción / Material', 'P. Unitario', 'Subtotal']],
    body: tableRows,
    theme: 'grid',
    headStyles: {
      fillColor: [15, 23, 42], // #0f172a
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      halign: 'center'
    },
    columnStyles: {
      0: { halign: 'center', cellWidth: 15 },
      1: { halign: 'center', cellWidth: 20 },
      2: { halign: 'left' },
      3: { halign: 'right', cellWidth: 25 },
      4: { halign: 'right', cellWidth: 25 }
    },
    styles: {
      fontSize: 9,
      cellPadding: 3,
      lineColor: [226, 232, 240]
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252]
    }
  });

  let finalY = doc.lastAutoTable.finalY + 10;
  if (finalY + 50 > 280) {
    doc.addPage();
    finalY = 20;
  }

  // Totales
  doc.setTextColor(15, 23, 42);
  doc.setFont("Helvetica", "normal");
  doc.setFontSize(10);
  doc.text("Subtotal (sin IGV):", 130, finalY);
  doc.text(`S/. ${subtotalNeto.toFixed(2)}`, 195, finalY, { align: "right" });

  doc.text("IGV (18%):", 130, finalY + 6);
  doc.text(`S/. ${igv.toFixed(2)}`, 195, finalY + 6, { align: "right" });

  doc.text("Costos de Envío (Flete):", 130, finalY + 12);
  doc.text(`S/. ${envioGeneral.toFixed(2)}`, 195, finalY + 12, { align: "right" });

  doc.setFillColor(255, 122, 0); // #ff7a00
  doc.rect(130, finalY + 17, 65, 10, 'F');
  doc.setTextColor(255, 255, 255);
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(11);
  doc.text("TOTAL GENERAL:", 133, finalY + 23);
  doc.text(`S/. ${totalConEnvio.toFixed(2)}`, 192, finalY + 23, { align: "right" });

  // Términos y Condiciones
  doc.setTextColor(100, 116, 139); // #64748b
  doc.setFont("Helvetica", "bold");
  doc.setFontSize(8);
  doc.text("TÉRMINOS Y CONDICIONES:", 15, finalY);

  doc.setFont("Helvetica", "normal");
  const terms = [
    "- Los precios mostrados incluyen IGV y corresponden a las ofertas de ferreterías seleccionadas.",
    "- Las cotizaciones de materiales de construcción fluctúan constantemente según mercado.",
    "- Esta proforma cuenta con una validez estricta de 3 días hábiles desde su emisión.",
    `- Despacho programado para el distrito de ${district} sujeto a peso total (${pesoGeneral.toFixed(1)} kg).`,
    "- Para concretar su pedido, proceda con el pago dentro de la app o contacte soporte."
  ];
  let termY = finalY + 5;
  terms.forEach(term => {
    doc.text(term, 15, termY);
    termY += 4;
  });

  // Numeración de páginas y pie de página decorativo
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setDrawColor(226, 232, 240);
    doc.setLineWidth(0.5);
    doc.line(15, 282, 195, 282);

    doc.setTextColor(148, 163, 184); // #94a3b8
    doc.setFontSize(8);
    doc.setFont("Helvetica", "normal");
    doc.text("ObraExpres S.A. | RUC 20601234567 | www.obraexpres.com", 15, 288);
    doc.text(`Página ${i} de ${pageCount}`, 195, 288, { align: "right" });
  }

  doc.save(`Proforma_ObraExpres_${proformaNum}.pdf`);
  showToast("Proforma PDF descargada con éxito", "success");
}
