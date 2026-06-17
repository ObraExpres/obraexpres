from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from .database import engine, get_db, Base
from . import models, schemas

# Asegurar que las tablas existen (en caso de que no se corra el seed)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ObraExpres API", version="1.0.0")

# Habilitar CORS para permitir llamadas del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stores")
def get_stores(db: Session = Depends(get_db)):
    stores = db.query(models.Store).all()
    result = []
    for s in stores:
        result.append({
            "id": s.id,
            "name": s.name,
            "color": s.color,
            "logo": s.logo,
            "rating": s.rating,
            "reviews": s.reviews,
            "address": s.address,
            "coords": {"x": s.coords_x, "y": s.coords_y},
            "hours": s.hours,
            "deliveryFee": s.delivery_fee,
            "minDeliveryTime": s.min_delivery_time
        })
    return result

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Product.category).distinct().all()
    return [c[0] for c in categories if c[0]]

@app.get("/api/products")
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    store_ids: Optional[str] = None,  # Recibe IDs separados por comas
    sort_by: Optional[str] = "default",
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    
    # 1. Filtro por categoría
    if category and category != "all":
        query = query.filter(models.Product.category == category)
        
    # 2. Filtro por búsqueda
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Product.name.ilike(search_filter)) |
            (models.Product.brand.ilike(search_filter)) |
            (models.Product.description.ilike(search_filter))
        )
        
    products = query.all()
    
    # Parsear tiendas
    parsed_store_ids = []
    if store_ids:
        parsed_store_ids = [s.strip() for s in store_ids.split(",") if s.strip()]
        
    # 3. Mapear y filtrar por ofertas de tienda en Python
    filtered_products = []
    for prod in products:
        matching_offers = []
        for offer in prod.offers:
            # Filtrar por tiendas
            if parsed_store_ids and offer.store_id not in parsed_store_ids:
                continue
            # Filtrar por precios
            if min_price is not None and offer.price < min_price:
                continue
            if max_price is not None and offer.price > max_price:
                continue
            matching_offers.append({
                "storeId": offer.store_id,
                "price": offer.price,
                "stock": offer.stock,
                "deliveryTime": offer.delivery_time
            })
            
        # Si tiene ofertas válidas bajo el filtro actual, añadir producto
        if len(matching_offers) > 0:
            filtered_products.append({
                "id": prod.id,
                "name": prod.name,
                "brand": prod.brand,
                "category": prod.category,
                "description": prod.description,
                "icon": prod.icon,
                "specs": prod.specs,
                "stores": matching_offers
            })
            
    # 4. Ordenación
    if sort_by == "price-asc":
        filtered_products.sort(key=lambda p: min(o["price"] for o in p["stores"]) if p["stores"] else float('inf'))
    elif sort_by == "price-desc":
        filtered_products.sort(key=lambda p: min(o["price"] for o in p["stores"]) if p["stores"] else float('-inf'), reverse=True)
    elif sort_by == "name-asc":
        filtered_products.sort(key=lambda p: p["name"])
        
    return filtered_products

# Tabla de pesos reales de los productos en kg
PRODUCT_WEIGHTS = {
    1: 1.3,      # Taladro DeWalt
    2: 2.0,      # Amoladora Bosch
    3: 42.5,     # Cemento Pacasmayo Antisalitre
    4: 2.0,      # Varilla de Fierro 6mm (9m)
    5: 12.0,     # Cable THW Indeco
    6: 0.3,      # Interruptor Bticino
    7: 2.5,      # Mezcladora Vainsa
    8: 2.0,      # Tubo PVC SAP Pavco
    9: 5.0,      # Pintura CPP (Galón)
    10: 25.0,    # Yeso Pacasmayo (25kg)
    11: 2.0,     # Pala Redonda
    12: 15.0,    # Carretilla Buggy
    13: 0.8,     # Martillo Stanley
    14: 0.4,     # Wincha Métrica Stanley
    15: 1.2,     # Nivel de Burbuja Stanley
    16: 1.5,     # Llave Stilson Ridgid
    17: 0.9,     # Juego Destornilladores Stanley
    18: 8.0,     # Escalera Tijera Nexstep
    19: 1.0,     # Clavos Arequipa 3" (1kg)
    20: 1.0,     # Alambre Nro 16 (1kg)
    21: 2.8,     # Ladrillo KK 18 Huecos Lark (Unidad)
    22: 40.0,    # Arena Fina Bolsa (40kg)
    23: 40.0,    # Piedra Chancada Bolsa (40kg)
    24: 1.2,     # Aditivo Plastificante Chema
    25: 25.0,    # Pegamento Celima (25kg)
    26: 0.3,     # Tubo Abasto Vainsa
    27: 35.0,    # Inodoro Trebol
    28: 4.0,     # Cable de red Dixon
    29: 0.1,     # Cinta Aislante 3M
    30: 0.1,     # Caja Octogonal Pavco
    31: 0.3,     # Llave Termomagnética Bticino
    32: 0.4,     # Silicona Tekno
    33: 0.3,     # Rodillo Tekno
    34: 0.1,     # Brocha CPP 3"
    # --- Obra Gruesa ---
    35: 42.5,    # Cemento Pacasmayo Extra Forte
    36: 42.5,    # Cemento Pacasmayo Tipo I
    37: 42.5,    # Cemento Sol
    38: 42.5,    # Cemento Inka
    39: 2800.0,  # Ladrillo KK 18 Huecos (Millar)
    40: 2.1,     # Ladrillo Pandereta (Unidad)
    41: 2100.0,  # Ladrillo Pandereta (Millar)
    42: 8.0,     # Ladrillo Techo Hueco 15
    43: 7.0,     # Ladrillo Techo Hueco 12
    44: 4.5,     # Ladrillo Techo Hueco 8
    45: 2.0,     # Aceros Arequipa 6mm (9m)
    46: 3.6,     # Aceros Arequipa 8mm (9m)
    47: 5.0,     # Aceros Arequipa 3/8" (9m)
    48: 9.0,     # Aceros Arequipa 1/2" (9m)
    49: 14.0,    # Aceros Arequipa 5/8" (9m)
    50: 20.0,    # Aceros Arequipa 3/4" (9m)
    51: 2.0,     # Siderperu 6mm (9m)
    52: 3.6,     # Siderperu 8mm (9m)
    53: 5.0,     # Siderperu 3/8" (9m)
    54: 9.0,     # Siderperu 1/2" (9m)
    55: 14.0,    # Siderperu 5/8" (9m)
    56: 20.0,    # Siderperu 3/4" (9m)
    57: 1600.0,  # Arena Gruesa (m³)
    58: 1500.0,  # Arena Fina (m³)
    59: 1550.0,  # Piedra Chancada 1/2" (m³)
    60: 1550.0,  # Piedra Chancada 3/4" (m³)
    61: 1700.0,  # Hormigón (m³)
    62: 1800.0   # Afirmado (m³)
}

