// Interfaz del camarero: mesa -> pedidos -> añadir o modificar.
// Solo usa los endpoints de la API; no guarda datos propios.

const state = {
  view: "tables",
  table: null,          // mesa seleccionada
  order: null,          // pedido que se está modificando
  products: new Map(),  // id -> detalle de producto (con categoría y presentaciones)
  newOrder: { productId: null, presentationId: null },
  editPresentationId: null,
};

const $ = (id) => document.getElementById(id);

// ---------- API ----------

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(errorText(body) || `Error ${response.status}`);
  }
  return body;
}

// FastAPI devuelve "detail" como texto (errores propios) o como lista (validación del JSON).
function errorText(body) {
  if (!body || body.detail === undefined) return "";
  if (typeof body.detail === "string") return body.detail;
  return body.detail.map((error) => error.msg).join(". ");
}

async function getProduct(productId) {
  if (!state.products.has(productId)) {
    state.products.set(productId, await api(`/products/${productId}`));
  }
  return state.products.get(productId);
}

// ---------- Utilidades de interfaz ----------

function el(tag, attributes = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attributes)) {
    if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (key === "class") node.className = value;
    else node.setAttribute(key, value);
  }
  node.append(...children);
  return node;
}

function showMessage(text, ok = false) {
  const box = $("message");
  box.textContent = text;
  box.classList.toggle("ok", ok);
  box.hidden = !text;
}

function show(view, title) {
  state.view = view;
  for (const name of ["tables", "orders", "new", "edit"]) {
    $(`view-${name}`).hidden = name !== view;
  }
  $("title").textContent = title;
  $("back").hidden = view === "tables";
  window.scrollTo(0, 0);
}

function chips(container, items, selectedId, onSelect) {
  container.replaceChildren(
    ...items.map((item) =>
      el("button", {
        type: "button",
        class: "chip" + (item.id === selectedId ? " selected" : ""),
        onclick: () => onSelect(item),
      }, item.name)
    )
  );
}

// Ejecuta una acción mostrando su error en pantalla en vez de romper la página.
async function run(action) {
  try {
    await action();
  } catch (error) {
    showMessage(error.message);
  }
}

// ---------- 1. Mesas ----------

async function openTables() {
  showMessage("");
  state.table = null;
  show("tables", "Mesas");
  const tables = await api("/tables");
  $("tables").replaceChildren(
    ...tables.map((table) =>
      el("button", { type: "button", class: "card", onclick: () => run(() => openOrders(table)) }, table.name)
    )
  );
}

// ---------- 2. Pedidos de la mesa ----------

async function openOrders(table) {
  state.table = table;
  show("orders", table.name);
  const orders = await api(`/tables/${table.id}/orders`);
  const products = await Promise.all(orders.map((order) => getProduct(order.product_id)));

  $("no-orders").hidden = orders.length > 0;
  $("orders").replaceChildren(
    ...orders.map((order, index) => {
      const product = products[index];
      const presentation = product.presentations.find((p) => p.id === order.presentation_id);
      return el("li", {},
        el("span", { class: "qty" }, `${order.quantity}×`),
        el("span", { class: "order-text" },
          product.name,
          el("small", {}, presentation ? presentation.name : `Presentación ${order.presentation_id}`)
        ),
        el("button", { type: "button", onclick: () => run(() => openEdit(order)) }, "Modificar")
      );
    })
  );
}

// ---------- 3. Añadir pedido ----------

async function openNew() {
  showMessage("");
  state.newOrder = { productId: null, presentationId: null };
  show("new", `Nuevo pedido · ${state.table.name}`);
  $("products").replaceChildren();
  $("new-form").hidden = true;
  const categories = await api("/categories");
  const select = (category) => run(() => selectCategory(categories, category));
  chips($("categories"), categories, null, select);
}

async function selectCategory(categories, category) {
  chips($("categories"), categories, category.id, (c) => run(() => selectCategory(categories, c)));
  state.newOrder = { productId: null, presentationId: null };
  $("new-form").hidden = true;
  const products = await api(`/categories/${category.id}/products`);
  renderProducts(products);
}

function renderProducts(products) {
  $("products").replaceChildren(
    ...products.map((product) =>
      el("button", {
        type: "button",
        class: "card" + (product.id === state.newOrder.productId ? " selected" : ""),
        onclick: () => run(() => selectProduct(products, product)),
      }, product.name)
    )
  );
}

async function selectProduct(products, product) {
  state.newOrder = { productId: product.id, presentationId: null };
  renderProducts(products);
  const detail = await getProduct(product.id);
  const presentations = detail.presentations;
  // Si solo hay una presentación (por ejemplo, bebidas por unidad), se elige sola.
  if (presentations.length === 1) state.newOrder.presentationId = presentations[0].id;
  const render = () =>
    chips($("new-presentations"), presentations, state.newOrder.presentationId, (p) => {
      showMessage("");
      state.newOrder.presentationId = p.id;
      render();
    });
  render();
  $("new-quantity").value = 1;
  $("new-form").hidden = false;
}

async function submitNew(event) {
  event.preventDefault();
  const { productId, presentationId } = state.newOrder;
  if (!presentationId) {
    showMessage("Elige una presentación.");
    return;
  }
  await api(`/tables/${state.table.id}/orders`, {
    method: "POST",
    body: JSON.stringify({
      product_id: productId,
      presentation_id: presentationId,
      quantity: Number($("new-quantity").value),
    }),
  });
  await openOrders(state.table);
  showMessage("Pedido añadido.", true);
}

// ---------- 4. Modificar pedido ----------

async function openEdit(order) {
  showMessage("");
  state.order = order;
  state.editPresentationId = order.presentation_id;
  const product = await getProduct(order.product_id);
  show("edit", `Modificar pedido · ${state.table.name}`);
  $("edit-product").textContent = product.name;
  $("edit-quantity").value = order.quantity;
  const render = () =>
    chips($("edit-presentations"), product.presentations, state.editPresentationId, (p) => {
      state.editPresentationId = p.id;
      render();
    });
  render();
}

async function submitEdit(event) {
  event.preventDefault();
  const changes = {};
  const quantity = Number($("edit-quantity").value);
  if (quantity !== state.order.quantity) changes.quantity = quantity;
  if (state.editPresentationId !== state.order.presentation_id) {
    changes.presentation_id = state.editPresentationId;
  }
  if (Object.keys(changes).length === 0) {
    await openOrders(state.table);
    showMessage("No había cambios que guardar.", true);
    return;
  }
  await api(`/tables/${state.table.id}/orders/${state.order.id}`, {
    method: "PATCH",
    body: JSON.stringify(changes),
  });
  await openOrders(state.table);
  showMessage("Pedido modificado.", true);
}

// ---------- Arranque ----------

function setupSteppers() {
  for (const stepper of document.querySelectorAll(".stepper")) {
    const input = $(stepper.dataset.target);
    for (const button of stepper.querySelectorAll("button")) {
      button.addEventListener("click", () => {
        const next = (Number(input.value) || 1) + Number(button.dataset.step);
        input.value = Math.min(99, Math.max(1, next));
      });
    }
  }
}

function goBack() {
  showMessage("");
  if (state.view === "orders") run(openTables);
  else run(() => openOrders(state.table));
}

setupSteppers();
$("back").addEventListener("click", goBack);
$("add-order").addEventListener("click", () => run(openNew));
$("new-form").addEventListener("submit", (event) => run(() => submitNew(event)));
$("edit-form").addEventListener("submit", (event) => run(() => submitEdit(event)));
run(openTables);
