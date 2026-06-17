from .database import engine, Base, SessionLocal
from .models import Store, Product, StoreProductAssociation

def seed_database():
    # Recrear tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Crear Tiendas
        stores_data = [
            Store(
                id="construmax",
                name="ConstruMax",
                color="#ff7a00",
                logo="🏗️",
                rating=4.6,
                reviews=1420,
                address="Av. Industrial 450, Zona Industrial",
                coords_x=30.0,
                coords_y=40.0,
                hours="Lun - Sáb: 7:30 AM - 7:00 PM",
                delivery_fee=15.0,  # S/. 15.00
                min_delivery_time="Hoy mismo"
            ),
            Store(
                id="ferretodo",
                name="Ferretodo Lambayeque",
                color="#059669",
                logo="🏬",
                rating=4.7,
                reviews=328,
                address="Av. Salaverry 102, Chiclayo",
                coords_x=65.0,
                coords_y=35.0,
                hours="Lun - Dom: 8:00 AM - 8:00 PM",
                delivery_fee=10.0,  # S/. 10.00
                min_delivery_time="En 2 horas (Chiclayo)"
            ),
            Store(
                id="depositoinca",
                name="Depósito El Inca",
                color="#dc2626",
                logo="⛰️",
                rating=4.5,
                reviews=810,
                address="Av. Larco 890, Trujillo",
                coords_x=20.0,
                coords_y=70.0,
                hours="Lun - Sáb: 7:00 AM - 6:00 PM",
                delivery_fee=25.0,  # S/. 25.00
                min_delivery_time="Hoy mismo (Trujillo)"

            )
        ]
        
        for store in stores_data:
            db.add(store)
        
        db.commit()
        print("Tiendas añadidas exitosamente.")

        # 2. Crear Catálogo Base de 34 Productos
        products_base = [
            {
                "id": 1,
                "name": "Taladro Percutor Inalámbrico 20V MAX",
                "brand": "DeWalt",
                "category": "Herramientas",
                "description": "Taladro percutor de alta potencia, ideal para concreto, madera y metal. Cuenta con motor brushless, 2 velocidades mecánicas y luz LED integrada.",
                "icon": "🔌",
                "specs": {"Voltaje": "20V MAX", "Velocidad": "2000 RPM", "Mandril": "1/2\"", "Peso": "1.3 kg"},
                "base_price": 499.0
            },
            {
                "id": 2,
                "name": "Amoladora Angular de 4-1/2\" (850W)",
                "brand": "Bosch",
                "category": "Herramientas",
                "description": "Amoladora potente y segura con switch de protección contra polvo. Ideal para cortes y desbastes en metales y piedra.",
                "icon": "⚙️",
                "specs": {"Potencia": "850 W", "Disco": "4-1/2\"", "Velocidad": "11,000 RPM", "Garantía": "1 año"},
                "base_price": 250.0
            },
            {
                "id": 3,
                "name": "Cemento Gris Portland Clase Extra (50kg)",
                "brand": "Cemex",
                "category": "Materiales",
                "description": "Cemento Portland de alta resistencia, ideal para todo tipo de obras estructurales, losas, firmes y columnas.",
                "icon": "🧱",
                "specs": {"Peso": "50 kg", "Clase": "CPO 40 RS", "Uso": "Estructuras", "Norma": "NMX-C-414"},
                "base_price": 27.0
            },
            {
                "id": 4,
                "name": "Varilla Corrugada de Acero R-42 1/2\" (6m)",
                "brand": "Ternium",
                "category": "Materiales",
                "description": "Varilla de acero de refuerzo con corrugas para adherencia al concreto. Esencial para vigas y columnas.",
                "icon": "🦯",
                "specs": {"Diámetro": "1/2\"", "Longitud": "6 m", "Grado": "42", "Peso": "5.96 kg"},
                "base_price": 45.0
            },
            {
                "id": 5,
                "name": "Rollo de Cable Eléctrico THW Calibre 12 AWG (100m)",
                "brand": "Condumex",
                "category": "Electricidad",
                "description": "Conductor de cobre de alta pureza con aislamiento de PVC antiflama para instalaciones residenciales.",
                "icon": "⚡",
                "specs": {"Calibre": "12 AWG", "Largo": "100 m", "Voltaje": "600 V", "Temp": "90°C"},
                "base_price": 145.0
            },
            {
                "id": 6,
                "name": "Interruptor Inteligente Wi-Fi de 3 Botones",
                "brand": "Lutron",
                "category": "Electricidad",
                "description": "Apagador de pared moderno táctil compatible con Alexa y Google Assistant para domótica sencilla.",
                "icon": "📱",
                "specs": {"Conectividad": "Wi-Fi 2.4GHz", "Botones": "3", "Voltaje": "110V-240V", "Carga": "600W/bto"},
                "base_price": 68.0
            },
            {
                "id": 7,
                "name": "Mezcladora Monomando para Cocina",
                "brand": "Helvex",
                "category": "Plomería",
                "description": "Grifo monomando contemporáneo en acabado cromo brillante con cartucho cerámico duradero.",
                "icon": "🚰",
                "specs": {"Acabado": "Cromo", "Material": "Latón macizo", "Control": "Monomando", "Altura": "32 cm"},
                "base_price": 299.0
            },
            {
                "id": 8,
                "name": "Tubo de PVC Sanitario de 4\" (Tramo 6m)",
                "brand": "Amanco",
                "category": "Plomería",
                "description": "Tubo de PVC rígido para instalaciones sanitarias, drenajes de aguas residuales y pluviales.",
                "icon": "🧪",
                "specs": {"Diámetro": "4\"", "Longitud": "6 m", "Material": "PVC Rígido", "Junta": "Cementar"},
                "base_price": 42.0
            },
            {
                "id": 9,
                "name": "Pintura Vinil-Acrílica Blanca Lavable (19L)",
                "brand": "Comex",
                "category": "Pinturas",
                "description": "Pintura base agua de alta cobertura para interiores y exteriores. Acabado mate y lavable.",
                "icon": "🎨",
                "specs": {"Volumen": "19 Litros", "Color": "Blanco", "Acabado": "Mate", "Rendimiento": "8m²/L"},
                "base_price": 185.0
            },
            {
                "id": 10,
                "name": "Yeso Blanco de Construcción (25kg)",
                "brand": "Yesera Regiomontana",
                "category": "Materiales",
                "description": "Yeso de fraguado rápido y alta blancura para acabados lisos en muros interiores.",
                "icon": "🥛",
                "specs": {"Peso": "25 kg", "Fraguado": "10-15 min", "Uso": "Solo interiores"},
                "base_price": 15.0
            },
            {
                "id": 11,
                "name": "Pala Redonda con Mango de Madera",
                "brand": "Truper",
                "category": "Herramientas",
                "description": "Pala redonda de acero al carbono con mango de madera de encino. Ideal para excavación.",
                "icon": "🥄",
                "specs": {"Tipo": "Redonda", "Mango": "Madera 30\"", "Material": "Acero al carbono"},
                "base_price": 35.0
            },
            {
                "id": 12,
                "name": "Carretilla de Mano 5.5 ft³",
                "brand": "Pretul",
                "category": "Herramientas",
                "description": "Carretilla de obra reforzada con llanta neumática. Perfecta para transportar mezclas y tierra.",
                "icon": "🛒",
                "specs": {"Capacidad": "5.5 ft³", "Llanta": "Neumática", "Material": "Acero estructurado"},
                "base_price": 180.0
            },
            {
                "id": 13,
                "name": "Martillo de Uña Curva 16 oz",
                "brand": "Stanley",
                "category": "Herramientas",
                "description": "Martillo clásico con cabeza de acero pulido y mango de fibra de vidrio que absorbe vibraciones.",
                "icon": "🔨",
                "specs": {"Peso": "16 oz", "Uña": "Curva", "Mango": "Fibra de vidrio"},
                "base_price": 29.0
            },
            {
                "id": 14,
                "name": "Cinta Métrica de 8m/26ft",
                "brand": "Lufkin",
                "category": "Herramientas",
                "description": "Cinta métrica con carcasa resistente a impactos y freno rápido de seguridad.",
                "icon": "📏",
                "specs": {"Largo": "8 m / 26 ft", "Ancho": "1\"", "Precisión": "Clase II"},
                "base_price": 24.0
            },
            {
                "id": 15,
                "name": "Nivel de Burbuja de 24\"",
                "brand": "Milwaukee",
                "category": "Herramientas",
                "description": "Nivel profesional de aluminio con viales de alta visibilidad para nivelación horizontal y vertical.",
                "icon": "⚖️",
                "specs": {"Longitud": "24\"", "Material": "Aluminio", "Precisión": "0.029°"},
                "base_price": 75.0
            },
            {
                "id": 16,
                "name": "Llave Stilson de 14\"",
                "brand": "Ridgid",
                "category": "Herramientas",
                "description": "Llave para tubos robusta con mordazas autoajustables de acero aleado de alta resistencia.",
                "icon": "🔧",
                "specs": {"Tamaño": "14\"", "Material": "Hierro nodular", "Apertura": "2\""},
                "base_price": 95.0
            },
            {
                "id": 17,
                "name": "Juego de Destornilladores (10 piezas)",
                "brand": "Craftsman",
                "category": "Herramientas",
                "description": "Set de destornilladores planos y phillips con mangos ergonómicos antideslizantes.",
                "icon": "🪛",
                "specs": {"Piezas": "10", "Puntas": "Planos y Philips", "Material": "Cromo Vanadio"},
                "base_price": 59.0
            },
            {
                "id": 18,
                "name": "Escalera de Tijera de Aluminio 6\"",
                "brand": "Werner",
                "category": "Herramientas",
                "description": "Escalera de aluminio ligera con plataforma y peldaños antideslizantes.",
                "icon": "🪜",
                "specs": {"Altura": "6 ft / 1.8 m", "Material": "Aluminio", "Carga": "113 kg"},
                "base_price": 240.0
            },
            {
                "id": 19,
                "name": "Clavos para Madera con Cabeza 3\" (1kg)",
                "brand": "Fiero",
                "category": "Materiales",
                "description": "Clavos de acero pulido con cabeza plana para carpintería estructural.",
                "icon": "📌",
                "specs": {"Longitud": "3\"", "Peso": "1 kg", "Material": "Acero al carbono"},
                "base_price": 8.0
            },
            {
                "id": 20,
                "name": "Alambre Galvanizado Calibre 16 (1kg)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Alambre de acero galvanizado maleable para amarres de armaduras de concreto.",
                "icon": "➰",
                "specs": {"Calibre": "16 AWG", "Peso": "1 kg", "Acabado": "Galvanizado"},
                "base_price": 9.0
            },
            {
                "id": 21,
                "name": "Ladrillo Klinker Rojo (Unidad)",
                "brand": "Ladrillera Rex",
                "category": "Materiales",
                "description": "Ladrillo de arcilla cocida a alta temperatura para fachadas y muros portantes.",
                "icon": "🧱",
                "specs": {"Medidas": "24x12x6 cm", "Color": "Rojo", "Resistencia": "20 MPa"},
                "base_price": 1.80
            },
            {
                "id": 22,
                "name": "Arena Fina Lavada (Bolsa 40kg)",
                "brand": "Cantera Local",
                "category": "Materiales",
                "description": "Arena lavada clasificada para tarrajeos finos y acabados de albañilería.",
                "icon": "⏳",
                "specs": {"Peso": "40 kg", "Tipo": "Fina lavada", "Uso": "Tarrajeo"},
                "base_price": 6.0
            },
            {
                "id": 23,
                "name": "Piedra Chancada de 1/2\" (Bolsa 40kg)",
                "brand": "Cantera Local",
                "category": "Materiales",
                "description": "Piedra chancada de granito para la preparación de concreto de alta resistencia.",
                "icon": "🪨",
                "specs": {"Peso": "40 kg", "Tamaño": "1/2\"", "Material": "Granito chancado"},
                "base_price": 7.0
            },
            {
                "id": 24,
                "name": "Aditivo Plastificante para Concreto (1L)",
                "brand": "Sika",
                "category": "Materiales",
                "description": "Aditivo que mejora la trabajabilidad y aumenta la resistencia inicial del concreto.",
                "icon": "🧴",
                "specs": {"Volumen": "1 Litro", "Tipo": "Plastificante", "Rendimiento": "1L por 5 bultos"},
                "base_price": 18.0
            },
            {
                "id": 25,
                "name": "Pegamento para Cerámico UltraFuerte (25kg)",
                "brand": "Celima",
                "category": "Materiales",
                "description": "Pegamento gris de alta adherencia para cerámicos en interiores sobre muros y pisos.",
                "icon": "🥣",
                "specs": {"Peso": "25 kg", "Color": "Gris", "Tiempo abierto": "20 min"},
                "base_price": 22.0
            },
            {
                "id": 26,
                "name": "Tubo de Abasto de Acero Inoxidable 1/2\"",
                "brand": "Vainsa",
                "category": "Plomería",
                "description": "Tubo de abasto flexible trenzado en acero inoxidable para inodoros y lavatorios.",
                "icon": "🚿",
                "specs": {"Medida": "1/2\" x 1/2\"", "Longitud": "40 cm", "Material": "Acero Inoxidable"},
                "base_price": 12.0
            },
            {
                "id": 27,
                "name": "Inodoro One Piece Blanco",
                "brand": "Trebol",
                "category": "Plomería",
                "description": "Inodoro de una sola pieza con descarga ecológica de doble pulsador.",
                "icon": "🚽",
                "specs": {"Modelo": "One Piece", "Color": "Blanco", "Descarga": "4.8L / 3L"},
                "base_price": 380.0
            },
            {
                "id": 28,
                "name": "Cable de Red UTP Categoría 6 (100m)",
                "brand": "Dixon",
                "category": "Electricidad",
                "description": "Cable UTP Cat 6 sólido de cobre para redes de datos de alta velocidad.",
                "icon": "🌐",
                "specs": {"Categoría": "Cat 6", "Largo": "100 m", "Hilos": "4 pares sólidos"},
                "base_price": 110.0
            },
            {
                "id": 29,
                "name": "Cinta Aislante de PVC Negra",
                "brand": "3M",
                "category": "Electricidad",
                "description": "Cinta aislante profesional retardante de flama y resistente a altos voltajes.",
                "icon": "🎗️",
                "specs": {"Medida": "3/4\" x 20m", "Material": "PVC", "Aislamiento": "600 V"},
                "base_price": 4.50
            },
            {
                "id": 30,
                "name": "Caja Octogonal de PVC para Luz",
                "brand": "Bticino",
                "category": "Electricidad",
                "description": "Caja octogonal pesada de PVC para instalaciones eléctricas empotradas.",
                "icon": "📦",
                "specs": {"Forma": "Octogonal", "Material": "PVC Pesado", "Salidas": "1/2\" y 3/4\""},
                "base_price": 1.20
            },
            {
                "id": 31,
                "name": "Llave Termomagnética 2x20A",
                "brand": "Schneider Electric",
                "category": "Electricidad",
                "description": "Interruptor termomagnético riel DIN para la protección contra sobrecargas y cortocircuitos.",
                "icon": "🎛️",
                "specs": {"Polos": "2", "Corriente": "20 A", "Montaje": "Riel DIN"},
                "base_price": 28.0
            },
            {
                "id": 32,
                "name": "Silicona Multiuso Transparente",
                "brand": "Tack",
                "category": "Pinturas",
                "description": "Sellador de silicona acética transparente ideal para baños, cocinas y vidrio.",
                "icon": "🧴",
                "specs": {"Volumen": "280 ml", "Color": "Transparente", "Curado": "Acético"},
                "base_price": 14.0
            },
            {
                "id": 33,
                "name": "Rodillo para Pintar Felpa Media 9\"",
                "brand": "Éxito",
                "category": "Pinturas",
                "description": "Rodillo de felpa de poliéster de media densidad para paredes lisas y semi-rugosas.",
                "icon": "🖌️",
                "specs": {"Ancho": "9\"", "Felpa": "3/8\"", "Tubo": "PVC estándar"},
                "base_price": 12.0
            },
            {
                "id": 34,
                "name": "Brocha para Pintar de Cerdas Naturales 3\"",
                "brand": "Truper",
                "category": "Pinturas",
                "description": "Brocha con mango de plástico y cerdas naturales firmes para acabados finos y parejos.",
                "icon": "🧹",
                "specs": {"Ancho": "3\"", "Cerdas": "Naturales", "Mango": "Ergonómico"},
                "base_price": 9.0
            }
        ]

        for p_data in products_base:
            product = Product(
                id=p_data["id"],
                name=p_data["name"],
                brand=p_data["brand"],
                category=p_data["category"],
                description=p_data["description"],
                icon=p_data["icon"],
                specs=p_data["specs"]
            )
            db.add(product)
            db.commit()
            
            # Asociar a las 3 tiendas con variaciones de precios (S/. 0.50 y S/. 1.00)
            # ConstruMax (construmax) -> precio base
            # Ferretodo Lambayeque (ferretodo) -> precio base + S/. 0.50 (o S/. 1.00 si P > 100)
            # Depósito El Inca (depositoinca) -> precio base - S/. 0.50 (o S/. 1.00 si P > 100)
            base_p = p_data["base_price"]
            diff = 0.50 if base_p < 100 else 1.00
            
            offers = [
                {
                    "store_id": "construmax",
                    "price": base_p,
                    "stock": 100,
                    "delivery_time": "Hoy mismo"
                },
                {
                    "store_id": "ferretodo",
                    "price": round(base_p + diff, 2),
                    "stock": 120,
                    "delivery_time": "En 2 horas"
                },
                {
                    "store_id": "depositoinca",
                    "price": max(round(base_p - diff, 2), 0.50),  # Nunca menor a 0.50
                    "stock": 150,
                    "delivery_time": "1-2 días"
                }
            ]
            
            for offer in offers:
                assoc = StoreProductAssociation(
                    store_id=offer["store_id"],
                    product_id=product.id,
                    price=offer["price"],
                    stock=offer["stock"],
                    delivery_time=offer["delivery_time"]
                )
                db.add(assoc)
            
        db.commit()
        print("Productos y ofertas añadidos exitosamente.")
    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
