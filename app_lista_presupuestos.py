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

def Filtrar_Presupuesto():
    st.subheader("Lista de Presupuesto")
    st.subheader("")

    filtro_descricao = st.sidebar.text_input("Buscar Presupuesto", placeholder="Nº Pres. Cliente o Vendedor ...", key="filtro_descricao")
    
    st.sidebar.empty()

    results = get_lista(f'%{filtro_descricao}%')
    if results:
        for row in results:
            button_clicked = st.button(f"Detalles Presupuesto Nº: {row[0]}")
            if button_clicked:   
                e = "1"  
            else:
                e = "0" 
            temp_color = "green" if row[6] == {'0'} else "none"
            st.markdown(f'<div style="color:{temp_color};"> FECHA: {row[4]} </div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:{temp_color}; margin-top: 5px;"> CLIENTE: {row[2]} </div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:{temp_color}; margin-top: 5px;"> VENDEDOR: {row[3]} </div>', unsafe_allow_html=True)
            valor_f ="VALOR: " + "{:,} Gs".format(int(row[5])).replace(",", ".")     
            st.markdown(f'<div style="float: right;color:{temp_color}; margin-top: 20px;margin-bottom: -20px;margin-right: 10px;">{valor_f}</div>', unsafe_allow_html=True)
            if e=="1":
                 with st.form(key='my_form'):
                    st.markdown(f'<div style="float: center;color:{temp_color}; margin-top: 5px;margin-bottom: -30px;">Detalles Presupuesto Nº: {row[0]}</div>', unsafe_allow_html=True)
                    st.markdown('<hr class="linha-cinza"; margin-top: 5px;margin-bottom: -30px;>', unsafe_allow_html=True)
                    st.text('ID     DESCRIPCION   CANT.  PRECIO   TOTAL')
                    st.text('01     PRODUTO 01      5    10.000  50.000')
                    st.text('05     PRODUTO 05      1   125.000 125.000')
                    st.markdown('<hr class="linha-cinza">', unsafe_allow_html=True) 
                    st.text('TOTAL: 175.000')
                    if st.form_submit_button(' ↑ '):
                        e = "0"
            st.markdown("<style> .linha-presupuesto {border: 0.1px solid burlywood;margin: 20px 0;}</style>",unsafe_allow_html=True)
            st.markdown('<hr class="linha-presupuesto">', unsafe_allow_html=True)

    else:
        st.warning("Nenhum resultado encontrado.")