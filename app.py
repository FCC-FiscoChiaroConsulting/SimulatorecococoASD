import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Simulatore Co.Co.Co Sportivi 2025",
    page_icon="⚽",
    layout="wide"
)

def formatta_euro(valore):
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatta_percentuale(valore, decimali=2):
    return f"{valore:.{decimali}f}%".replace(".", ",")

def calcola_irpef(reddito_imponibile):
    if reddito_imponibile <= 0: return 0
    elif reddito_imponibile <= 28000: return reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000: return 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else: return 28000 * 0.23 + 22000 * 0.35 + (reddito_imponibile - 50000) * 0.43

def calcola_cococo_sportivo(compenso_lordo, tipo_attivita, altra_previdenza=False, 
                            addizionali_reg=0, addizionali_com=0):
    # [LA TUA FUNZIONE IDENTICA - non tocco nulla]
    franchigia_fiscale = min(compenso_lordo, 15000)
    franchigia_contributiva = min(compenso_lordo, 5000)
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50
    if altra_previdenza:
        aliquota_ivs, aliquota_aggiuntiva = 24.0, 2.03
    else:
        aliquota_ivs, aliquota_aggiuntiva = 25.0, 2.03
    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100)
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi
    contributi_lavoratore = totale_contributi_inps * (1/3)
    contributi_societa = totale_contributi_inps * (2/3)
    reddito_imponibile = max(0, compenso_lordo - franchigia_fiscale)
    reddito_imponibile_netto = max(0, reddito_imponibile - contributi_lavoratore)
    irpef = calcola_irpef(reddito_imponibile_netto)
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100)
    totale_imposte = irpef + addizionale_regionale + addizionale_comunale
    totale_trattenute = contributi_lavoratore + totale_imposte
    netto_lavoratore = compenso_lordo - totale_trattenute
    costo_totale_societa = compenso_lordo + contributi_societa
    tax_rate = (totale_trattenute / compenso_lordo) * 100 if compenso_lordo > 0 else 0

    return {
        'compenso_lordo': compenso_lordo, 'franchigia_fiscale': franchigia_fiscale,
        'franchigia_contributiva': franchigia_contributiva, 'base_contrib_grezza': base_contrib_grezza,
        'base_contrib_ridotta': base_contrib_ridotta, 'aliquota_ivs': aliquota_ivs,
        'aliquota_aggiuntiva': aliquota_aggiuntiva, 'contributi_ivs': contributi_ivs,
        'contributi_aggiuntivi': contributi_aggiuntivi, 'totale_contributi': totale_contributi_inps,
        'contributi_lavoratore': contributi_lavoratore, 'contributi_societa': contributi_societa,
        'reddito_imponibile': reddito_imponibile, 'reddito_imponibile_netto': reddito_imponibile_netto,
        'irpef': irpef, 'addizionale_regionale': addizionale_regionale, 'addizionale_comunale': addizionale_comunale,
        'totale_imposte': totale_imposte, 'totale_trattenute': totale_trattenute, 'netto_lavoratore': netto_lavoratore,
        'costo_totale_societa': costo_totale_societa, 'tax_rate': tax_rate
    }

# HEADER (IDENTICO)
st.title("⚽ Simulatore Co.Co.Co Sportivi 2025")
st.markdown("**by Fisco Chiaro Consulting**")

st.info("""
**ℹ️ Collaborazioni Sportive (Co.Co.Co) - Novità 2025:**
- 🎯 **Esenzione fiscale fino a 15.000€** sui compensi da ASD/SSD
- 💰 **Esenzione contributiva fino a 5.000€** sui compensi da ASD/SSD
- 📉 **Dimezzamento 50%** base contributiva su eccedenza (fino 2027)
- ⚖️ **Ripartizione contributi:** 1/3 lavoratore - 2/3 società sportiva
- 🏢 Valido per: istruttori, allenatori, preparatori, collaboratori amministrativi
""")

st.markdown("---")

# LAYOUT (STRUTTURA SEMPLICE COME QUELLO CHE FUNZIONA)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Dati Input")
    
    tipo_attivita = st.selectbox(
        "Tipo di collaborazione",
        ["Istruttore/Allenatore sportivo","Personal trainer","Preparatore atletico",
         "Maestro di sport","Collaboratore amministrativo-gestionale","Altro collaboratore sportivo"],
        key="tipo_attivita"
    )
    
    compenso_lordo = st.number_input(
        "Compenso lordo annuo (€)", min_value=0, max_value=200000, value=18000, step=1000,
        key="compenso_lordo"
    )
    
    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria", key="altra_prev"
    )
    
    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input("Add. Regionale (%)", 0.0, 3.33, 1.23, 0.1, key="add_reg")
    with col_add2:
        addizionale_com = st.number_input("Add. Comunale (%)", 0.0, 0.8, 0.5, 0.1, key="add_com")

with col2:
    st.header("📊 Risultati (Live)")
    
    # ✅ CALCOLO IMMEDIATO - FUNZIONA SEMPRE
    risultato = calcola_cococo_sportivo(compenso_lordo, tipo_attivita, altra_prev, addizionale_reg, addizionale_com)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.metric("Lordo", formatta_euro(risultato['compenso_lordo']))
    with col_b: st.metric("Netto", formatta_euro(risultato['netto_lavoratore']))
    with col_c: st.metric("Costo Società", formatta_euro(risultato['costo_totale_societa']))
    
    st.metric("Tax Rate", formatta_percentuale(risultato['tax_rate']))



