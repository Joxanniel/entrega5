import streamlit as st
# --------------------------------------------------
# Configuración general
# --------------------------------------------------
st.set_page_config(
 page_title="Derecho a tener derechos",
 page_icon="��������",
 layout="wide",
 initial_sidebar_state="collapsed"
)
# --------------------------------------------------
# Contenido
# Este es contenido demostrativo. Luego podemos
# sustituirlo por el contenido exacto autorizado.
# --------------------------------------------------
DERECHOS = [
 { 
 "nombre": "Educación",
 "icono": "������������",
 "color": "#E8F1FF",
 "acento": "#2457A7",
 "resumen": (
 "La educación permite desarrollar conocimientos, participar "
 "en la sociedad y ampliar las posibilidades de vida."
 ),
 "situacion": (
 "Una estudiante deja de asistir a clases porque su escuela "
 "no cuenta con transporte accesible."
 ),
 "pregunta": (
 "¿Qué barreras, además del costo, pueden limitar el acceso "
 "a la educación?"
 ),
 "opciones": [
 "La falta de transporte",
 "La discapacidad sin acomodos",
 "La distancia geográfica",
 "Todas las anteriores"
 ],
 "correcta": "Todas las anteriores"
 },
 { 
 "nombre": "Salud",
 "icono": "����",
 "color": "#FFF0F1",
 "acento": "#A83246",
 "resumen": (
 "El acceso a servicios de salud adecuados influye en la "
 "dignidad, la autonomía y el bienestar de las personas."
 ),
 "situacion": (
 "Una persona espera varios meses para recibir una cita médica "
 "especializada que necesita con urgencia."
 ),
 "pregunta": (
 "¿Todas las personas tienen las mismas condiciones para "
 "recibir atención médica?"
 ),
 "opciones": [
 "Sí, porque los hospitales están abiertos",
 "No, existen barreras económicas y geográficas",
 "Solo depende de la voluntad de la persona",
 "La salud no se relaciona con los derechos"
 ],
 "correcta": "No, existen barreras económicas y geográficas"
 },
 { 
 "nombre": "Vivienda",
 "icono": "�������",
 "color": "#FFF4E6",
 "acento": "#9B5700",
 "resumen": (
 "Una vivienda segura y adecuada es parte de las condiciones "
 "necesarias para vivir con dignidad."
 ),
 "situacion": (
 "Una familia tiene que abandonar su comunidad porque el costo "
 "del alquiler aumentó considerablemente."
 ),
 "pregunta": (
 "¿Cómo puede el desplazamiento afectar los vínculos de una comunidad?"
 ),
 "opciones": [
 "Puede romper redes de apoyo",
 "No produce ningún efecto",
 "Solo cambia la dirección postal",
 "Siempre mejora la vida comunitaria"
 ],
 "correcta": "Puede romper redes de apoyo"
 },
 { 
 "nombre": "Trabajo",
 "icono": "�������",
 "color": "#EDF8F0",
 "acento": "#27653A",
 "resumen": (
 "El derecho al trabajo incluye condiciones justas, seguras "
 "y respetuosas de la dignidad humana."
 ),
 "situacion": (
 "Una empleada trabaja horas adicionales con frecuencia, "
 "pero no recibe compensación."
 ),
 "pregunta": (
 "¿Qué elementos ayudan a reconocer una condición laboral injusta?"
 ),
 "opciones": [
 "Falta de paga",
 "Riesgos de seguridad",
 "Discriminación",
 "Todas las anteriores"
 ],
 "correcta": "Todas las anteriores"
 },
 { 
 "nombre": "Acceso a la información",
 "icono": "���",
 "color": "#F1EEFF",
 "acento": "#584199",
 "resumen": (
 "La información pública permite comprender, cuestionar y "
 "fiscalizar decisiones que afectan a la sociedad."
 ),
 "situacion": (
 "Una comunidad solicita información sobre un proyecto público, "
 "pero la agencia no responde."
 ),
 "pregunta": (
 "¿Por qué el acceso a información pública fortalece la democracia?"
 ),
 "opciones": [
 "Permite fiscalizar decisiones",
 "Evita toda diferencia de opinión",
 "Sustituye la participación ciudadana",
 "Convierte toda información en privada"
 ],
 "correcta": "Permite fiscalizar decisiones"
 } 
]
# --------------------------------------------------
# Estado de la aplicación
# --------------------------------------------------
if "derecho_actual" not in st.session_state:
 st.session_state.derecho_actual = 0
