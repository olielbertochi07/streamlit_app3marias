import streamlit as st
from db_functions import check_login
from app_functions import Filtrar, login_page
from app_lista_presupuestos import Filtrar_Presupuesto
from app_nuevo_presupuesto import *
opcoes = ["Lista de Stock", "Presupuesto","Nuevo Presupuesto"]


def main():

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if st.session_state['logged_in']:

        choice = st.sidebar.selectbox("Seleccionar Menu", opcoes)
        st.sidebar.subheader("________________________________")

        if choice == "Lista de Stock":
            Filtrar()
        if choice == "Presupuesto":
            Filtrar_Presupuesto()
        if choice == "Nuevo Presupuesto":
            Nuevo_Presupuesto()
    else:
        login_page()

if __name__ == "__main__":
    st.set_page_config( 
        page_title="Bertochi Sistemas",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    main()