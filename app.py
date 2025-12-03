import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Configurazione pagina
st.set_page_config(
    page_title="Simulatore Co.Co.Co Sportivi 2025",
    page_icon="⚽",
    layout="wide"
)

# ============================================================================ #
# MESSAGGIO INIZIALE DI CARICAMENTO
# ============================================================================ #
if "app_loaded" not in st.session_state:
    loading_container = st.empty()

    with loading_container.container():
        st.info("🔄 **Caricamento del simulatore in corso...**")
        st.markdown(
            """
        Stiamo preparando il calcolatore per le collaborazioni sportive.  
        **Attendi circa 20 secondi**, la pagina si aggiornerà automaticamente.
        
        ⏳ *Caricamento delle normative fiscali 2025...*
        """
        )

        progress_bar = st.progress(0)
        for percent in range(100):
            time.sleep(0.2)  # 20 secondi
            progress_bar.progress(percent + 1)

    loading_container.empty()
    st.session_state.app_loaded = True
    st.rerun()


# ============================================================================ #
# FUNZIONI DI FORMATTAZIONE
# ============================================================================ #
def formatta_euro(valore: float) -> str:
    """Formatta un numero in euro con separatori italiani."""
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatta_percentuale(valore: float, decimali: int = 2) -> str:
    """Formatta una percentuale con virgola italiana."""
    return f"{valore:.{decimali}f}%".replace(".", ",")


# ============================================================================ #
# CALCOLO IRPEF
# ============================================================================ #
def calcola_irpef(reddito_imponibile: float) -> float:
    """Calcola IRPEF con scaglioni 2025."""
    if reddito_imponibile <= 0:
        return 0.0
    elif reddito_imponibile <= 28000:
        irpef = reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000:
        irpef = 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else:
        irpef = (
            28000 * 0.23
            + 22000 * 0.35
            + (reddito_imponibile - 50000) * 0.43
        )
    return irpef


# ============================================================================ #
# CALCOLO Co.Co.Co SPORTIVO
# ============================================================================ #
def calcola_cococo_sportivo(
    compenso_lordo: float,
    tipo_attivita: str,
    altra_previdenza: bool = False,
    addizionali_reg: float = 0.0,
    addizionali_com: float = 0.0,
) -> dict:
    """
    Calcola imposte, contributi e costi per co.co.co sportivo.

    Parametri:
    - compenso_lordo: Compenso lordo annuo pattuito
    - tipo_attivita: Tipo di collaborazione sportiva (solo informativo, non incide sul calcolo)
    - altra_previdenza: Se ha già altra pensione/previdenza
    - addizionali_reg: Aliquota addizionale regionale IRPEF
    - addizionali_com: Aliquota addizionale comunale IRPEF
    """

    # ESENZIONI E FRANCHIGIE
    franchigia_fiscale = min(compenso_lordo, 15000)   # Esenzione fiscale 15.000€
    franchigia_contributiva = min(compenso_lordo, 5000)  # Esenzione contributiva 5.000€

    # BASE CONTRIBUTIVA
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50  # dimezzamento fino al 2027

    # Aliquote INPS Gestione Separata 2025
    if altra_previdenza:
        aliquota_ivs = 24.0  # Con altra pensione/previdenza
        aliquota_aggiuntiva = 2.03
    else:
        aliquota_ivs = 25.0  # Senza altra previdenza
        aliquota_aggiuntiva = 2.03

    # Contributi IVS (sul 50% della base)
    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100)

    # Contributi aggiuntivi (sull’eccedenza piena)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100)

    # Totale contributi INPS
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi

    # Ripartizione 1/3 – 2/3
    contributi_lavoratore = totale_contributi_inps * (1 / 3)
    contributi_societa = totale_contributi_inps * (2 / 3)

    # CALCOLO FISCALE
    reddito_imponibile = max(0, compenso_lordo - franchigia_fiscale)
    reddito_imponibile_netto = max(0, reddito_imponibile - contributi_lavoratore)

    # IRPEF + addizionali
    irpef = calcola_irpef(reddito_imponibile_netto)
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100)

    totale_imposte = irpef + addizionale_regionale + addizionale_comunale

    # Totale trattenute lavoratore
    totale_trattenute = contributi_lavoratore + totale_imposte

    # Netto e costo
    netto_lavoratore = compenso_lordo - totale_trattenute
    costo_totale_societa = compenso_lordo + contributi_societa

    tax_rate = (
        (totale_trattenute / compenso_lordo) * 100 if compenso_lordo > 0 else 0
    )

    return {
        "tipo_attivita": tipo_attivita,
        "compenso_lordo": compenso_lordo,
        "franchigia_fiscale": franchigia_fiscale,
        "franchigia_contributiva": franchigia_contributiva,
        "base_contrib_grezza": base_contrib_grezza,
        "base_contrib_ridotta": base_contrib_ridotta,
        "aliquota_ivs": aliquota_ivs,
        "aliquota_aggiuntiva": aliquota_aggiuntiva,
        "contributi_ivs": contributi_ivs,
        "contributi_aggiuntivi": contributi_aggiuntivi,
        "totale_contributi": totale_contributi_inps,
        "contributi_lavoratore": contributi_lavoratore,
        "contributi_societa": contributi_societa,
        "reddito_imponibile": reddito_imponibile,
        "reddito_imponibile_netto": reddito_imponibile_netto,
        "irpef": irpef,
        "addizionale_regionale": addizionale_regionale,
        "addizionale_comunale": addizionale_comunale,
        "totale_imposte": totale_imposte,
        "totale_trattenute": totale_trattenute,
        "netto_lavoratore": netto_lavoratore,
        "costo_totale_societa": costo_totale_societa,
        "tax_rate": tax_rate,
    }


