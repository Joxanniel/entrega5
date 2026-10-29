import streamlit as st
st.title("Derecho a tener derechos")
opcion = st.selectbox(
 "Escoge un derecho",
 ["Educación","Salud","Vivienda"]
)
if opcion == "Educación":
 st.write("Aquí va el resumen.")