# Matriz de distancias en km a distritos de la Zona Norte
DISTANCES = {
    "construmax": {
        "Chiclayo": 5.0,
        "Pimentel": 15.0,
        "Lambayeque": 12.0,
        "Trujillo": 200.0,
        "Víctor Larco": 205.0,
        "El Porvenir": 202.0
    },
    "ferretodo": {
        "Chiclayo": 12.0,
        "Pimentel": 22.0,
        "Lambayeque": 3.0,
        "Trujillo": 212.0,
        "Víctor Larco": 217.0,
        "El Porvenir": 214.0
    },
    "depositoinca": {
        "Chiclayo": 200.0,
        "Pimentel": 210.0,
        "Lambayeque": 208.0,
        "Trujillo": 6.0,
        "Víctor Larco": 4.0,
        "El Porvenir": 10.0
    }
}

@app.post("/api/orders")
def create_order(checkout: schemas.CheckoutIn, db: Session = Depends(get_db)):
    if not checkout.items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")
        
    valid_districts = {"Chiclayo", "Pimentel", "Lambayeque", "Trujillo", "Víctor Larco", "El Porvenir"}
    if checkout.district not in valid_districts:
        raise HTTPException(status_code=400, detail="Distrito de despacho no válido")
        
    subtotal = 0.0
    order_items_to_create = []
    items_by_store = {}
    
    # Procesar cada item del carrito
    for item in checkout.items:
        product = db.query(models.Product).filter(models.Product.id == item.productId).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto con id {item.productId} no encontrado")
            
        assoc = db.query(models.StoreProductAssociation).filter(
            models.StoreProductAssociation.product_id == item.productId,
            models.StoreProductAssociation.store_id == item.storeId
        ).first()
        
        if not assoc:
            raise HTTPException(status_code=400, detail=f"El producto {product.name} no está disponible en la tienda {item.storeId}")
            
        if assoc.stock < item.quantity:
            store_name = db.query(models.Store.name).filter(models.Store.id == item.storeId).scalar() or item.storeId
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{product.name}' en {store_name}. Disponible: {assoc.stock}, Solicitado: {item.quantity}"
            )
            
        # Calcular precio
        item_total_price = assoc.price * item.quantity
        subtotal += item_total_price
        
        # Descontar stock de la base de datos
        assoc.stock -= item.quantity
        
        # Agrupar por tienda para cálculo de logística
        if item.storeId not in items_by_store:
            items_by_store[item.storeId] = []
        items_by_store[item.storeId].append((product.id, item.quantity))
        
        # Obtener nombre de la tienda para el pedido
        store_name = db.query(models.Store.name).filter(models.Store.id == item.storeId).scalar() or item.storeId
        
        order_items_to_create.append(models.OrderItem(
            product_id=product.id,
            product_name=product.name,
            store_id=assoc.store_id,
            store_name=store_name,
            quantity=item.quantity,
            price=assoc.price
        ))
        
    # Calcular cargos de envío dinámicos por tienda
    shipping_fee = 0.0
    for store_id, items in items_by_store.items():
        # Calcular peso total
        peso_tienda = sum(PRODUCT_WEIGHTS.get(pid, 2.0) * qty for pid, qty in items)
        
        # Obtener distancia
        distancia = DISTANCES.get(store_id, {}).get(checkout.district, 10.0)
        
        # Calcular flete según reglas de peso
        if peso_tienda <= 20.0:
            flete_tienda = 15.0
        else:
            flete_tienda = 80.0 + (peso_tienda - 20.0) * 0.50
            
        shipping_fee += round(flete_tienda, 2)
            
    total = subtotal + shipping_fee

    
    # Crear objeto de orden
    order = models.Order(
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        total=total,
        items=order_items_to_create
    )
    
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la orden: {str(e)}")
        
    # Formatear la salida de los items
    items_out = []
    for o_item in order.items:
        items_out.append({
            "productId": o_item.product_id,
            "productName": o_item.product_name,
            "storeId": o_item.store_id,
            "storeName": o_item.store_name,
            "quantity": o_item.quantity,
            "price": o_item.price
        })
        
    return {
        "id": order.id,
        "createdAt": order.created_at,
        "subtotal": order.subtotal,
        "shippingFee": order.shipping_fee,
        "total": order.total,
        "items": items_out
    }


@app.post("/api/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        password=user.password  # En producción usaríamos un hash real (e.g. bcrypt)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")
        
    return db_user


# Montar la carpeta frontend de forma estática en la raíz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


