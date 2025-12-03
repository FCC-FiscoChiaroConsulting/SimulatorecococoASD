import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Simulatore Co.Co.Co Sportivi 2025",
    page_icon="⚽",
    layout="wide"
)

# ------------------------------------------------------------
# FUNZIONI DI FORMATTAZIONE
# ------------------------------------------------------------
def formatta_euro(valore: float) -> str:
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatta_percentuale(valore: float, decimali: int = 2) -> str:
    return f"{valore:.{decimali}f}%".replace(".", ",")

# ------------------------------------------------------------
# CALCOLO IRPEF
# ------------------------------------------------------------
def calcola_irpef(reddito_imponibile: float) -> float:
    if reddito_imponibile <= 0:
        return 0.0
    elif reddito_imponibile <= 28000:
        return reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000:
        return 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else:
        return 28000 * 0.23 + 22000 * 0.35 + (reddito_imponibile - 50000) * 0.43

# ------------------------------------------------------------
# CALCOLO Co.Co.Co SPORTIVO
# ------------------------------------------------------------
def calcola_cococo_sportivo(
    compenso_lordo: float,
    tipo_attivita: str,
    altra_previdenza: bool = False,
    addizionali_reg: float = 0.0,
    addizionali_com: float = 0.0,
) -> dict:

    # Esenzioni
    franchigia_fiscale = min(compenso_lordo, 15000)      # esenzione fiscale 15.000 €
    franchigia_contributiva = min(compenso_lordo, 5000)  # esenzione contributiva 5.000 €

    # Base contributiva
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50    # dimezzamento fino al 2027

    # Aliquote INPS
    if altra_previdenza:
        aliquota_ivs = 24.0
    else:
        aliquota_ivs = 25.0
    aliquota_aggiuntiva = 2.03

    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100)
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi

    contributi_lavoratore = totale_contributi_inps / 3
    contributi_societa = totale_contributi_inps * 2 / 3

    reddito_imponibile = max(0, compenso_lordo - franchigia_fiscale)
    reddito_imponibile_netto = max(0, reddito_imponibile - contributi_lavoratore)

    irpef = calcola_irpef(reddito_imponibile_netto)
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100)
    totale_imposte = irpef + addizionale_regionale + addizionale_comunale

    totale_trattenute = contributi_lavoratore + totale_imposte
    netto_lavoratore = compenso_lordo - totale_trattenute
    costo_totale_societa = compenso_lordo + contributi_societa

    tax_rate = (totale_trattenute / compenso_lordo * 100) if compenso_lordo > 0 else 0

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

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.title("⚽ Simulatore Co.Co.Co Sportivi 2025")
st.markdown("**by Fisco Chiaro Consulting**")
st.markdown("---")

# ------------------------------------------------------------
# LAYOUT A DUE COLONNE
# ------------------------------------------------------------
col1, col2 = st.columns([1, 1])

# ========================= COLONNA SINISTRA (INPUT) =========================
with col1:
    st.header("📝 Dati Input")

    tipo_attivita = st.radio(
        "Categoria di collaborazione",
        ["Collaboratore sportivo", "Collaboratore amministrativo-gestionale"],
    )

    compenso_lordo = st.number_input(
        "Compenso lordo annuo (€)",
        min_value=0,
        max_value=200000,
        value=18000,
        step=1000,
        help="Inserisci il compenso lordo annuo pattuito",
    )

    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria",
        help="Se già pensionato o iscritto ad altra cassa, aliquota INPS ridotta al 24%",
    )

    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input(
            "Addizionale regionale (%)",
            min_value=0.0,
            max_value=3.33,
            value=1.23,
            step=0.1,
        )
    with col_add2:
        addizionale_com = st.number_input(
            "Addizionale comunale (%)",
            min_value=0.0,
            max_value=0.8,
            value=0.5,
            step=0.1,
        )