if "completados" not in st.session_state:
 st.session_state.completados = []
if "respuestas" not in st.session_state:
 st.session_state.respuestas = {}
indice = st.session_state.derecho_actual
derecho = DERECHOS[indice]
# --------------------------------------------------
# Estilos visuales
# --------------------------------------------------
st.markdown(
 """
 <style>
 .block-container {
 max-width: 1100px;
 padding-top: 2rem;
 padding-bottom: 4rem;
 } 
 .hero {
 padding: 2.1rem;
 border-radius: 24px;
 background:
 linear-gradient(
 135deg,
 rgba(27, 56, 94, 1) 0%,
 rgba(69, 105, 143, 1) 100%
 );
 color: white;
 margin-bottom: 1.5rem;
 } 
 .hero h1 {
 color: white;
 margin: 0;
 font-size: 3rem;
 line-height: 1.05;
 } 
 .hero p {
 font-size: 1.12rem;
 line-height: 1.55;
 margin-top: 1rem;
 margin-bottom: 0;
 max-width: 760px;
 } 
 .derecho-card {
 border-radius: 22px;
 padding: 2rem;
 margin-top: 1rem;
 margin-bottom: 1.5rem;
 border: 1px solid rgba(30, 40, 50, 0.10);
 box-shadow: 0 8px 24px rgba(20, 35, 50, 0.08);
 } 
 .derecho-icono {
 font-size: 3.1rem;
 margin-bottom: 0.4rem;
 } 
 .derecho-titulo {
 font-size: 2.1rem;
 font-weight: 750;
 margin-bottom: 0.7rem;
 } 
 .derecho-resumen {
 font-size: 1.12rem;
 line-height: 1.65;
 max-width: 800px;
 } 
 .etiqueta {
 text-transform: uppercase;
 letter-spacing: 0.08em;
 font-weight: 700;
 font-size: 0.78rem;
 opacity: 0.76;
 margin-bottom: 0.4rem;
 } 
 .situacion {
 background: #F7F8FA;
 border-left: 6px solid #304D6D;
 border-radius: 10px;
 padding: 1.2rem 1.3rem;
 font-size: 1.05rem;
 line-height: 1.55;
 margin: 1rem 0 1.4rem 0;
 } 
 .pie {
 text-align: center;
 color: #5E6872;
 font-size: 0.88rem;
 margin-top: 3rem;
 } 
 div[data-testid="stButton"] button {
 border-radius: 999px;
 min-height: 3rem;
 font-weight: 650;
 } 
 div[data-testid="stProgress"] > div > div {
 border-radius: 999px;
 } 
 </style>
 """,
 unsafe_allow_html=True
)
# --------------------------------------------------
# Encabezado
# --------------------------------------------------
st.markdown(
 """
 <div class="hero">
 <div style="font-size: 1rem; font-weight: 700; opacity: .86;">
 EXPERIENCIA INTERACTIVA
 </div>
 <h1>Derecho a tener derechos</h1>
 <p>
 Explora situaciones cotidianas, identifica posibles barreras
 y reflexiona sobre cómo los derechos se manifiestan en la vida real.
 </p>
 </div>
 """,
 unsafe_allow_html=True
)
# --------------------------------------------------
# Progreso
# --------------------------------------------------
progreso = (indice + 1) / len(DERECHOS)
col_progreso, col_numero = st.columns([5, 1])
with col_progreso:
 st.progress(progreso)
with col_numero:
 st.markdown(
 f"**{indice + 1} de {len(DERECHOS)}**"
 )
