import mysql.connector
import streamlit as st
from decouple import config
from hashlib import *
DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_PORT = config('DB_PORT')
DB_DATABASE = config('DB_DATABASE')
def check_login(username, password):
    sql = "CALL `App_Consulta_Sessao`(%s, %s)"
    mycursor.execute(sql, (username, password))
    result = mycursor.fetchone()
    return result
mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    database=DB_DATABASE)
mycursor = mydb.cursor()

def Filtrar():
    st.subheader("Lista de Productos")
    st.subheader("")
    filtro_id = st.sidebar.text_input("Cód. Int.", key="filtro_id")
    filtro_codigo = st.sidebar.text_input("Código", key="filtro_codigo")
    filtro_descricao = st.sidebar.text_input("Descripción", key="filtro_descricao")
    if filtro_id == "":
        filtro_id = '%'
    sql = "CALL `App_Consulta_Stock`(%s, %s, %s, '100')"
    mycursor.execute(sql, (filtro_id, f'%{filtro_codigo}%', f'%{filtro_descricao}%'))
    results = mycursor.fetchall()
    formatted_results = [{"Id": row[0], "Codigo": row[1], "Descripcion": row[2], "Stock": row[3], "Min": row[4], "Mayorista": row[5], "Venta": row[6]} for row in results]
    for idx, row in enumerate(formatted_results):
        if idx > 0:
            st.write('---')
        left_column, right_column = st.columns([1, 3])
        with left_column:
            id_format = (f'ID: {row["Id"]}')
            codigo_format = (f'{row["Codigo"]}')
            st.markdown(f'<div style="float: left;">{id_format}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="float: left;">{codigo_format}</div>', unsafe_allow_html=True)     
            descripcion_format = (f'{row["Descripcion"]}')
            st.markdown(f'<div style="text-align; font-weight: bold;">{descripcion_format}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align; font-weight: bold;">' '</div>', unsafe_allow_html=True) 
            if row['Stock'] <= row['Min']:
                stock_formatted = "<span style='color: red;'>Stock: {:,} UN</span>".format(int(row['Stock'])).replace(",", ".")
            else:
                stock_formatted = "<span style='color: green;'>Stock: {:,} UN</span>".format(int(row['Stock'])).replace(",", ".")
            st.markdown(f'{stock_formatted}', unsafe_allow_html=True)
        with right_column:
            may_formatted = "Mayorista: " + "{:,} Gs".format(int(row['Mayorista'])).replace(",", ".")
            vent_formatted ="Venta: " + "{:,} Gs".format(int(row['Venta'])).replace(",", ".")     
            st.markdown(f'<div style="float: left;">{may_formatted}</div><div style="float: right;">{vent_formatted}</div>', unsafe_allow_html=True)       
def login_page():
    st.title("Bertochi Sistemas")
    username = st.text_input("",placeholder="Informe el Usuario", key="user-input")
    password = st.text_input("",placeholder="Informe la Contraseña", type="password")
    if st.button("Iniciar Sessão"):
        if check_login(username.upper, password.upper):
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("Login falhou. Verifique suas credenciais.")
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if st.session_state['logged_in']:
        Filtrar()
    else:
        login_page()
if __name__ == "__main__":
    st.set_page_config( 
        page_title="Bertochi Sistemas",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

    main()