# ============================================================================ #
# HEADER
# ============================================================================ #
st.title("⚽ Simulatore Co.Co.Co Sportivi 2025")
st.markdown("**by Fisco Chiaro Consulting**")

st.info(
    """
**ℹ️ Collaborazioni Sportive (Co.Co.Co) - Novità 2025:**
- 🎯 **Esenzione fiscale fino a 15.000€** sui compensi da ASD/SSD  
- 💰 **Esenzione contributiva fino a 5.000€** sui compensi da ASD/SSD  
- 📉 **Dimezzamento 50%** base contributiva su eccedenza (fino 2027)  
- ⚖️ **Ripartizione contributi:** 1/3 lavoratore - 2/3 società sportiva  
- 🏢 Valido per: istruttori, allenatori, preparatori, collaboratori amministrativi  
"""
)

st.markdown("---")

# ============================================================================ #
# LAYOUT A DUE COLONNE
# ============================================================================ #
col1, col2 = st.columns([1, 1])

# --------------------------- COLONNA SINISTRA - INPUT ----------------------- #
with col1:
    st.header("📝 Dati Input")

    st.subheader("Tipo di collaborazione")
    tipo_attivita = st.selectbox(
        "Seleziona il tipo di attività",
        [
            "Istruttore/Allenatore sportivo",
            "Personal trainer",
            "Preparatore atletico",
            "Maestro di sport",
            "Collaboratore amministrativo-gestionale",
            "Altro collaboratore sportivo",
        ],
        key="tipo_attivita_select",
    )

    st.markdown("---")

    st.subheader("💰 Compenso annuo")
    compenso_lordo = st.number_input(
        "Compenso lordo annuo (€)",
        min_value=0,
        max_value=200000,
        value=18000,
        step=1000,
        key="compenso_lordo_input",
        help="Compenso lordo annuo pattuito con la società sportiva",
    )

    st.markdown("---")

    st.subheader("📊 Situazione previdenziale")
    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria",
        key="altra_prev_check",
        help="Se già pensionato o iscritto ad altra cassa, aliquota INPS ridotta al 24%",
    )

    st.markdown("---")

    st.subheader("🏛️ Addizionali IRPEF (opzionale)")
    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input(
            "Add. Regionale (%)",
            min_value=0.0,
            max_value=3.33,
            value=1.23,
            step=0.1,
            key="addizionale_reg_input",
            help="Varia per regione (es. Puglia 1,23%)",
        )
    with col_add2:
        addizionale_com = st.number_input(
            "Add. Comunale (%)",
            min_value=0.0,
            max_value=0.8,
            value=0.5,
            step=0.1,
            key="addizionale_com_input",
            help="Varia per comune (0-0,8%)",
        )