# --------------------------------------------------
# Tarjeta principal
# --------------------------------------------------
st.markdown(
 f"""
 <div
 class="derecho-card"
 style="
 background: {derecho['color']};
 border-top: 8px solid {derecho['acento']};
 "
 >
 <div class="derecho-icono">{derecho['icono']}</div>
 <div
 class="derecho-titulo"
 style="color: {derecho['acento']};"
 >
 {derecho['nombre']}
 </div>
 <div class="derecho-resumen">
 {derecho['resumen']}
 </div>
 </div>
 """,
 unsafe_allow_html=True
)
# --------------------------------------------------
# Situación y selección
# --------------------------------------------------
col_izq, col_der = st.columns([1.1, 0.9], gap="large")
with col_izq:
 st.markdown("### Una situación posible")
 st.markdown(
 f"""
 <div class="situacion">
 {derecho['situacion']}
 </div>
 """,
 unsafe_allow_html=True
 )
 st.markdown("### Pregunta para pensar")
 st.write(derecho["pregunta"])
 seleccion = st.radio(
 "Selecciona una respuesta:",
 derecho["opciones"],
 index=None,
 key=f"quiz_{indice}"
 )
 if st.button(
 "Comprobar respuesta",
 type="primary",
 use_container_width=True
 ):
 if seleccion is None:
 st.warning("Selecciona una opción antes de comprobar.")
 elif seleccion == derecho["correcta"]:
 st.success(
 "La respuesta es adecuada. Ahora considera qué otras "
 "condiciones podrían cambiar el análisis."
 )
 if indice not in st.session_state.completados:
 st.session_state.completados.append(indice)
 else:
 st.error(
 "Esa respuesta deja fuera elementos importantes. "
 "Revisa la situación y prueba otra vez."
 )
with col_der:
 st.markdown("### Tu reflexión")
 respuesta_guardada = st.session_state.respuestas.get(indice, "")
 reflexion = st.text_area(
 "¿Qué cambiarías en esta situación para proteger mejor este derecho?",
 value=respuesta_guardada,
 height=180,
 placeholder=(
 "Puedes mencionar responsabilidades públicas, "
 "barreras estructurales o acciones comunitarias."
 ),
 key=f"reflexion_{indice}"
 )
 if st.button(
 "Guardar reflexión",
 use_container_width=True
 ):
 if reflexion.strip():
 st.session_state.respuestas[indice] = reflexion.strip()
 st.success(
 "La reflexión quedó guardada mientras mantengas abierta esta sesión."
 )
 else:
 st.warning("Escribe una reflexión antes de guardarla.")
 st.caption(
 "Este prototipo no envía ni almacena información en una base de datos."
 )
# --------------------------------------------------
# Navegación
# --------------------------------------------------
st.divider()
anterior, centro, siguiente = st.columns([1, 1.3, 1])
with anterior:
 if st.button(
 "← Derecho anterior",
 disabled=(indice == 0),
 use_container_width=True
 ):
 st.session_state.derecho_actual -= 1
 st.rerun()
with centro:
 completados = len(st.session_state.completados)
 st.markdown(
 f"""
 <div style="text-align:center; padding-top:.65rem;">
 <strong>{completados}</strong> de
 <strong>{len(DERECHOS)}</strong> ejercicios completados
 </div>
 """,
 unsafe_allow_html=True
 )
with siguiente:
 if st.button(
 "Próximo derecho →",
 disabled=(indice == len(DERECHOS) - 1),
 type="primary",
 use_container_width=True
 ):
 st.session_state.derecho_actual += 1
 st.rerun()
# --------------------------------------------------
# Cierre
# --------------------------------------------------
if indice == len(DERECHOS) - 1:
 st.divider()
 st.markdown("## Cierre de la experiencia")
 if len(st.session_state.completados) == len(DERECHOS):
 st.success(
 "Completaste todas las situaciones. "
 "El próximo paso podría ser comparar tus respuestas "
 "con las de otras personas mediante una conversación grupal."
 )
 st.balloons()
 else:
 st.info(
 "Puedes regresar a los derechos anteriores para completar "
 "los ejercicios pendientes."
 )
st.markdown(
 """
 <div class="pie">
 Prototipo educativo para explorar decisiones de UX, UI,
 accesibilidad y arquitectura de información.
 </div>
 """,
 unsafe_allow_html=True
