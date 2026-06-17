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

        # 2. Crear Catálogo Base de 62 Productos Localizados (34 originales + 28 nuevos)
        products_base = [
            # --- CATEGORÍA: HERRAMIENTAS (IDs 1-2, 11-18) ---
            {
                "id": 1,
                "name": "Taladro Percutor Inalámbrico DeWalt 20V Max",
                "brand": "DeWalt",
                "category": "Herramientas",
                "description": "Taladro percutor brushless de alta potencia, ideal para concreto, madera y metal. Incluye maletín y 2 baterías.",
                "icon": "🔌",
                "specs": {"Voltaje": "20V MAX", "Velocidad": "2000 RPM", "Mandril": "1/2\"", "Garantía": "3 años"},
                "base_price": 499.0
            },
            {
                "id": 2,
                "name": "Amoladora Angular Bosch 4-1/2\" 850W",
                "brand": "Bosch",
                "category": "Herramientas",
                "description": "Amoladora potente y segura con switch de protección contra polvo. Ergonómica y de larga vida útil.",
                "icon": "⚙️",
                "specs": {"Potencia": "850 W", "Disco": "4-1/2\"", "Velocidad": "11,000 RPM", "Garantía": "1 año"},
                "base_price": 239.0
            },
            # --- CEMENTOS ORIGINAL Y NUEVOS (ID 3 + 35-38) ---
            {
                "id": 3,
                "name": "Cemento Pacasmayo Antisalitre MS (Bolsa 42.5 kg)",
                "brand": "Pacasmayo",
                "category": "Materiales",
                "description": "Cemento adicionado tipo MS de resistencia moderada a los sulfatos. Ideal para cimientos y ambientes húmedos.",
                "icon": "🧱",
                "specs": {"Peso": "42.5 kg", "Tipo": "MS (Antisalitre)", "Origen": "Perú"},
                "base_price": 31.00
            },
            # --- ACERO CORRUGADO ORIGINAL (ID 4) ---
            {
                "id": 4,
                "name": "Varilla de Fierro Corrugado Aceros Arequipa 6mm (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro corrugado de alta adherencia de 6mm de diámetro. Cumple con normas ASTM A615 Grado 60.",
                "icon": "🦯",
                "specs": {"Diámetro": "6 mm", "Longitud": "9 m", "Peso/Varilla": "2.0 kg"},
                "base_price": 12.00
            },
            # --- ELECTRICIDAD ORIGINAL (IDs 5-6, 28-31) ---
            {
                "id": 5,
                "name": "Rollo de Cable THW Indeco 12 AWG (100m)",
                "brand": "Indeco",
                "category": "Electricidad",
                "description": "Conductor de cobre de alta pureza con aislamiento de PVC antiflama. Excelente conductividad y seguridad.",
                "icon": "⚡",
                "specs": {"Calibre": "12 AWG (4 mm²)", "Largo": "100 m", "Voltaje": "450/750 V", "Color": "Rojo/Negro"},
                "base_price": 185.0
            },
            {
                "id": 6,
                "name": "Interruptor Simple Bticino Modus Plus",
                "brand": "Bticino",
                "category": "Electricidad",
                "description": "Interruptor de pared de diseño moderno y alta durabilidad. Línea Modus Plus original.",
                "icon": "📱",
                "specs": {"Tipo": "Simple", "Voltaje": "220V", "Corriente": "10 A", "Color": "Blanco"},
                "base_price": 8.50
            },
            # --- PLOMERÍA ORIGINAL (IDs 7-8, 26-27) ---
            {
                "id": 7,
                "name": "Mezcladora Monomando para Lavadero Vainsa",
                "brand": "Vainsa",
                "category": "Plomería",
                "description": "Grifería monomando con acabado cromado y cartucho cerámico para mayor control del flujo de agua.",
                "icon": "🚰",
                "specs": {"Acabado": "Cromo", "Material": "Bronce", "Control": "Monomando", "Garantía": "De por vida"},
                "base_price": 189.0
            },
            {
                "id": 8,
                "name": "Tubo PVC SAP Presión Pavco Clase 10 1/2\" (3m)",
                "brand": "Pavco",
                "category": "Plomería",
                "description": "Tubo de PVC rígido para instalaciones de agua fría a alta presión. Resistente y duradero.",
                "icon": "🧪",
                "specs": {"Diámetro": "1/2\"", "Longitud": "3 m", "Clase": "Clase 10 (Presión)"},
                "base_price": 8.50
            },
            # --- PINTURAS ORIGINAL (IDs 9, 32-34) ---
            {
                "id": 9,
                "name": "Pintura Látex CPP Pato Lavable Blanco (Galón)",
                "brand": "CPP",
                "category": "Pinturas",
                "description": "Pintura látex blanca lavable de excelente acabado y gran rendimiento para interiores y exteriores.",
                "icon": "🎨",
                "specs": {"Medida": "1 Galón", "Color": "Blanco", "Acabado": "Mate"},
                "base_price": 45.0
            },
            # --- MATERIALES MENORES ORIGINALES (IDs 10, 19-25) ---
            {
                "id": 10,
                "name": "Yeso Extrablanco de Obra Pacasmayo (25kg)",
                "brand": "Pacasmayo",
                "category": "Materiales",
                "description": "Yeso de fraguado rápido y alta blancura para empastados finos y acabados de techos interiores.",
                "icon": "📦",
                "specs": {"Peso": "25 kg", "Color": "Blanco", "Uso": "Acabados de tarrajeo"},
                "base_price": 18.0
            },
            # --- HERRAMIENTAS ORIGINAL (IDs 11-18) ---
            {
                "id": 11,
                "name": "Pala Redonda Tramontina con Mango de Madera",
                "brand": "Tramontina",
                "category": "Herramientas",
                "description": "Pala de acero templado con mango de madera ergonómico. Herramienta clásica de excavación.",
                "icon": "🥄",
                "specs": {"Tipo": "Redonda", "Mango": "Madera con empuñadura Y", "Largo": "105 cm"},
                "base_price": 49.0
            },
            {
                "id": 12,
                "name": "Carretilla Buggy Tramontina de Acero 80L",
                "brand": "Tramontina",
                "category": "Herramientas",
                "description": "Carretilla de gran resistencia para transporte de tierra, concreto y agregados en obra.",
                "icon": "🛒",
                "specs": {"Capacidad": "80 L / 5.5 ft³", "Llanta": "Neumática", "Material": "Acero reforzado"},
                "base_price": 189.0
            },
            {
                "id": 13,
                "name": "Martillo de Uña Stanley Fibra de Vidrio 16 oz",
                "brand": "Stanley",
                "category": "Herramientas",
                "description": "Martillo ergonómico con cabeza de acero pulido y mango de fibra de vidrio que reduce vibraciones.",
                "icon": "🔨",
                "specs": {"Peso": "16 oz", "Mango": "Fibra de vidrio", "Uso": "Carpintería"},
                "base_price": 39.0
            },
            {
                "id": 14,
                "name": "Wincha Métrica Stanley Global 8m/26ft",
                "brand": "Stanley",
                "category": "Herramientas",
                "description": "Cinta métrica con bloqueo fuerte y gancho magnético. Lectura rápida en pulgadas y centímetros.",
                "icon": "📏",
                "specs": {"Largo": "8 m / 26 ft", "Ancho cinta": "1\"", "Material": "Carcasa ABS"},
                "base_price": 35.0
            },
            {
                "id": 15,
                "name": "Nivel de Burbuja de Aluminio Stanley 24\"",
                "brand": "Stanley",
                "category": "Herramientas",
                "description": "Nivel metálico de gran precisión con 3 viales para comprobar horizontales, verticales y 45°.",
                "icon": "📐",
                "specs": {"Largo": "24\" (60 cm)", "Material": "Aluminio", "Precisión": "0.5 mm/m"},
                "base_price": 59.0
            },
            {
                "id": 16,
                "name": "Llave Stilson de Acero Ridgid 14\"",
                "brand": "Ridgid",
                "category": "Herramientas",
                "description": "Llave para tubos de alta resistencia con mordazas de acero de aleación para una sujeción firme.",
                "icon": "🔧",
                "specs": {"Medida": "14\" (350 mm)", "Capacidad tubo": "2\"", "Material": "Hierro nodular"},
                "base_price": 149.0
            },
            {
                "id": 17,
                "name": "Juego de Destornilladores Stanley (10 piezas)",
                "brand": "Stanley",
                "category": "Herramientas",
                "description": "Set de destornilladores planos y phillips con mangos ergonómicos antideslizantes de alta torsión.",
                "icon": "🪛",
                "specs": {"Piezas": "10", "Varilla": "Acero Cromo Vanadio", "Puntas": "Magnéticas"},
                "base_price": 69.0
            },
            {
                "id": 18,
                "name": "Escalera de Tijera de Aluminio Nexstep 6 Peldaños",
                "brand": "Nexstep",
                "category": "Herramientas",
                "description": "Escalera de aluminio ligera y de alta seguridad para trabajos de altura mediana.",
                "icon": "🪜",
                "specs": {"Peldaños": "6", "Material": "Aluminio", "Capacidad": "150 kg"},
                "base_price": 199.0
            },
            # --- MATERIALES MENORES (IDs 19-20, 22-25) ---
            {
                "id": 19,
                "name": "Clavos para Madera con Cabeza Aceros Arequipa 3\" (1kg)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Clavos de acero pulido de 3 pulgadas con cabeza plana para carpintería estructural y encofrados.",
                "icon": "📌",
                "specs": {"Medida": "3\"", "Peso": "1 kg", "Material": "Acero trefilado"},
                "base_price": 9.50
            },
            {
                "id": 20,
                "name": "Alambre Negro Recocido Nro 16 Aceros Arequipa (1kg)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Alambre recocido dulce calibre 16, ideal para amarres de varillas de acero estructural.",
                "icon": "🪢",
                "specs": {"Nro/Calibre": "Nro 16", "Peso": "1 kg", "Uso": "Amarre de fierro"},
                "base_price": 9.00
            },
            # --- LADRILLO ORIGINAL REEMPLAZADO CON PRODUCTO PERUANO (ID 21) ---
            {
                "id": 21,
                "name": "Ladrillo King Kong 18 Huecos Lark (Unidad)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Ladrillo de arcilla estructurado de 18 huecos ideal para la construcción de muros portantes de albañilería confinada.",
                "icon": "🧱",
                "specs": {"Medidas": "9x12.5x23 cm", "Tipo": "King Kong (18 huecos)", "Peso/unidad": "2.8 kg"},
                "base_price": 1.20
            },
            # --- AGREGADOS EN BOLSA (IDs 22-23) ---
            {
                "id": 22,
                "name": "Arena Fina Lavada en Bolsa (40kg)",
                "brand": "Genérico",
                "category": "Materiales",
                "description": "Arena fina cribada y seca en bolsa de fácil manipulación. Ideal para tarrajeo fino de interiores.",
                "icon": "⏳",
                "specs": {"Peso": "40 kg", "Granulometría": "Fina lavada"},
                "base_price": 8.00
            },
            {
                "id": 23,
                "name": "Piedra Chancada de 1/2\" en Bolsa (40kg)",
                "brand": "Genérico",
                "category": "Materiales",
                "description": "Piedra triturada de cantera de 1/2 pulgada. Ideal para mezclas de concreto de alta resistencia en espacios reducidos.",
                "icon": "🪨",
                "specs": {"Peso": "40 kg", "Tamaño": "1/2\""},
                "base_price": 8.50
            },
            # --- QUÍMICOS Y PEGAMENTOS (IDs 24-25) ---
            {
                "id": 24,
                "name": "Aditivo Plastificante Chema Plast para Concreto (1L)",
                "brand": "Chema",
                "category": "Materiales",
                "description": "Aditivo líquido plastificante que reduce la cantidad de agua y mejora la resistencia mecánica del concreto.",
                "icon": "🧴",
                "specs": {"Volumen": "1 Litro", "Rendimiento": "1 bolsa de cemento por dosis"},
                "base_price": 24.00
            },
            {
                "id": 25,
                "name": "Pegamento Gris Celima Interiores (25kg)",
                "brand": "Celima",
                "category": "Materiales",
                "description": "Adhesivo cementicio en polvo formulado especialmente para la instalación de cerámicas y mayólicas en interiores.",
                "icon": "🩹",
                "specs": {"Peso": "25 kg", "Color": "Gris", "Uso": "Cerámicos interiores"},
                "base_price": 22.00
            },
            # --- PLOMERÍA ORIGINAL (IDs 26-27) ---
            {
                "id": 26,
                "name": "Tubo de Abasto Flexible de Acero Inoxidable Vainsa 1/2\"",
                "brand": "Vainsa",
                "category": "Plomería",
                "description": "Tubo de abasto flexible trenzado de acero inoxidable para conexión confiable de inodoros y grifos.",
                "icon": "⛓️",
                "specs": {"Medida": "1/2\" x 1/2\"", "Longitud": "40 cm", "Presión máx": "120 PSI"},
                "base_price": 25.0
            },
            {
                "id": 27,
                "name": "Inodoro Rapid Jet One Piece Trebol Blanco",
                "brand": "Trebol",
                "category": "Plomería",
                "description": "Sanitario de porcelana vitrificada con sistema de descarga eficiente de un solo cuerpo. Ahorro de agua.",
                "icon": "🚽",
                "specs": {"Diseño": "One Piece (Un cuerpo)", "Color": "Blanco", "Consumo": "4.8 LPF"},
                "base_price": 489.0
            },
            # --- ELECTRICIDAD ORIGINAL (IDs 28-31) ---
            {
                "id": 28,
                "name": "Cable de Red UTP Categoría 6 Dixon (100m)",
                "brand": "Dixon",
                "category": "Electricidad",
                "description": "Cable UTP Cat 6 con hilos 100% de cobre sólido. Ideal para redes Gigabit y transmisión limpia.",
                "icon": "🛜",
                "specs": {"Categoría": "Cat 6", "Longitud": "100 m", "Conductor": "Cobre sólido"},
                "base_price": 120.0
            },
            {
                "id": 29,
                "name": "Cinta Aislante de PVC 3M Temflex 1700",
                "brand": "3M",
                "category": "Electricidad",
                "description": "Cinta aislante de alta calidad para empalmes eléctricos y aislamiento primario de cables.",
                "icon": "🎗️",
                "specs": {"Medida": "3/4\" x 20m", "Espesor": "0.18 mm", "Color": "Negra"},
                "base_price": 4.50
            },
            {
                "id": 30,
                "name": "Caja Octogonal de PVC Pesado Pavco",
                "brand": "Pavco",
                "category": "Electricidad",
                "description": "Caja de paso octogonal resistente para empotrar luminarias y derivaciones en losas de techo aligerado.",
                "icon": "📦",
                "specs": {"Forma": "Octogonal", "Material": "PVC Pesado", "Salidas": "1/2\" y 3/4\""},
                "base_price": 1.20
            },
            {
                "id": 31,
                "name": "Llave Termomagnética Din Bticino 2x20A",
                "brand": "Bticino",
                "category": "Electricidad",
                "description": "Dispositivo automático de protección contra sobrecargas y cortocircuitos. Montaje en riel DIN.",
                "icon": "🔌",
                "specs": {"Polos": "2 (Bipolar)", "Corriente": "20 A", "Montaje": "Riel DIN (2 módulos)"},
                "base_price": 32.00
            },
            # --- PINTURAS ORIGINAL (IDs 32-34) ---
            {
                "id": 32,
                "name": "Sellador Silicona Multiuso Tekno Transparente",
                "brand": "Tekno",
                "category": "Pinturas",
                "description": "Sellador acrílico transparente multiuso para sellar juntas en baños, cocinas, puertas y ventanas.",
                "icon": "🧴",
                "specs": {"Volumen": "300 ml", "Color": "Transparente", "Uso": "Multiuso"},
                "base_price": 12.50
            },
            {
                "id": 33,
                "name": "Rodillo para Pintar Felpa Media Tekno 9\"",
                "brand": "Tekno",
                "category": "Pinturas",
                "description": "Rodillo de felpa de poliéster de media densidad para paredes lisas y semi-rugosas. Pintado rápido.",
                "icon": "🖌️",
                "specs": {"Medida": "9\" (23 cm)", "Tipo": "Felpa media", "Mango": "Ergonómico de plástico"},
                "base_price": 15.00
            },
            {
                "id": 34,
                "name": "Brocha para Pintar de Cerdas Naturales CPP 3\"",
                "brand": "CPP",
                "category": "Pinturas",
                "description": "Brocha clásica con cerdas naturales firmes para un acabado uniforme y pintura sin grumos.",
                "icon": "🧹",
                "specs": {"Ancho": "3\"", "Cerdas": "Naturales", "Mango": "Madera barnizada"},
                "base_price": 8.50
            },

            # ==========================================
            #   NUEVOS PRODUCTOS DE OBRA GRUESA (IDs 35-62)
            # ==========================================

            # --- CATEGORÍA: CEMENTOS (IDs 35-38) ---
            {
                "id": 35,
                "name": "Cemento Pacasmayo Extra Forte (Bolsa 42.5 kg)",
                "brand": "Pacasmayo",
                "category": "Materiales",
                "description": "Cemento adicionado Portland Tipo ICO con filler calizo. Excelente trabajabilidad y menor fisuración.",
                "icon": "🧱",
                "specs": {"Peso": "42.5 kg", "Tipo": "ICO (Adicionado)", "Uso": "Tarrajeos y encofrados"},
                "base_price": 27.50
            },
            {
                "id": 36,
                "name": "Cemento Pacasmayo Tipo I (Bolsa 42.5 kg)",
                "brand": "Pacasmayo",
                "category": "Materiales",
                "description": "Cemento Portland Tipo I tradicional de alta resistencia inicial. Ideal para vaciados de concreto estructural.",
                "icon": "🧱",
                "specs": {"Peso": "42.5 kg", "Tipo": "Tipo I (Puro)", "Uso": "Estructuras, losas y columnas"},
                "base_price": 28.50
            },
            {
                "id": 37,
                "name": "Cemento Sol (Bolsa 42.5 kg)",
                "brand": "Sol",
                "category": "Materiales",
                "description": "Cemento Portland Tipo I líder en Lima y el norte peruano. Garantiza fraguado seguro en zapatas y columnas.",
                "icon": "🧱",
                "specs": {"Peso": "42.5 kg", "Tipo": "Tipo I", "Origen": "Unacem"},
                "base_price": 29.00
            },
            {
                "id": 38,
                "name": "Cemento Inka Ultra Resistente (Bolsa 42.5 kg)",
                "brand": "Inka",
                "category": "Materiales",
                "description": "Cemento Portland adicionado de alta resistencia al agua y salitre. Costo-beneficio óptimo.",
                "icon": "🧱",
                "specs": {"Peso": "42.5 kg", "Tipo": "Adicionado", "Rendimiento": "Alto"},
                "base_price": 26.50
            },

            # --- CATEGORÍA: LADRILLOS (IDs 39-44) ---
            {
                "id": 39,
                "name": "Ladrillo King Kong 18 Huecos Lark (Millar)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Lote de 1000 ladrillos King Kong para muros estructurales. Arcilla de alta cocción.",
                "icon": "🏗️",
                "specs": {"Cantidad": "1000 unidades (Millar)", "Medidas": "9x12.5x23 cm", "Peso/Lote": "2800 kg"},
                "base_price": 1100.00
            },
            {
                "id": 40,
                "name": "Ladrillo Pandereta Lark (Unidad)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Ladrillo de arcilla ligero especial para tabiquería y divisiones que no soportan carga estructural.",
                "icon": "🧱",
                "specs": {"Medidas": "9x11x23 cm", "Tipo": "Pandereta lisa", "Peso/unidad": "2.1 kg"},
                "base_price": 0.95
            },
            {
                "id": 41,
                "name": "Ladrillo Pandereta Lark (Millar)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Lote de 1000 ladrillos Pandereta para divisiones de muros interiores. Peso ligero.",
                "icon": "🏗️",
                "specs": {"Cantidad": "1000 unidades (Millar)", "Medidas": "9x11x23 cm", "Peso/Lote": "2100 kg"},
                "base_price": 880.00
            },
            {
                "id": 42,
                "name": "Ladrillo de Techo Hueco 15 Lark (Unidad)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Ladrillo hueco de arcilla cocida de 15 cm de altura, ideal para el aligerado de losas de techos residenciales.",
                "icon": "🧱",
                "specs": {"Medidas": "15x30x30 cm", "Tipo": "Hueco 15", "Peso/unidad": "8.0 kg"},
                "base_price": 3.30
            },
            {
                "id": 43,
                "name": "Ladrillo de Techo Hueco 12 Lark (Unidad)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Ladrillo hueco de arcilla de 12 cm de altura para techos ligeros de tramos cortos.",
                "icon": "🧱",
                "specs": {"Medidas": "12x30x30 cm", "Tipo": "Hueco 12", "Peso/unidad": "7.0 kg"},
                "base_price": 3.00
            },
            {
                "id": 44,
                "name": "Ladrillo de Techo Hueco 8 Lark (Unidad)",
                "brand": "Lark",
                "category": "Materiales",
                "description": "Ladrillo hueco ultra-ligero de 8 cm de altura para losas de aligerados especiales.",
                "icon": "🧱",
                "specs": {"Medidas": "8x30x30 cm", "Tipo": "Hueco 8", "Peso/unidad": "4.5 kg"},
                "base_price": 2.50
            },

            # --- CATEGORÍA: ACERO CORRUGADO (IDs 45-56) ---
            # Aceros Arequipa
            {
                "id": 45,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 6mm (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro de 6mm de diámetro, muy usado como acero de temperatura en techos aligerados y estribos cortos.",
                "icon": "🦯",
                "specs": {"Diámetro": "6 mm", "Longitud": "9 m", "Peso/Varilla": "2.0 kg"},
                "base_price": 12.00
            },
            {
                "id": 46,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 8mm (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro de 8mm de diámetro. Ideal para estribos de vigas y columnas residenciales.",
                "icon": "🦯",
                "specs": {"Diámetro": "8 mm", "Longitud": "9 m", "Peso/Varilla": "3.6 kg"},
                "base_price": 19.00
            },
            {
                "id": 47,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 3/8\" (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro de 3/8\" de diámetro. Componente esencial para el refuerzo secundario y viguetas.",
                "icon": "🦯",
                "specs": {"Diámetro": "3/8\" (9.5 mm)", "Longitud": "9 m", "Peso/Varilla": "5.0 kg"},
                "base_price": 25.00
            },
            {
                "id": 48,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 1/2\" (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro corrugado estructural de 1/2 pulgada de diámetro. Elemento básico para vigas, columnas y zapatas.",
                "icon": "🦯",
                "specs": {"Diámetro": "1/2\" (12.7 mm)", "Longitud": "9 m", "Peso/Varilla": "9.0 kg"},
                "base_price": 41.00
            },
            {
                "id": 49,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 5/8\" (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro de 5/8\" de diámetro de alta resistencia. Empleado en estructuras de luces amplias y cimientos.",
                "icon": "🦯",
                "specs": {"Diámetro": "5/8\" (15.9 mm)", "Longitud": "9 m", "Peso/Varilla": "14.0 kg"},
                "base_price": 65.00
            },
            {
                "id": 50,
                "name": "Varilla de Acero Corrugado Aceros Arequipa 3/4\" (9m)",
                "brand": "Aceros Arequipa",
                "category": "Materiales",
                "description": "Fierro pesado de 3/4\" de diámetro. Ideal para construcciones comerciales y columnas robustas.",
                "icon": "🦯",
                "specs": {"Diámetro": "3/4\" (19.1 mm)", "Longitud": "9 m", "Peso/Varilla": "20.0 kg"},
                "base_price": 94.00
            },
            # Siderperu
            {
                "id": 51,
                "name": "Varilla de Acero Corrugado Siderperu 6mm (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro corrugado Siderperu de 6mm. Flexibilidad y ductilidad garantizada según normas.",
                "icon": "🦯",
                "specs": {"Diámetro": "6 mm", "Longitud": "9 m", "Peso/Varilla": "2.0 kg"},
                "base_price": 11.50
            },
            {
                "id": 52,
                "name": "Varilla de Acero Corrugado Siderperu 8mm (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro corrugado Siderperu de 8mm. Ideal para refuerzos transversales (estribos).",
                "icon": "🦯",
                "specs": {"Diámetro": "8 mm", "Longitud": "9 m", "Peso/Varilla": "3.6 kg"},
                "base_price": 18.50
            },
            {
                "id": 53,
                "name": "Varilla de Acero Corrugado Siderperu 3/8\" (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro corrugado Siderperu de 3/8 pulgada. Óptima ductilidad para vigas y losas.",
                "icon": "🦯",
                "specs": {"Diámetro": "3/8\" (9.5 mm)", "Longitud": "9 m", "Peso/Varilla": "5.0 kg"},
                "base_price": 24.50
            },
            {
                "id": 54,
                "name": "Varilla de Acero Corrugado Siderperu 1/2\" (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro corrugado Siderperu de 1/2 pulgada de diámetro. Gran adherencia al concreto.",
                "icon": "🦯",
                "specs": {"Diámetro": "1/2\" (12.7 mm)", "Longitud": "9 m", "Peso/Varilla": "9.0 kg"},
                "base_price": 39.50
            },
            {
                "id": 55,
                "name": "Varilla de Acero Corrugado Siderperu 5/8\" (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro de alta tracción Siderperu de 5/8\". Fabricación de alta tecnología en Chimbote.",
                "icon": "🦯",
                "specs": {"Diámetro": "5/8\" (15.9 mm)", "Longitud": "9 m", "Peso/Varilla": "14.0 kg"},
                "base_price": 63.50
            },
            {
                "id": 56,
                "name": "Varilla de Acero Corrugado Siderperu 3/4\" (9m)",
                "brand": "Siderperu",
                "category": "Materiales",
                "description": "Fierro estructural pesado Siderperu de 3/4 pulgada para obras de concreto armado complejas.",
                "icon": "🦯",
                "specs": {"Diámetro": "3/4\" (19.1 mm)", "Longitud": "9 m", "Peso/Varilla": "20.0 kg"},
                "base_price": 91.50
            },

            # --- CATEGORÍA: AGREGADOS (IDs 57-62) ---
            {
                "id": 57,
                "name": "Arena Gruesa por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Arena de grano grueso y limpio, ideal para preparar morteros de asentado de ladrillos y dosificación de concreto estructural.",
                "icon": "🏜️",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1600 kg/m³"},
                "base_price": 65.00
            },
            {
                "id": 58,
                "name": "Arena Fina por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Arena fina cribada de río. Ideal para tarrajeo liso en interiores y acabados finos de muros.",
                "icon": "⏳",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1500 kg/m³"},
                "base_price": 70.00
            },
            {
                "id": 59,
                "name": "Piedra Chancada de 1/2\" por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Piedra chancada triturada de 1/2 pulgada, ideal para dosificación de concreto de f'c = 210 kg/cm².",
                "icon": "🪨",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1550 kg/m³"},
                "base_price": 75.00
            },
            {
                "id": 60,
                "name": "Piedra Chancada de 3/4\" por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Piedra chancada triturada de 3/4 de pulgada. Usada en concretos estructurales densos y zapatas de cimentación.",
                "icon": "🪨",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1550 kg/m³"},
                "base_price": 75.00
            },
            {
                "id": 61,
                "name": "Hormigón de Concreto por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Mezcla natural de piedra y arena ideal para concretos de cimientos, sobrecimientos y falsos pisos.",
                "icon": "🪨",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1700 kg/m³"},
                "base_price": 55.00
            },
            {
                "id": 62,
                "name": "Afirmado por Metro Cúbico (m³)",
                "brand": "Cantera local",
                "category": "Materiales",
                "description": "Material afirmado compactable ideal para bases de pisos y nivelación previa al vaciado de falsos pisos.",
                "icon": "🏜️",
                "specs": {"Unidad": "m³ (Cubo)", "Densidad aprox": "1800 kg/m³"},
                "base_price": 45.00
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
