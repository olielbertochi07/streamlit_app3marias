
import streamlit as st

def main():
    st.button("teste")

    #if 'logged_in' not in st.session_state:
    #    st.session_state['logged_in'] = False
    #if st.session_state['logged_in']:
    #    Filtrar()
    #else:
    #    login_page()
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