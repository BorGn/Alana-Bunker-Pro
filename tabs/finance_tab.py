import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

DB_PATH = "C:/Alana/docs/finance_settings.json"

def carregar_dados():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r") as f:
                data = json.load(f)
                data["data_inv"] = datetime.strptime(data["data_inv"], "%Y-%m-%d").date()
                return data
        except: pass
    return {"cap_total": 50000.0, "no_cofre": 45000.0, "data_inv": datetime.now().date() - timedelta(days=30), "cdi": 11.15, "modo": "Anual"}

def render():
    st.header("💰 Gestão Meli+ (Conversão Visual)")
    dados = carregar_dados()
    
    visao = st.radio("Foco da Análise", ["Apenas Cofrinho", "Conta + Cofrinho"], horizontal=True, key="v_switch")

    with st.expander("⚙️ Parâmetros de Mercado", expanded=True):
        col1, col2 = st.columns(2)
        total = col1.number_input("Saldo Total (R$)", value=float(dados.get("cap_total", 50000.0)), key="f_t")
        cofre = col2.number_input("No Cofrinho (R$)", value=float(dados.get("no_cofre", 45000.0)), key="f_c")
        
        modo = st.radio("Modo de Entrada", ["Anual", "Mensal"], index=0 if dados.get("modo") == "Anual" else 1, horizontal=True, key="f_m")
        val_cdi = st.number_input(f"Digite o CDI {modo} (%)", value=float(dados.get("cdi", 11.15)), format="%.4f", key="f_i")
        
        # --- BLOCO DE CONVERSÃO VISUAL ---
        if modo == "Anual":
            equiv = ((1 + (val_cdi/100))**(1/12) - 1) * 100
            st.info(f"📊 **{val_cdi:.2f}% ao ano** equivale a **{equiv:.4f}% ao mês**.")
        else:
            equiv = ((1 + (val_cdi/100))**12 - 1) * 100
            st.info(f"📊 **{val_cdi:.4f}% ao mês** equivale a **{equiv:.2f}% ao ano**.")

        data_ini = st.date_input("Data Inicial", value=dados["data_inv"], key="f_d")

        if st.button("💾 Salvar Parâmetros", key="f_s"):
            if val_cdi > 40: 
                st.error("⚠️ Taxa improvável. Digite o CDI Bruto.")
            else:
                with open(DB_PATH, "w") as f:
                    json.dump({"cap_total": total, "no_cofre": cofre, "data_inv": str(data_ini), "cdi": val_cdi, "modo": modo}, f)
                st.rerun()

    # Cálculo
    cdi_a = val_cdi/100 if modo == "Anual" else ((1 + (val_cdi/100))**12) - 1
    t120 = (1 + (cdi_a * 1.20))**(1/252) - 1
    t105 = (1 + (cdi_a * 1.05))**(1/252) - 1

    dias = pd.date_range(start=data_ini, end=datetime.now().date(), freq='B')
    
    if len(dias) > 0:
        l_tot, l_cof, s_t, s_c = [], [], total, cofre
        for _ in dias:
            r_cof = (min(s_c, 50000.0) * t120) + (max(0, s_c - 50000.0) * t105)
            r_cnt = (s_t - s_c) * t105
            s_t += r_cof + r_cnt
            s_c += r_cof
            l_tot.append(s_t)
            l_cof.append(s_c)

        st.divider()
        c_a, c_b = st.columns(2)
        if visao == "Apenas Cofrinho":
            c_a.metric("Saldo Cofrinho", f"R$ {l_cof[-1]:,.2f}")
            c_b.metric("Rendimento (120%)", f"R$ {l_cof[-1] - cofre:,.2f}")
            st.area_chart(pd.DataFrame({"Cofrinho": l_cof}, index=dias))
        else:
            c_a.metric("Saldo Consolidado", f"R$ {l_tot[-1]:,.2f}")
            c_b.metric("Rendimento Total", f"R$ {l_tot[-1] - total:,.2f}")
            st.line_chart(pd.DataFrame({"Total": l_tot, "Cofrinho": l_cof}, index=dias))
