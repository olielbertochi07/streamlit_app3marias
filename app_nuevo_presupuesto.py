import streamlit as st
from db_functions import get_database_connection

def get_lista(filtro_):  
    mydb = get_database_connection()
    mycursor = mydb.cursor()
    SQL = "CALL `App_Consulta_Presupuestos`(%s);"
    mycursor.execute(SQL, (filtro_,))
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results

def Nuevo_Presupuesto():
    st.subheader("Lista de Presupuesto")
  
    btn_gravar = st.button("Gravar", key="btn_nuevo")

    st.markdown('<hr class="linha-cinza">', unsafe_allow_html=True)
    st.markdown("<style> .linha-cinza {margin: 0px 0;}</style>",unsafe_allow_html=True)


    st.markdown('<div class="dado">teste</div>',unsafe_allow_html=True)


    
    st.markdown("<style> .dado {color: red; margin: 0px 0;}</style>",unsafe_allow_html=True)

   
   

    st.markdown('<hr class="linha-cinza">', unsafe_allow_html=True) 
   
