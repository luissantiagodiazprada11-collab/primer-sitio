#!/usr/bin/env python3
"""Build the Spanish and English ST3 Pro pages from one template.

    python3 src/build.py   ->  st3-pro-es.html, st3-pro-en.html (repo root)

Camera moves and callout positions are shared; only the copy changes.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "src" / "st3-pro.template.html").read_text(encoding="utf-8")

# Shared per-scene staging: camera (focus point in scooter coords, zoom,
# optional screen target) and callout anchor geometry.
STAGING = {
    "intro":      {"cam": {"f": [300, 205], "z": 1.15}, "d": 5600, "screen": "25"},
    "motor":      {"cam": {"f": [130, 312], "z": 2.3}, "screen": "25",
                   "callouts": [{"p": [146, 300], "dx": 60, "dy": -190, "len": 170}]},
    "battery":    {"cam": {"f": [300, 270], "z": 1.85}, "screen": "25",
                   "callouts": [{"p": [250, 272], "dx": 40, "dy": -120, "len": 170}]},
    "suspension": {"cam": {"f": [300, 290], "z": 1.15}, "screen": "22",
                   "callouts": [{"p": [172, 301], "dx": -40, "dy": 190, "len": 150},
                                {"p": [454, 300], "dx": 40, "dy": 190, "len": 150}]},
    "tires":      {"cam": {"f": [470, 312], "z": 2.3}, "screen": "25",
                   "callouts": [{"p": [504, 278], "dx": 50, "dy": -90, "len": 160}]},
    "brakes":     {"cam": {"f": [300, 260], "z": 1.1}, "screen": "0", "halt": 950,
                   "callouts": [{"p": [130, 312], "dx": 30, "dy": 170, "len": 130},
                                {"p": [470, 312], "dx": -30, "dy": 170, "len": 130}]},
    "lights":     {"cam": {"f": [300, 230], "z": 1.05}, "screen": "18",
                   "callouts": [{"p": [440, 198], "dx": -60, "dy": -230, "len": 150},
                                {"p": [300, 291], "dx": -40, "dy": 150, "len": 160},
                                {"p": [66, 299], "dx": 30, "dy": -170, "len": 140}]},
    "smart":      {"cam": {"f": [405, 110], "z": 1.9, "t": [300, 560]}, "screen": "25",
                   "callouts": [{"p": [396, 70], "dx": -40, "dy": -110, "len": 150},
                                {"p": [430, 180], "dx": -50, "dy": 110, "len": 150}]},
    "speed":      {"cam": {"f": [300, 240], "z": 0.95}, "screen": "speed"},
    "press":      {"cam": {"f": [300, 240], "z": 0.9}, "screen": "25", "d": 8800},
    "outro":      {"cam": {"f": [300, 300], "z": 0.82}, "screen": "P", "d": 10000, "halt": 0},
}

ES = {
    "file": "st3-pro-es.html",
    "locale": "es-CO",
    "ui": {
        "lang": "es", "alt_lang": "en", "alt_href": "st3-pro-en.html",
        "title": "ST3 Pro en movimiento",
        "description": "Presentación animada del scooter eléctrico Navee ST3 Pro: 1.350 W, 596,7 Wh, suspensión Damping Arm, llantas tubeless de 10\", Apple Find My e IPX5.",
        "a_player": "Reproductor", "a_roledesc": "presentación",
        "a_stage": "Animación del Navee ST3 Pro. Toca los lados para cambiar de escena o el centro para pausar.",
        "a_lang": "Idioma",
        "b_restart": "Volver al inicio", "b_prev": "Escena anterior", "b_pause": "Pausar",
        "b_next": "Escena siguiente", "b_fs": "Pantalla completa",
        "hint_keys": "<kbd>←</kbd> <kbd>→</kbd> navegar · <kbd>Espacio</kbd> pausa · <kbd>F</kbd> pantalla completa",
        "hint_touch": "Toca los lados para navegar · mantén presionado para pausar",
        "kicker": "Presentación animada",
        "lang_switch": '<span aria-current="true">ES</span><a href="st3-pro-en.html" hreflang="en" lang="en">EN</a>',
        "lead": "El scooter eléctrico para la ciudad, en once escenas: motor, batería, suspensión, llantas, frenos, luces, conectividad, velocidad y lo que dice la prensa.",
        "rec_link": "Modo grabación 9:16",
        "sources_title": "Fuentes",
        "src_official": "ficha técnica oficial (UE)",
        "note": "Animación de fan, no oficial. Datos tomados de la ficha técnica oficial y de reseñas independientes. Algunas cifras (velocidad máxima, potencia nominal) varían según el mercado. La autonomía real depende del peso, el terreno, el clima y el modo de manejo.",
        "ph_status": "Conectado", "ph_battery": "≈ 41 km", "ph_lock": "Bloquear",
        "ph_cruise": "Crucero", "ph_prox": "Desbloqueo por proximidad",
    },
    "js_ui": {"scene": "Escena", "pause": "Pausar", "play": "Reproducir"},
    "scenes": {
        "intro": {"nav": "Presentación", "v": "ST3 Pro", "eyebrow": "Presentamos", "stat": "ST3 PRO",
                  "label": "Navee · Movilidad urbana",
                  "cap": "Potencia de sobra, suspensión de cuatro brazos y tecnología inteligente para moverte por la ciudad."},
        "motor": {"nav": "Motor", "v": "1.350 W", "eyebrow": "01 — Motor", "num": 1350, "unit": "W",
                  "label": "Potencia pico",
                  "specs": [["600 W", "Nominal"], ["28 %", "Pendiente máx."], ["Trasero", "Tracción"]],
                  "cap": "En pruebas independientes subió una cuesta del 17\u00a0% a casi 17\u00a0km/h.",
                  "callouts": [{"t": "Motor trasero", "s": "600 W nominales"}]},
        "battery": {"nav": "Batería", "v": "596,7 Wh", "eyebrow": "02 — Batería", "num": 596.7, "dec": 1, "unit": "Wh",
                    "label": "Batería de 48 V",
                    "range": {"a": 53.33, "b": 66.67, "real": "Real 40–50 km", "max": "Máx. 75 km"},
                    "specs": [["48 V", "Voltaje"], ["18650", "Celdas 13S5P"], ["8–10 h", "Carga completa"]],
                    "cap": "Hasta 75 km declarados a 15 km/h. En pruebas reales, entre 40 y 50 km.",
                    "callouts": [{"t": "Pack 48 V", "s": "Integrado en el deck"}]},
        "suspension": {"nav": "Suspensión", "v": "4 brazos", "eyebrow": "03 — Suspensión", "num": 4,
                       "label": "Brazos Damping Arm",
                       "specs": [["2", "Delanteros"], ["2", "Traseros"], ["Elastómero", "Amortiguación"]],
                       "cap": "Las reseñas la ubican entre las más suaves de su categoría: se traga baches, grietas y andenes.",
                       "callouts": [{"t": "Trasera", "s": "2 brazos"}, {"t": "Delantera", "s": "2 brazos"}]},
        "tires": {"nav": "Llantas", "v": "10\" × 2,5\"", "eyebrow": "04 — Llantas", "stat": "10\"",
                  "label": "Tubeless autosellantes",
                  "specs": [["10\" × 2,5\"", "Medida"], ["Sin cámara", "Tubeless"], ["Gel sellante", "Anti-pinchazos"]],
                  "cap": "Neumáticos anchos que sellan solos los pinchazos pequeños y dan más agarre en el asfalto.",
                  "callouts": [{"t": "10\" Tubeless", "s": "Autosellante"}]},
        "brakes": {"nav": "Frenado", "v": "3 + TCS", "eyebrow": "05 — Frenado", "num": 3,
                   "label": "Sistemas de freno",
                   "specs": [["Tambor", "Delantero"], ["Disco", "Trasero"], ["E-ABS", "3 niveles"]],
                   "cap": "Con control de tracción TCS, que evita que la rueda patine al acelerar o frenar fuerte.",
                   "callouts": [{"t": "Disco", "s": "Trasero"}, {"t": "Tambor", "s": "Delantero"}]},
        "lights": {"nav": "Iluminación", "v": "RGB", "eyebrow": "06 — Iluminación", "stat": "RGB",
                   "label": "Luz ambiental en el deck",
                   "specs": [["Auto", "Faro con sensor"], ["LED", "Luz de freno"], ["Manubrio", "Direccionales"]],
                   "cap": "El faro se enciende solo al anochecer y el color de las luces del deck se elige desde la app.",
                   "callouts": [{"t": "Faro automático", "s": "Sensor de luz"},
                                {"t": "Luz ambiental RGB", "s": "Personalizable"},
                                {"t": "Luz de freno", "s": "LED"}]},
        "smart": {"nav": "Conectividad", "v": "Find My", "eyebrow": "07 — Conectividad", "stat": "App",
                  "label": "+ Apple Find My",
                  "specs": [["Find My", "Localización iOS"], ["Proximidad", "Desbloqueo"], ["Crucero", "Control"]],
                  "cap": "Encuéntralo desde tu iPhone, bloquéalo desde la app y desbloquéalo con solo acercarte.",
                  "callouts": [{"t": "Pantalla", "s": "Velocidad y modo"}, {"t": "IPX5", "s": "Resiste salpicaduras"}]},
        "speed": {"nav": "Velocidad", "v": "40 km/h", "eyebrow": "08 — Rendimiento", "num": 40, "unit": "km/h", "sup": "*",
                  "label": "Velocidad máxima",
                  "specs": [["3 + peatón", "Modos"], ["120 kg", "Carga máx."], ["25,3 kg", "Peso"]],
                  "cap": "Medido en pruebas: 40,4 km/h reales. Respeta siempre el límite de tu ciudad.",
                  "foot": "*Versión internacional. En la Unión Europea se limita a 25 km/h."},
        "press": {"nav": "Prensa", "v": "4 reseñas", "eyebrow": "La prensa opina",
                  "quotes": [["Es como un Rolls-Royce.", "New Atlas"],
                             ["Un scooter sólido con una suspensión seria.", "The Gadgeteer"],
                             ["Potente, divertido, útil.", "Cult of Mac"],
                             ["El mejor scooter urbano de 2025.", "AndroidGuys"]],
                  "fine": "Titulares de reseñas, traducidos del inglés."},
        "outro": {"nav": "Ficha técnica", "v": "Resumen", "eyebrow": "Navee", "stat": "ST3 PRO",
                  "label": "Hecho para la ciudad",
                  "sheet": [["bolt", "1.350 W", "Potencia pico"], ["pin", "75 km", "Autonomía declarada"],
                            ["battery", "596,7 Wh", "Batería 48 V"], ["spring", "4 brazos", "Suspensión"],
                            ["tire", "10\" × 2,5\"", "Tubeless"], ["slope", "28 %", "Pendiente máx."],
                            ["weight", "25,3 kg", "Peso"], ["drop", "IPX5", "Resistencia al agua"],
                            ["locate", "Find My", "Localización"]],
                  "fine": "Animación de fan, no oficial. Datos de la ficha técnica oficial y reseñas independientes; pueden variar según el mercado."},
    },
}

EN = {
    "file": "st3-pro-en.html",
    "locale": "en-US",
    "ui": {
        "lang": "en", "alt_lang": "es", "alt_href": "st3-pro-es.html",
        "title": "ST3 Pro in Motion",
        "description": "Animated showcase of the Navee ST3 Pro electric scooter: 1,350 W, 596.7 Wh, Damping Arm suspension, 10\" tubeless tires, Apple Find My and IPX5.",
        "a_player": "Player", "a_roledesc": "presentation",
        "a_stage": "Navee ST3 Pro animation. Tap the sides to change scenes or the center to pause.",
        "a_lang": "Language",
        "b_restart": "Back to start", "b_prev": "Previous scene", "b_pause": "Pause",
        "b_next": "Next scene", "b_fs": "Full screen",
        "hint_keys": "<kbd>←</kbd> <kbd>→</kbd> navigate · <kbd>Space</kbd> pause · <kbd>F</kbd> full screen",
        "hint_touch": "Tap the sides to navigate · press and hold to pause",
        "kicker": "Animated showcase",
        "lang_switch": '<a href="st3-pro-es.html" hreflang="es" lang="es">ES</a><span aria-current="true">EN</span>',
        "lead": "The city electric scooter, in eleven scenes: motor, battery, suspension, tires, brakes, lights, connectivity, speed and what the press says.",
        "rec_link": "9:16 recording mode",
        "sources_title": "Sources",
        "src_official": "official spec sheet (EU)",
        "note": "Unofficial fan animation. Data from the official spec sheet and independent reviews. Some figures (top speed, rated power) vary by market. Real-world range depends on rider weight, terrain, weather and riding mode.",
        "ph_status": "Connected", "ph_battery": "≈ 25 mi", "ph_lock": "Lock",
        "ph_cruise": "Cruise", "ph_prox": "Proximity unlock",
    },
    "js_ui": {"scene": "Scene", "pause": "Pause", "play": "Play"},
    "scenes": {
        "intro": {"nav": "Intro", "v": "ST3 Pro", "eyebrow": "Introducing", "stat": "ST3 PRO",
                  "label": "Navee · Urban mobility",
                  "cap": "Plenty of power, four-arm suspension and smart tech for getting around the city."},
        "motor": {"nav": "Motor", "v": "1,350 W", "eyebrow": "01 — Motor", "num": 1350, "unit": "W",
                  "label": "Peak power",
                  "specs": [["600 W", "Rated"], ["28%", "Max. grade"], ["Rear", "Drive"]],
                  "cap": "In independent testing it climbed a 17% grade at 10.5 mph.",
                  "callouts": [{"t": "Rear motor", "s": "600 W rated"}]},
        "battery": {"nav": "Battery", "v": "596.7 Wh", "eyebrow": "02 — Battery", "num": 596.7, "dec": 1, "unit": "Wh",
                    "label": "48 V battery",
                    "range": {"a": 53.65, "b": 66.52, "real": "Tested 25–31 mi", "max": "Max 46.6 mi"},
                    "specs": [["48 V", "Voltage"], ["18650", "Cells 13S5P"], ["8–10 h", "Full charge"]],
                    "cap": "Up to 46.6 miles claimed at 9 mph. Real-world tests: 25 to 31 miles.",
                    "callouts": [{"t": "48 V pack", "s": "Built into the deck"}]},
        "suspension": {"nav": "Suspension", "v": "4 arms", "eyebrow": "03 — Suspension", "num": 4,
                       "label": "Damping Arm suspension",
                       "specs": [["2", "Front"], ["2", "Rear"], ["Elastomer", "Damping"]],
                       "cap": "Reviewers call it one of the smoothest rides in its class. Potholes, cracks and curbs disappear.",
                       "callouts": [{"t": "Rear", "s": "2 arms"}, {"t": "Front", "s": "2 arms"}]},
        "tires": {"nav": "Tires", "v": "10\" × 2.5\"", "eyebrow": "04 — Tires", "stat": "10\"",
                  "label": "Self-sealing tubeless",
                  "specs": [["10\" × 2.5\"", "Size"], ["Tubeless", "No inner tube"], ["Sealant gel", "Puncture-resistant"]],
                  "cap": "Wide tires that seal small punctures on their own and grip the road better.",
                  "callouts": [{"t": "10\" Tubeless", "s": "Self-sealing"}]},
        "brakes": {"nav": "Braking", "v": "3 + TCS", "eyebrow": "05 — Braking", "num": 3,
                   "label": "Braking systems",
                   "specs": [["Drum", "Front"], ["Disc", "Rear"], ["E-ABS", "3 levels"]],
                   "cap": "Plus TCS traction control, which keeps the wheel from slipping under hard acceleration or braking.",
                   "callouts": [{"t": "Disc", "s": "Rear"}, {"t": "Drum", "s": "Front"}]},
        "lights": {"nav": "Lighting", "v": "RGB", "eyebrow": "06 — Lighting", "stat": "RGB",
                   "label": "Deck ambient lighting",
                   "specs": [["Auto", "Light-sensing lamp"], ["LED", "Brake light"], ["Handlebar", "Turn signals"]],
                   "cap": "The headlight switches on by itself at dusk, and you pick the deck light color in the app.",
                   "callouts": [{"t": "Auto headlight", "s": "Light sensor"},
                                {"t": "RGB ambient light", "s": "Customizable"},
                                {"t": "Brake light", "s": "LED"}]},
        "smart": {"nav": "Connectivity", "v": "Find My", "eyebrow": "07 — Connectivity", "stat": "App",
                  "label": "+ Apple Find My",
                  "specs": [["Find My", "iOS tracking"], ["Proximity", "Unlock"], ["Cruise", "Control"]],
                  "cap": "Find it from your iPhone, lock it from the app and unlock it just by walking up.",
                  "callouts": [{"t": "Display", "s": "Speed and mode"}, {"t": "IPX5", "s": "Splash resistant"}]},
        "speed": {"nav": "Speed", "v": "25 mph", "eyebrow": "08 — Performance", "num": 25, "unit": "mph", "sup": "*",
                  "label": "Top speed",
                  "specs": [["3 + walk", "Modes"], ["265 lb", "Max. load"], ["55.8 lb", "Weight"]],
                  "cap": "Clocked at 25.1 mph in independent testing. Always ride within local limits.",
                  "foot": "*US version. EU models are limited to 25 km/h (15.5 mph)."},
        "press": {"nav": "Press", "v": "4 reviews", "eyebrow": "What reviewers say",
                  "quotes": [["It's like a Rolls-Royce.", "New Atlas"],
                             ["Solid scooter with serious suspension.", "The Gadgeteer"],
                             ["Powerful, fun, useful.", "Cult of Mac"],
                             ["The Best Commuter Scooter of 2025.", "AndroidGuys"]],
                  "fine": "Review headlines."},
        "outro": {"nav": "Spec sheet", "v": "Summary", "eyebrow": "Navee", "stat": "ST3 PRO",
                  "label": "Built for the city",
                  "sheet": [["bolt", "1,350 W", "Peak power"], ["pin", "46.6 mi", "Claimed range"],
                            ["battery", "596.7 Wh", "48 V battery"], ["spring", "4 arms", "Suspension"],
                            ["tire", "10\" × 2.5\"", "Tubeless"], ["slope", "28%", "Max. grade"],
                            ["weight", "55.8 lb", "Weight"], ["drop", "IPX5", "Water resistance"],
                            ["locate", "Find My", "Tracking"]],
                  "fine": "Unofficial fan animation. Data from the official spec sheet and independent reviews; may vary by market."},
    },
}


def scenes_for(lang):
    out = []
    for sid, stage in STAGING.items():
        text = dict(lang["scenes"][sid])
        scene = {"id": sid, **stage, **text}
        if "callouts" in stage:
            labels = text.get("callouts", [])
            scene["callouts"] = [{**geo, **lbl} for geo, lbl in zip(stage["callouts"], labels)]
        out.append(scene)
    return out


def build(lang):
    html = TEMPLATE
    for key, val in lang["ui"].items():
        html = html.replace("{{" + key + "}}", val)
    assert "{{" not in html, "unfilled placeholder in template"
    data = {"locale": lang["locale"], "ui": lang["js_ui"], "scenes": scenes_for(lang)}
    html = html.replace("/*DATA*/", json.dumps(data, ensure_ascii=False))
    (ROOT / lang["file"]).write_text(html, encoding="utf-8")
    print("wrote", lang["file"])


if __name__ == "__main__":
    for lang in (ES, EN):
        build(lang)
