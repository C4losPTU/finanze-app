import streamlit as st
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
import numpy as np

FILE_CSV = "transazioni.csv"

# ⭐ LE TUE FUNZIONI ORIGINALI (non tocco nulla!)
def aggiungi_entrata(descrizione, importo):
    transazione = {
        "tipo": "entrata",
        "desc": descrizione,
        "importo": importo,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.success(f"✅ Aggiunta entrata: {descrizione} - €{importo:.2f}")
    return transazione

def aggiungi_uscita(descrizione, importo):
    transazione = {
        "tipo": "uscita", 
        "desc": descrizione,
        "importo": importo,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.success(f"✅ Aggiunta uscita: {descrizione} - €{importo:.2f}")
    return transazione

def calcola_bilancio(transazioni):
    entrate = 0
    uscite = 0
    for t in transazioni:
        if t["tipo"] == "entrata":
            entrate += t["importo"]
        else:
            uscite += t["importo"]
    bilancio = entrate - uscite
    return entrate, uscite, bilancio

def formatta_bilancio(entrate, uscite, bilancio):
    testo = f"## 💰 BILANCIO MENSILE\n"
    testo += f"**Entrate totali:** €{entrate:.2f}\n"
    testo += f"**Uscite totali:** €{uscite:.2f}\n"
    testo += f"**Bilancio:** €{bilancio:.2f}\n"
    if bilancio >= 0:
        testo += "🎉 **IN GUADAGNO!**"
    else:
        testo += "⚠️ **IN ROSSO!**"
    return testo

def genera_lista_transazioni(transazioni):
    if not transazioni:
        return "Nessuna transazione registrata."
    testo = "### 📋 LISTA TRANSAZIONI"
    for t in transazioni:
        riga = f"**{t['tipo'].upper()}**: {t['desc']} - €{t['importo']:.2f} [{t['data']}]"
        testo += f"\n• {riga}"
    return testo

def salva_transazioni_csv(transazioni):
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tipo", "desc", "importo", "data"])
        for t in transazioni:
            writer.writerow([t["tipo"], t["desc"], t["importo"], t["data"]])

def carica_transazioni_csv():
    transazioni_caricate = []
    if os.path.exists(FILE_CSV):
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transazioni_caricate.append({
                    "tipo": row["tipo"],
                    "desc": row["desc"], 
                    "importo": float(row["importo"]),
                    "data": row["data"]
                })
    return transazioni_caricate

# 🌐 STREAMLIT INTERFACE (converte il tuo Gradio)
st.set_page_config(page_title="Finanze", layout="wide")
st.title("💰 Il tuo bilancio personale")

# 📊 Session state (come il tuo transazioni[])
if 'transazioni' not in st.session_state:
    st.session_state.transazioni = carica_transazioni_csv()

# 🎛️ INTERFACCIA (stesso tuo Gradio ma Streamlit)
col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Nuova transazione")
    tipo = st.radio("Tipo:", ["entrata", "uscita"], horizontal=True)
    descrizione = st.text_input("Descrizione:", placeholder="Es: Stipendio, Supermercato")
    importo = st.number_input("Importo (€):", min_value=0.01, step=10.0, format="%.2f")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ AGGIUNGI", type="primary"):
            if descrizione and importo > 0:
                if tipo == "entrata":
                    st.session_state.transazioni.append(aggiungi_entrata(descrizione, importo))
                else:
                    st.session_state.transazioni.append(aggiungi_uscita(descrizione, importo))
                salva_transazioni_csv(st.session_state.transazioni)
                st.rerun()
            else:
                st.error("❌ Descrizione e importo > 0!")
    
    with col_btn2:
        if st.button("🔄 RESET TUTTO"):
            st.session_state.transazioni = []
            salva_transazioni_csv([])
            st.rerun()

with col2:
    # 📈 GRAFICO (la tua funzione!)
    entrate, uscite, bilancio = calcola_bilancio(st.session_state.transazioni)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(["💚 Entrate", "❤️ Uscite"], [entrate, uscite], color=["green", "red"])
    ax.set_title("Il tuo bilancio mensile", fontsize=16)
    ax.set_ylabel("€", fontsize=14)
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

# 📋 METRICS + LISTA
col_met1, col_met2, col_met3 = st.columns(3)
col_met1.metric("💰 Entrate", f"€{entrate:.2f}")
col_met2.metric("💸 Uscite", f"€{uscite:.2f}") 
col_met3.metric("🎯 Bilancio", f"€{bilancio:.2f}", delta_color="normal")

st.markdown(formatta_bilancio(entrate, uscite, bilancio))
st.markdown(genera_lista_transazioni(st.session_state.transazioni))

# 🔧 DEBUG
with st.expander("🐛 Debug - Dati raw"):
    st.write(st.session_state.transazioni)
