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

def lista_items(flt_):
    mydb = get_database_connection()
    myc = mydb.cursor()
    SQL = "CALL `App_Consulta_Presupuestos_Items`(%s);"
    myc.execute(SQL,(flt_,))
    results = myc.fetchall()
    myc.close()
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
                e = row[0]  
            else:
                e = "0" 
            temp_color = "green" if row[6] == {'0'} else "none"

            st.markdown(f'<div style="float: left; margin-top: 10px; color:{temp_color};"> Fecha: {row[4]} </div> <div style="float: right; margin-top: 10px;color:{temp_color};">Hora: {row[8]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="float: left; color:{temp_color}; margin-top: 0px;"> Cliente: {row[2]} </div>', unsafe_allow_html=True)
            st.markdown(f'<div style="float: left; color:{temp_color}; margin-top: 0px;"> Vendedor: {row[3]} </div>', unsafe_allow_html=True)
            if row[7] !='':
                st.markdown(f'<div style="float: left; color:{temp_color}; margin-top: 0px;"> Observación: {row[7]} </div>', unsafe_allow_html=True)
            
            valor_f ="Total Pres.: " + "{:,} Gs".format(int(row[5])).replace(",", ".")     
            st.markdown(f'<div style="float: right;color:{temp_color}; margin-top: 0px;margin-bottom: -10px;margin-right: 10px;">{valor_f}</div>', unsafe_allow_html=True)
           
            if e != "0":
                 with st.form(key='my_form'):
                    st.markdown(f'<div style="float: center;color:{temp_color}; margin-top: 5px;margin-bottom: -30px;">Items Presupuesto Nº: {row[0]}</div>', unsafe_allow_html=True)
                    st.markdown('<hr class="linha-cinza"; margin-top: 5px;margin-bottom: -30px;>', unsafe_allow_html=True),
                    rst = lista_items(e)
                    total = 0
                    for row in rst:                
                        id_format = (f'ID: {row[0]}')
                        codigo_format = (f'CODIGO: {row[1]}')

                        st.markdown(f'<div style="float: left;color:{temp_color};">{id_format}</div> <div style="float: right;color:{temp_color};">{codigo_format}</div>', unsafe_allow_html=True)

                        descripcion_format = (f'{row[2]}')
                        st.markdown(f'<div style="float: left;color:{temp_color};">{descripcion_format}</div>', unsafe_allow_html=True)
                        ctd_formatted = "<span>Cantidad: {:,} Und</span>".format(int(row[3])).replace(",", ".")
                        pc_formatted = "Precio: " + "{:,} Gs".format(int(row[4])).replace(",", ".")
                        tl_formatted ="Total: " + "{:,} Gs".format(int(row[5])).replace(",", ".")  
                        st.markdown(f'<div style="display: inline-block; float: left; margin: 0 auto; color:{temp_color};">{ctd_formatted}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="display: inline-block; float: left; margin-right: 40px; color:{temp_color};">{pc_formatted}</div> <div style="display: inline-block; float: right; color:{temp_color};">{tl_formatted}</div>', unsafe_allow_html=True)
                        total +=  row[5]    
                        st.markdown('---')

                    total_formatted = "Total: " + "{:,} Gs".format(int(total)).replace(",", ".")
                    st.markdown(f'<div style="float: right;color:{temp_color};">{total_formatted}</div>', unsafe_allow_html=True)
                    if st.form_submit_button('Volver ↑','Click Para Ocultar Detalles'):
                        d = "0"
                    
            st.markdown("<style> .linha-presupuesto {border: 0.1px solid burlywood;margin: 20px 0;}</style>",unsafe_allow_html=True)
            st.markdown('<hr class="linha-presupuesto">', unsafe_allow_html=True)

    else:
        st.warning("Nenhum resultado encontrado.")