# ========================= COLONNA DESTRA (RISULTATI) =======================
with col2:
    st.header("📊 Risultati")

    # QUI VEDI SUBITO SE L'INPUT CAMBIA
    st.caption(f"Compenso lordo usato nel calcolo: **{compenso_lordo} €**")

    risultato = calcola_cococo_sportivo(
        compenso_lordo,
        tipo_attivita,
        altra_prev,
        addizionale_reg,
        addizionale_com,
    )

    st.subheader("💼 Panoramica")
    st.write(f"**Categoria:** {risultato['tipo_attivita']}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Compenso Lordo", formatta_euro(risultato["compenso_lordo"]))
    with c2:
        st.metric("Netto Lavoratore", formatta_euro(risultato["netto_lavoratore"]))
    with c3:
        st.metric("Costo Società", formatta_euro(risultato["costo_totale_societa"]))

    c4, c5 = st.columns(2)
    with c4:
        st.metric("Netto Mensile", formatta_euro(risultato["netto_lavoratore"] / 12))
    with c5:
        st.metric("Tax rate effettivo", formatta_percentuale(risultato["tax_rate"]))

    st.markdown("---")
    st.subheader("💼 Dettaglio contributi INPS")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")
    st.write(
        f"**Esenzione contributiva (5.000€):** -{formatta_euro(risultato['franchigia_contributiva'])}"
    )
    st.write(f"**Eccedenza contributiva:** {formatta_euro(risultato['base_contrib_grezza'])}")
    st.write(
        f"**Base contributiva dimezzata (50%):** {formatta_euro(risultato['base_contrib_ridotta'])}"
    )
    st.write(
        f"**Contributi IVS ({formatta_percentuale(risultato['aliquota_ivs'], 0)}):** "
        f"{formatta_euro(risultato['contributi_ivs'])}"
    )
    st.write(
        f"**Contributi aggiuntivi ({formatta_percentuale(risultato['aliquota_aggiuntiva'])}):** "
        f"{formatta_euro(risultato['contributi_aggiuntivi'])}"
    )
    st.write(f"**Totale contributi INPS:** {formatta_euro(risultato['totale_contributi'])}")

    st.markdown("---")
    st.subheader("⚖️ Ripartizione contributi")

    r1, r2 = st.columns(2)
    with r1:
        st.metric("Quota lavoratore (1/3)", formatta_euro(risultato["contributi_lavoratore"]))
    with r2:
        st.metric("Quota società (2/3)", formatta_euro(risultato["contributi_societa"]))

    st.markdown("---")
    st.subheader("🧮 Dettaglio fiscale (IRPEF)")

    st.write(f"**Esenzione fiscale (15.000€):** -{formatta_euro(risultato['franchigia_fiscale'])}")
    st.write(f"**Reddito imponibile:** {formatta_euro(risultato['reddito_imponibile'])}")
    st.write(
        f"**Contributi deducibili (lavoratore):** -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(
        f"**Reddito imponibile netto:** {formatta_euro(risultato['reddito_imponibile_netto'])}"
    )
    st.write(f"**IRPEF:** {formatta_euro(risultato['irpef'])}")
    st.write(f"**Addizionale regionale:** {formatta_euro(risultato['addizionale_regionale'])}")
    st.write(f"**Addizionale comunale:** {formatta_euro(risultato['addizionale_comunale'])}")
    st.write(f"**Totale imposte:** {formatta_euro(risultato['totale_imposte'])}")

    st.markdown("---")
    st.subheader("📋 Riepilogo")

    st.write(f"**Compenso lordo:** {formatta_euro(risultato['compenso_lordo'])}")
    st.write(
        f"├─ Contributi INPS lavoratore: -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(f"└─ Imposte (IRPEF + add.): -{formatta_euro(risultato['totale_imposte'])}")
    st.write(f"**= NETTO LAVORATORE:** {formatta_euro(risultato['netto_lavoratore'])}")

    st.markdown("---")
    st.write("**Costo per la società sportiva:**")
    st.write(f"├─ Compenso lordo: {formatta_euro(risultato['compenso_lordo'])}")
    st.write(
        f"└─ Contributi INPS società (2/3): +{formatta_euro(risultato['contributi_societa'])}"
    )
    st.write(
        f"**= COSTO TOTALE SOCIETÀ:** {formatta_euro(risultato['costo_totale_societa'])}"
    )

# ------------------------------------------------------------
# TABELLA COMPARATIVA (OPZIONALE)
# ------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Tabella comparativa")

df = pd.DataFrame(
    {
        "Voce": [
            "Compenso Lordo",
            "Contributi lavoratore (1/3)",
            "Imposte (IRPEF + add.)",
            "Netto lavoratore",
            "",
            "Contributi società (2/3)",
            "Costo totale società",
        ],
        "Importo": [
            formatta_euro(risultato["compenso_lordo"]),
            formatta_euro(risultato["contributi_lavoratore"]),
            formatta_euro(risultato["totale_imposte"]),
            formatta_euro(risultato["netto_lavoratore"]),
            "",
            formatta_euro(risultato["contributi_societa"]),
            formatta_euro(risultato["costo_totale_societa"]),
        ],
    }
)
st.table(df)
