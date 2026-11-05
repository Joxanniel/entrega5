import os

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

# --------------------------------------------------
# Configuración general
# --------------------------------------------------

st.set_page_config(
    page_title="Derechos son tuyos",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

URL_APP = "https://hukupc3tapvxtdambwhebk.streamlit.app/"
URL_PROYECTO = "https://espaciosabiertos.org/derecho-a-tener-derechos-2/"

MAPA = "images/mapa.png"
LOGO_EA = "images/logo-espacios-abiertos.png"
LOGO_CPI = "images/logo-cpi.png"

# --------------------------------------------------
# Contenido (separado del diseño)
# Revisa estos textos y enlaces antes de entregar.
# --------------------------------------------------

ORGANIZACIONES = {
    "proyecto": (
        "«Derechos. Son tuyos. Defiéndelos.» es una serie de videos y materiales "
        "educativos sobre derechos humanos y derechos constitucionales de Puerto Rico. "
        "Fue un esfuerzo conjunto de Espacios Abiertos y el Centro de Periodismo "
        "Investigativo. Se presentó como servicio público por WIPR y recibió un "
        "premio Emmy en 2016."
    ),
    "ea": (
        "Espacios Abiertos es una organización sin fines de lucro de Puerto Rico que "
        "promueve la transparencia, el acceso a la información y la participación "
        "ciudadana."
    ),
    "cpi": (
        "El Centro de Periodismo Investigativo (CPI) es una organización periodística "
        "sin fines de lucro de Puerto Rico que investiga temas de interés público y "
        "defiende el acceso a la información."
    ),
}

# x0 y x1 marcan la zona del edificio en la imagen del mapa (ancho original = 1200 px)
DERECHOS = [
    {
        "id": "educacion",
        "numero": 1,
        "lugar": "Escuela",
        "nombre": "Educación",
        "icono": "🎓",
        "color": "#E8F1FF",
        "acento": "#2457A7",
        "x0": 50, "x1": 410,
        "resumen": (
            "La Constitución de Puerto Rico dice que toda persona tiene derecho a una "
            "educación que la ayude a desarrollarse plenamente y a respetar los "
            "derechos humanos."
        ),
        "sabias_que": (
            "El derecho a la educación no es solo tener una escuela. También incluye "
            "poder llegar a ella, tener maestros y materiales, y recibir acomodos si "
            "los necesitas."
        ),
        "video": "",  # Pega aquí el enlace oficial del video (YouTube o Vimeo)
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Educacion-FINAL.pdf",
        "pregunta": "¿Cuál de estas situaciones afecta el derecho a la educación?",
        "opciones": [
            "Cierran la escuela del barrio y no ofrecen otra cerca ni transporte.",
            "La maestra asigna un proyecto largo para el viernes.",
            "La escuela cambia el horario del recreo.",
        ],
        "correcta": 0,
        "explicacion": (
            "Si cierran una escuela y no hay otra opción ni transporte, los "
            "estudiantes pierden acceso a la educación. Una tarea larga o un cambio de "
            "horario pueden ser molestos, pero no impiden estudiar."
        ),
    },
    {
        "id": "salud",
        "numero": 2,
        "lugar": "Hospital",
        "nombre": "Salud",
        "icono": "🩺",
        "color": "#FFF0F1",
        "acento": "#A83246",
        "x0": 430, "x1": 770,
        "resumen": (
            "La Declaración Universal de Derechos Humanos reconoce que toda persona "
            "tiene derecho a un nivel de vida adecuado que le asegure la salud y la "
            "asistencia médica."
        ),
        "sabias_que": (
            "No basta con que exista un hospital. Si una persona no puede pagar, no "
            "tiene cómo llegar o espera meses por una cita urgente, su derecho a la "
            "salud se ve afectado."
        ),
        "video": "",
        "pdf": "",
        "pregunta": "¿Cuál situación muestra una barrera para el derecho a la salud?",
        "opciones": [
            "Una persona prefiere ir al médico en la mañana.",
            "En el pueblo no hay centro de salud y la persona no tiene cómo llegar al más cercano.",
            "El médico le receta un medicamento para el catarro.",
        ],
        "correcta": 1,
        "explicacion": (
            "La distancia y la falta de transporte son barreras reales: impiden "
            "recibir atención médica. Escoger un horario o recibir una receta no "
            "limita el acceso."
        ),
    },
    {
        "id": "vivienda",
        "numero": 3,
        "lugar": "Casa",
        "nombre": "Vivienda",
        "icono": "🏠",
        "color": "#FFF4E6",
        "acento": "#9B5700",
        "x0": 800, "x1": 1140,
        "resumen": (
            "La Declaración Universal de Derechos Humanos también incluye la vivienda: "
            "toda persona necesita un lugar seguro y adecuado para vivir con dignidad."
        ),
        "sabias_que": (
            "Cuando el alquiler sube tanto que una familia tiene que irse de su "
            "comunidad, no solo cambia de dirección: puede perder su escuela, su "
            "trabajo y su red de apoyo."
        ),
        "video": "",
        "pdf": "",
        "pregunta": "¿Cuál situación afecta el derecho a una vivienda adecuada?",
        "opciones": [
            "Una familia decide pintar su casa de otro color.",
            "Un vecino se muda a otro pueblo porque consiguió un trabajo nuevo.",
            "Una familia tiene que irse de su comunidad porque el alquiler subió y no puede pagarlo.",
        ],
        "correcta": 2,
        "explicacion": (
            "Tener que abandonar tu hogar porque no puedes pagarlo afecta el derecho a "
            "la vivienda. Mudarse por decisión propia o pintar la casa no lo afecta."
        ),
    },
]

TOTAL = len(DERECHOS)

# --------------------------------------------------
# Estado de la aplicación
# --------------------------------------------------

DEFAULTS = {
    "pantalla": "inicio",
    "anterior": "inicio",
    "actual": 0,
    "completados": [],
    "letra_grande": False,
    "menos_animacion": False,
}
for clave, valor in DEFAULTS.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor if not isinstance(valor, list) else []


def ir(pantalla, actual=None):
    if pantalla == "ayuda":
        st.session_state.anterior = st.session_state.pantalla
    if actual is not None:
        st.session_state.actual = actual
    st.session_state.pantalla = pantalla


def completar(indice):
    if indice not in st.session_state.completados:
        st.session_state.completados.append(indice)


def siguiente():
    if len(st.session_state.completados) == TOTAL:
        ir("final")
    else:
        ir("mapa")


def reiniciar():
    st.session_state.completados = []
    for d in DERECHOS:
        st.session_state.pop(f"resp_{d['id']}", None)
        st.session_state.pop(f"ok_{d['id']}", None)
    ir("inicio")


# --------------------------------------------------
# Estilos visuales
# --------------------------------------------------

base = 1.15 if st.session_state.letra_grande else 1.0
animacion = "" if st.session_state.menos_animacion else """
    .block-container > div { animation: aparecer .45s ease-out; }
    @keyframes aparecer { from {opacity: 0; transform: translateY(12px);} to {opacity: 1; transform: none;} }
"""

st.markdown(
    f"""
    <style>
    html {{ font-size: {base * 100}%; }}
    .block-container {{ max-width: 760px; padding-top: 1.5rem; padding-bottom: 4rem; }}
    {animacion}
    .hero {{
        padding: 1.8rem; border-radius: 22px; color: white; margin-bottom: 1.2rem;
        background: linear-gradient(135deg, #1B385E 0%, #45698F 100%);
    }}
    .hero h1 {{ color: white; margin: 0; font-size: 2.4rem; line-height: 1.1; }}
    .hero p {{ font-size: 1.1rem; line-height: 1.5; margin: .8rem 0 0 0; }}
    .etiqueta {{ text-transform: uppercase; letter-spacing: .08em; font-weight: 700;
        font-size: .8rem; opacity: .85; margin-bottom: .4rem; }}
    .tarjeta {{ border-radius: 20px; padding: 1.5rem; margin: .6rem 0 1.2rem 0;
        border: 1px solid rgba(30,40,50,.12); box-shadow: 0 8px 24px rgba(20,35,50,.08); }}
    .tarjeta h2 {{ margin: .2rem 0 .6rem 0; }}
    .tarjeta p {{ font-size: 1.08rem; line-height: 1.6; margin: 0; color: #1E2A36; }}
    .lugar {{ font-size: 1.05rem; padding: .35rem 0; }}
    .pie {{ text-align: center; color: #5E6872; font-size: .85rem; margin-top: 2.5rem; }}
    div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a {{
        border-radius: 999px; min-height: 3rem; font-weight: 650; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Aviso de prototipo en progreso
# --------------------------------------------------

st.markdown(
    """
    <div role="note" style="border:2px dashed #9B5700; background:#FFF4E6; color:#5A3300;
         border-radius:14px; padding:.7rem 1rem; margin-bottom:1rem; font-size:.95rem;">
        🚧 <b>Prototipo en progreso.</b> Faltan los videos oficiales, algunos PDF y los logos,
        y los derechos escogidos están pendientes de aprobación.
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Barra de navegación (siempre visible)
# --------------------------------------------------

pantalla = st.session_state.pantalla
nav1, nav2, nav3 = st.columns(3)
nav1.button("🏠 Inicio", on_click=ir, args=("inicio",), width="stretch",
            disabled=pantalla == "inicio")
nav2.button("🗺️ Mapa", on_click=ir, args=("mapa",), width="stretch",
            disabled=pantalla == "mapa")
nav3.button("❓ Ayuda", on_click=ir, args=("ayuda",), width="stretch",
            disabled=pantalla == "ayuda")


def barra_progreso():
    hechos = len(st.session_state.completados)
    st.progress(hechos / TOTAL, text=f"Progreso: {hechos} de {TOTAL} derechos completados")


def mapa_con_marcas():
    """Abre el mapa y dibuja un ✓ verde sobre los lugares completados."""
    imagen = Image.open(MAPA).convert("RGB")
    dibujo = ImageDraw.Draw(imagen)
    for i in st.session_state.completados:
        d = DERECHOS[i]
        cx = (d["x0"] + d["x1"]) // 2
        cy = 150
        dibujo.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill="#1E7B3A", outline="white", width=6)
        dibujo.line([(cx - 18, cy), (cx - 5, cy + 15), (cx + 20, cy - 14)], fill="white", width=9)
    return imagen


# --------------------------------------------------
# Pantalla 1: Inicio
# --------------------------------------------------

def pantalla_inicio():
    logos = [p for p in (LOGO_EA, LOGO_CPI) if os.path.exists(p)]
    if logos:
        cols = st.columns(len(logos))
        for col, ruta in zip(cols, logos):
            nombre = "Espacios Abiertos" if "espacios" in ruta else "Centro de Periodismo Investigativo"
            col.image(ruta, caption=f"Logo de {nombre}", width="stretch")

    st.markdown(
        """
        <div class="hero">
            <div class="etiqueta">Experiencia interactiva</div>
            <h1>Derechos son tuyos</h1>
            <p>Recorre tu comunidad y descubre cómo tus derechos aparecen en lugares
            que conoces: la escuela, el hospital y tu casa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(MAPA, caption="Ilustración de una comunidad con una escuela, un hospital y una casa.",
             width="stretch")
    st.markdown("**Tiempo aproximado:** 10 minutos · **3 lugares** · una pregunta en cada uno")
    st.button("Comenzar →", type="primary", on_click=ir, args=("mapa",), width="stretch")
    with st.expander("¿Qué es «Derechos son tuyos»?"):
        st.write(ORGANIZACIONES["proyecto"])
        st.link_button("Ver el proyecto original (sitio externo) ↗", URL_PROYECTO)


# --------------------------------------------------
# Pantalla 2: Mapa con hotspots
# --------------------------------------------------

def pantalla_mapa():
    st.markdown("## Mi comunidad")
    st.write("Toca un **lugar con número** para descubrir el derecho que hay ahí.")
    barra_progreso()

    clic = streamlit_image_coordinates(
        mapa_con_marcas(), key="clic_mapa", width="stretch", cursor="pointer"
    )
    st.caption("Mapa: 1 Escuela, 2 Hospital, 3 Casa. Los lugares completados tienen un ✓.")

    if clic and clic.get("width"):
        x = clic["x"] * 1200 / clic["width"]
        firma = (clic["x"], clic["y"], clic.get("unix_time"))
        if st.session_state.get("ultimo_clic") != firma:
            st.session_state.ultimo_clic = firma
            for i, d in enumerate(DERECHOS):
                if d["x0"] <= x <= d["x1"]:
                    ir("aprender", i)
                    st.rerun()

    st.markdown("**O escoge de la lista:**")
    for i, d in enumerate(DERECHOS):
        hecho = i in st.session_state.completados
        etiqueta = f"{d['numero']}. {d['lugar']} → {d['nombre']}" + ("  ✓ completado" if hecho else "")
        st.button(etiqueta, key=f"lista_{d['id']}", on_click=ir, args=("aprender", i),
                  width="stretch")


# --------------------------------------------------
# Pantalla 3: Aprender
# --------------------------------------------------

def pantalla_aprender():
    i = st.session_state.actual
    d = DERECHOS[i]

    a, b = st.columns([1, 1])
    a.button("← Mapa", on_click=ir, args=("mapa",))
    b.markdown(f"<div style='text-align:right;padding-top:.6rem'><b>Lugar {i + 1} de {TOTAL}</b></div>",
               unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="tarjeta" style="background:{d['color']}; border-top: 8px solid {d['acento']};">
            <div style="font-size:2.6rem" aria-hidden="true">{d['icono']}</div>
            <div class="etiqueta" style="color:{d['acento']}">{d['lugar']}</div>
            <h2 style="color:{d['acento']}">Derecho a la {d['nombre'].lower()}</h2>
            <p>{d['resumen']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recorte = Image.open(MAPA).crop((d["x0"], 180, d["x1"], 650))
    st.image(recorte, caption=f"Ilustración de la {d['lugar'].lower()} de la comunidad.", width=260)

    with st.expander("💡 ¿Sabías que...? (toca para ver)"):
        st.write(d["sabias_que"])

    st.markdown("### Recursos")
    if d["video"]:
        st.video(d["video"])
        st.caption("Si el video tiene subtítulos, actívalos con el botón CC del reproductor.")
    else:
        st.info("🎬 Video: pendiente de añadir el enlace oficial.")
    if d["pdf"]:
        st.link_button("📄 Abrir material educativo (PDF, sitio externo) ↗", d["pdf"],
                       width="stretch")
    else:
        st.info("📄 PDF: pendiente de añadir el enlace oficial.")

    st.button("Ir a la pregunta →", type="primary", on_click=ir, args=("actividad",),
              width="stretch")


# --------------------------------------------------
# Pantalla 4: Actividad
# --------------------------------------------------

def pantalla_actividad():
    i = st.session_state.actual
    d = DERECHOS[i]

    a, b = st.columns([1, 1])
    a.button("← Volver", on_click=ir, args=("aprender",))
    b.markdown(f"<div style='text-align:right;padding-top:.6rem'><b>Lugar {i + 1} de {TOTAL}</b></div>",
               unsafe_allow_html=True)

    st.markdown(f"## Pon a prueba lo aprendido\n**{d['icono']} {d['nombre']}**")
    st.markdown(f"#### {d['pregunta']}")

    eleccion = st.radio("Escoge una respuesta:", range(len(d["opciones"])),
                        format_func=lambda k: d["opciones"][k], index=None, key=f"resp_{d['id']}")

    if st.button("Comprobar", type="primary", width="stretch"):
        if eleccion is None:
            st.warning("Escoge una opción antes de comprobar.")
        elif eleccion == d["correcta"]:
            st.session_state[f"ok_{d['id']}"] = True
            completar(i)
        else:
            st.session_state[f"ok_{d['id']}"] = False

    resultado = st.session_state.get(f"ok_{d['id']}")
    if resultado is True:
        st.success(f"✓ ¡Correcto! {d['explicacion']}")
        etiqueta = "Ver mi resultado final →" if len(st.session_state.completados) == TOTAL \
            else "Siguiente lugar →"
        st.button(etiqueta, type="primary", on_click=siguiente, width="stretch")
    elif resultado is False:
        st.error("✗ Todavía no. Vuelve a leer la situación y piensa: ¿cuál impide que una persona "
                 "ejerza su derecho? Intenta otra vez.")


# --------------------------------------------------
# Pantalla 5: Final
# --------------------------------------------------

def pantalla_final():
    if not st.session_state.menos_animacion and not st.session_state.get("celebrado"):
        st.balloons()
        st.session_state.celebrado = True

    st.markdown(
        f"""
        <div class="hero" style="text-align:center">
            <div style="font-size:3rem" aria-hidden="true">🏅</div>
            <h1>¡Completaste el recorrido!</h1>
            <p>{TOTAL} de {TOTAL} derechos. Ahora puedes reconocer tus derechos en lugares
            de tu comunidad y sabes dónde buscar más información.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Comparte la app")
    st.code(URL_APP, language=None)
    st.caption("Usa el botón de copiar (esquina del recuadro) para copiar el enlace.")
    c1, c2 = st.columns(2)
    c1.link_button("Compartir por WhatsApp ↗",
                   f"https://wa.me/?text=Aprende%20sobre%20tus%20derechos%3A%20{URL_APP}",
                   width="stretch")
    c2.link_button("Compartir por correo ↗",
                   f"mailto:?subject=Derechos%20son%20tuyos&body={URL_APP}",
                   width="stretch")

    st.markdown("### Todos los recursos")
    for d in DERECHOS:
        st.markdown(f"**{d['icono']} {d['nombre']}**")
        if d["pdf"]:
            st.link_button(f"PDF de {d['nombre']} ↗", d["pdf"])
        if d["video"]:
            st.link_button(f"Video de {d['nombre']} ↗", d["video"])
    st.link_button("Proyecto completo en Espacios Abiertos ↗", URL_PROYECTO)

    st.button("← Volver al inicio y empezar otra vez", on_click=reiniciar, width="stretch")


# --------------------------------------------------
# Pantalla 6: Ayuda, acerca y ajustes
# --------------------------------------------------

def pantalla_ayuda():
    st.button("← Volver", on_click=ir, args=(st.session_state.anterior,))
    st.markdown("## Cómo usar la app")
    st.markdown(
        "1. Toca un lugar con número en el mapa.\n"
        "2. Lee la explicación y mira el video o el PDF.\n"
        "3. Contesta la pregunta. Si te equivocas, puedes intentar otra vez.\n"
        "4. Cuando completes los 3 lugares, verás tu resultado final."
    )

    st.markdown("## Acerca del proyecto")
    st.write(ORGANIZACIONES["proyecto"])
    c1, c2 = st.columns(2)
    with c1:
        if os.path.exists(LOGO_EA):
            st.image(LOGO_EA, caption="Logo de Espacios Abiertos", width=160)
        st.markdown("**Espacios Abiertos**")
        st.write(ORGANIZACIONES["ea"])
    with c2:
        if os.path.exists(LOGO_CPI):
            st.image(LOGO_CPI, caption="Logo del Centro de Periodismo Investigativo", width=160)
        st.markdown("**Centro de Periodismo Investigativo**")
        st.write(ORGANIZACIONES["cpi"])

    st.markdown("## Ajustes")
    st.toggle("Letra más grande", key="letra_grande")
    st.toggle("Menos animaciones", key="menos_animacion")

    st.markdown("## Créditos")
    st.caption(
        "Contenido basado en «Derechos. Son tuyos. Defiéndelos.» de Espacios Abiertos y el "
        "Centro de Periodismo Investigativo. Ilustración del mapa creada para este prototipo. "
        "Se usó inteligencia artificial para apoyar la generación del código; el contenido y las "
        "decisiones de diseño fueron revisados por el estudiante. "
        "Esta app no recopila ni guarda datos personales."
    )


# --------------------------------------------------
# Mostrar la pantalla actual
# --------------------------------------------------

{
    "inicio": pantalla_inicio,
    "mapa": pantalla_mapa,
    "aprender": pantalla_aprender,
    "actividad": pantalla_actividad,
    "final": pantalla_final,
    "ayuda": pantalla_ayuda,
}[pantalla]()

st.markdown(
    "<div class='pie'>Prototipo educativo · Arte Digital 1 · UPR Río Piedras</div>",
    unsafe_allow_html=True,
)
