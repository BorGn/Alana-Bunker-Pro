import streamlit as st
from core.functions import detectar_drives

def render():
    with st.sidebar:
        st.title("🛰️ Alana Bunker")
        st.caption("v.20.02 | Unidades Ativas")
        st.divider()
        
        drives = detectar_drives()
        cols = st.columns(len(drives))
        for i, d in enumerate(drives):
            if cols[i].button(d[0], key=f"drive_btn_{d}"):
                st.session_state.dir_atual = d
                st.rerun()
        st.divider()