# --------------------------- COLONNA DESTRA - RISULTATI --------------------- #
with col2:
    st.header("📊 Risultati Simulazione")

    risultato = calcola_cococo_sportivo(
        compenso_lordo,
        tipo_attivita,
        altra_prev,
        addizionale_reg,
        addizionale_com,
    )

    st.subheader("💼 Panoramica")
    st.write(f"**Tipo di attività:** {risultato['tipo_attivita']}")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(
            "Compenso Lordo",
            formatta_euro(risultato["compenso_lordo"]),
            help="Compenso lordo annuo pattuito",
        )
    with col_b:
        st.metric(
            "Netto Lavoratore",
            formatta_euro(risultato["netto_lavoratore"]),
            help="Quanto riceve effettivamente il lavoratore",
        )
    with col_c:
        st.metric(
            "Costo Società",
            formatta_euro(risultato["costo_totale_societa"]),
            help="Costo totale per la società sportiva",
        )

    col_d, col_e = st.columns(2)
    with col_d:
        st.metric(
            "Netto Mensile",
            formatta_euro(risultato["netto_lavoratore"] / 12),
            help="Netto medio mensile lavoratore",
        )
    with col_e:
        st.metric(
            "Tax Rate Effettivo",
            formatta_percentuale(risultato["tax_rate"]),
            help="% trattenute su compenso lordo",
        )

    st.markdown("---")
    st.subheader("💼 Dettaglio Contributi INPS")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")

    if risultato["franchigia_contributiva"] > 0:
        st.success(
            f"✅ **Esenzione contributiva:** -{formatta_euro(risultato['franchigia_contributiva'])} (primi 5.000€)"
        )

    if risultato["base_contrib_grezza"] > 0:
        st.write(f"**Eccedenza:** {formatta_euro(risultato['base_contrib_grezza'])}")
        st.info(
            f"💡 **Dimezzamento 50%:** {formatta_euro(risultato['base_contrib_grezza'])} × 50% = "
            f"{formatta_euro(risultato['base_contrib_ridotta'])} (agevolazione fino 2027)"
        )

    st.write(
        f"**Aliquota IVS:** {formatta_percentuale(risultato['aliquota_ivs'], 0)} (calcolata sul 50%)"
    )
    st.write(f"**Contributi IVS:** {formatta_euro(risultato['contributi_ivs'])}")

    st.write(
        f"**Aliquota aggiuntiva:** {formatta_percentuale(risultato['aliquota_aggiuntiva'])} (maternità, malattia, ecc.)"
    )
    st.write(
        f"**Contributi aggiuntivi:** {formatta_euro(risultato['contributi_aggiuntivi'])}"
    )

    st.markdown("---")
    st.write(
        f"**Totale contributi INPS:** {formatta_euro(risultato['totale_contributi'])}"
    )

    st.markdown("---")
    st.subheader("⚖️ Ripartizione Contributi")

    col_ris1, col_ris2 = st.columns(2)
    with col_ris1:
        st.metric(
            "Quota Lavoratore (1/3)",
            formatta_euro(risultato["contributi_lavoratore"]),
            help="Contributi a carico del lavoratore",
        )
    with col_ris2:
        st.metric(
            "Quota Società (2/3)",
            formatta_euro(risultato["contributi_societa"]),
            help="Contributi a carico della società sportiva",
        )

    st.markdown("---")
    st.subheader("🧮 Dettaglio Fiscale (IRPEF)")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")

    if risultato["franchigia_fiscale"] > 0:
        st.success(
            f"✅ **Esenzione fiscale:** -{formatta_euro(risultato['franchigia_fiscale'])} (primi 15.000€ da ASD/SSD)"
        )

    st.write(f"**Reddito imponibile:** {formatta_euro(risultato['reddito_imponibile'])}")
    st.write(
        f"**Contributi deducibili:** -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(
        f"**Reddito imponibile netto:** {formatta_euro(risultato['reddito_imponibile_netto'])}"
    )
