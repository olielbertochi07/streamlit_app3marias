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
            st.markdown(f'<div style="color:{temp_color};"> FECHA: {row[4]} </div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:{temp_color}; margin-top: 5px;"> CLIENTE: {row[2]} </div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:{temp_color}; margin-top: 5px;"> VENDEDOR: {row[3]} </div>', unsafe_allow_html=True)
            valor_f ="TOTAL PRES.: " + "{:,} Gs".format(int(row[5])).replace(",", ".")     
            st.markdown(f'<div style="float: right;color:{temp_color}; margin-top: 20px;margin-bottom: -20px;margin-right: 10px;">{valor_f}</div>', unsafe_allow_html=True)
            if e != "0":
                 with st.form(key='my_form'):
                    st.markdown(f'<div style="float: center;color:{temp_color}; margin-top: 5px;margin-bottom: -30px;">Items Presupuesto Nº: {row[0]}</div>', unsafe_allow_html=True)
                    st.markdown('<hr class="linha-cinza"; margin-top: 5px;margin-bottom: -30px;>', unsafe_allow_html=True),
                    rst = lista_items(e)
                    total = 0
                    for row in rst:                
                        left_column, right_column = st.columns([2, 1])
                        with left_column:
                            id_format = (f'ID: {row[0]}')
                            codigo_format = (f'{row[1]}')
                            st.markdown(f'<div style="float: left;color:{temp_color};">{id_format}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="float: left;color:{temp_color};">{codigo_format}</div>', unsafe_allow_html=True)     
                            descripcion_format = (f'{row[2]}')
                            st.markdown(f'<div style="float: left;color:{temp_color};">{descripcion_format}</div>', unsafe_allow_html=True)
                    
                        with right_column:
                            ctd_formatted = "<span>Cant: {:,} </span>".format(int(row[3])).replace(",", ".")
                            pc_formatted = "Precio: " + "{:,} Gs".format(int(row[4])).replace(",", ".")
                            tl_formatted ="Total: " + "{:,} Gs".format(int(row[5])).replace(",", ".")  

                            st.markdown(f'<div style="display: inline-block; float: left; margin-right: 40px; color:{temp_color};">{ctd_formatted}</div> <div style="display: inline-block;margin-right: 50px; text-align: center; color:{temp_color};">{pc_formatted}</div> <div style="display: inline-block; float: right; color:{temp_color};">{tl_formatted}</div>', unsafe_allow_html=True)

                            total +=  row[5]
                        st.markdown('<hr class="linha-cinza";color:{temp_color}; margin-top: -100px;margin-bottom: -30px;>', unsafe_allow_html=True) 
                    total_formatted = "Total: " + "{:,} Gs".format(int(total)).replace(",", ".")
                    st.markdown(f'<div style="float: right;color:{temp_color};">{total_formatted}</div>', unsafe_allow_html=True)
                    if st.form_submit_button('↑'):
                        d = "0"
                    
            st.markdown("<style> .linha-presupuesto {border: 0.1px solid burlywood;margin: 20px 0;}</style>",unsafe_allow_html=True)
            st.markdown('<hr class="linha-presupuesto">', unsafe_allow_html=True)

    else:
        st.warning("Nenhum resultado encontrado.")