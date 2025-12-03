import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Configurazione pagina
st.set_page_config(
    page_title="Simulatore Co.Co.Co Lavoratori Sportivi 2025",
    page_icon="⚽",
    layout="wide"
)

# =====================================================================
# FUNZIONI DI UTILITÀ
# =====================================================================
def formatta_euro(valore):
    """Formatta un numero in euro con separatori italiani"""
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatta_percentuale(valore, decimali=2):
    """Formatta una percentuale con virgola italiana"""
    return f"{valore:.{decimali}f}%".replace(".", ",")

def calcola_irpef(reddito_imponibile):
    """Calcola IRPEF con scaglioni 2025"""
    if reddito_imponibile <= 0:
        return 0.0
    elif reddito_imponibile <= 28_000:
        return reddito_imponibile * 0.23
    elif reddito_imponibile <= 50_000:
        return 28_000 * 0.23 + (reddito_imponibile - 28_000) * 0.35
    else:
        return (
            28_000 * 0.23
            + 22_000 * 0.35
            + (reddito_imponibile - 50_000) * 0.43
        )

def calcola_cococo_sportivo(compenso_lordo,
                            altra_previdenza=False,
                            addizionali_reg=0.0,
                            addizionali_com=0.0):
    """
    Calcola imposte, contributi e costi per collaboratore sportivo in Co.Co.Co.

    Ipotesi:
    - Compenso interamente da ASD/SSD
    - Esenzione fiscale 15.000 €
    - Esenzione contributiva 5.000 €
    - Dimezzamento base contributiva eccedenza (50%) fino al 2027
    - Ripartizione contributi: 1/3 lavoratore, 2/3 società
    """

    # FRANCHIGIE
    franchigia_fiscale = min(compenso_lordo, 15_000)
    franchigia_contributiva = min(compenso_lordo, 5_000)

    # BASE CONTRIBUTIVA
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50  # agevolazione 50%

    # ALIQUOTE INPS GESTIONE SEPARATA
    if altra_previdenza:
        aliquota_ivs = 24.0
    else:
        aliquota_ivs = 25.0
    aliquota_aggiuntiva = 2.03  # maternità, malattia, ANF, DIS-COLL

    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100)
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi

    contributi_lavoratore = totale_contributi_inps / 3
    contributi_societa = totale_contributi_inps * 2 / 3

    # BASE FISCALE
    reddito_imponibile = max(0, compenso_lordo - franchigia_fiscale)
    reddito_imponibile_netto = max(0, reddito_imponibile - contributi_lavoratore)

    # IMPOSTE
    irpef = calcola_irpef(reddito_imponibile_netto)
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100)
    totale_imposte = irpef + addizionale_regionale + addizionale_comunale

    # TOTALE TRATTENUTE E RISULTATI
    totale_trattenute_lavoratore = contributi_lavoratore + totale_imposte
    netto_lavoratore = compenso_lordo - totale_trattenute_lavoratore
    costo_totale_societa = compenso_lordo + contributi_societa

    tax_rate = (totale_trattenute_lavoratore / compenso_lordo * 100) if compenso_lordo > 0 else 0

    return {
        'compenso_lordo': compenso_lordo,
        'franchigia_fiscale': franchigia_fiscale,
        'franchigia_contributiva': franchigia_contributiva,
        'base_contrib_grezza': base_contrib_grezza,
        'base_contrib_ridotta': base_contrib_ridotta,
        'aliquota_ivs': aliquota_ivs,
        'aliquota_aggiuntiva': aliquota_aggiuntiva,
        'contributi_ivs': contributi_ivs,
        'contributi_aggiuntivi': contributi_aggiuntivi,
        'totale_contributi': totale_contributi_inps,
        'contributi_lavoratore': contributi_lavoratore,
        'contributi_societa': contributi_societa,
        'reddito_imponibile': reddito_imponibile,
        'reddito_imponibile_netto': reddito_imponibile_netto,
        'irpef': irpef,
        'addizionale_regionale': addizionale_regionale,
        'addizionale_comunale': addizionale_comunale,
        'totale_imposte': totale_imposte,
        'totale_trattenute_lavoratore': totale_trattenute_lavoratore,
        'netto_lavoratore': netto_lavoratore,
        'costo_totale_societa': costo_totale_societa,
        'tax_rate': tax_rate
    }

# =====================================================================
# HEADER CON LOGO
# =====================================================================
try:
    logo = Image.open("FCC-LOGO.jpg")
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(logo, width=150)
    with col_title:
        st.title("⚽ Simulatore Co.Co.Co")
        st.title("Collaboratori Sportivi 2025")
        st.markdown("**by Fisco Chiaro Consulting**")
except:
    st.title("⚽ Simulatore Co.Co.Co")
    st.title("Collaboratori Sportivi 2025")
    st.markdown("**by Fisco Chiaro Consulting**")

st.info("""
**ℹ️ Collaborazioni Sportive (Co.Co.Co) – Riforma dello Sport (D.Lgs. 36/2021)**

- 🎯 Esenzione fiscale fino a **15.000€** sui compensi da
