import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Simulatore Co.Co.Co Sportivi 2025",
    page_icon="⚽",
    layout="wide"
)

def formatta_euro(valore):
    """Formatta un numero in euro con separatori italiani"""
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatta_percentuale(valore, decimali=2):
    """Formatta una percentuale con virgola italiana"""
    return f"{valore:.{decimali}f}%".replace(".", ",")

def calcola_irpef(reddito_imponibile):
    """
    Calcola IRPEF con scaglioni 2025
    """
    # Scaglioni IRPEF 2025
    if reddito_imponibile <= 0:
        return 0
    elif reddito_imponibile <= 28000:
        irpef = reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000:
        irpef = 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else:
        irpef = 28000 * 0.23 + 22000 * 0.35 + (reddito_imponibile - 50000) * 0.43

    return irpef

def calcola_cococo_sportivo(compenso_lordo, tipo_attivita, altra_previdenza=False, 
                            addizionali_reg=0, addizionali_com=0):
    """
    Calcola imposte, contributi e costi per co.co.co sportivo

    Parametri:
    - compenso_lordo: Compenso lordo annuo pattuito
    - tipo_attivita: Tipo di collaborazione sportiva
    - altra_previdenza: Se ha già altra pensione/previdenza
    - addizionali_reg: Aliquota addizionale regionale IRPEF
    - addizionali_com: Aliquota addizionale comunale IRPEF
    """

    # ESENZIONI E FRANCHIGIE
    franchigia_fiscale = min(compenso_lordo, 15000)  # Esenzione fiscale 15.000€
    franchigia_contributiva = min(compenso_lordo, 5000)  # Esenzione contributiva 5.000€

    # CALCOLO CONTRIBUTIVO
    # Base imponibile contributiva (compenso - franchigia 5.000€)
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)

    # Dimezzamento 50% fino al 2027 (D.Lgs. 36/2021)
    base_contrib_ridotta = base_contrib_grezza * 0.50

    # Aliquote INPS Gestione Separata 2025
    if altra_previdenza:
        aliquota_ivs = 24.0  # Con altra pensione/previdenza
        aliquota_aggiuntiva = 2.03  # Maternità, malattia, ANF, DIS-COLL
    else:
        aliquota_ivs = 25.0  # Senza altra previdenza
        aliquota_aggiuntiva = 2.03

    # Contributi IVS (sul 50% della base)
    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100)

    # Contributi aggiuntivi (sul totale eccedenza, non dimezzati)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100)

    # Totale contributi INPS
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi

    # Ripartizione contributi: 1/3 lavoratore, 2/3 società
    contributi_lavoratore = totale_contributi_inps * (1/3)
    contributi_societa = totale_contributi_inps * (2/3)

    # CALCOLO FISCALE
    # Reddito imponibile (compenso - franchigia fiscale 15.000€)
    reddito_imponibile = max(0, compenso_lordo - franchigia_fiscale)

    # Deduzione contributi versati dal lavoratore
    reddito_imponibile_netto = max(0, reddito_imponibile - contributi_lavoratore)

    # IRPEF (scaglioni)
    irpef = calcola_irpef(reddito_imponibile_netto)

    # Addizionali regionali e comunali
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100)

    # Totale imposte
    totale_imposte = irpef + addizionale_regionale + addizionale_comunale

    # CALCOLI FINALI
    # Totale trattenute lavoratore
    totale_trattenute = contributi_lavoratore + totale_imposte

    # Netto al lavoratore
    netto_lavoratore = compenso_lordo - totale_trattenute

    # Costo totale per la società
    costo_totale_societa = compenso_lordo + contributi_societa

    # Tax rate effettivo
    tax_rate = (totale_trattenute / compenso_lordo) * 100 if compenso_lordo > 0 else 0

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
        'totale_trattenute': totale_trattenute,
        'netto_lavoratore': netto_lavoratore,
        'costo_totale_societa': costo_totale_societa,
        'tax_rate': tax_rate
    }

# ============================================================================
# HEADER
# ============================================================================
st.title("⚽ Simulatore Co.Co.Co Sportivi 2025")
st.markdown("**by Fisco Chiaro Consulting**")

# Info box
st.info("""
**ℹ️ Collaborazioni Sportive (Co.Co.Co) - Novità 2025:**
- 🎯 **Esenzione fiscale fino a 15.000€** sui compensi da ASD/SSD
- 💰 **Esenzione contributiva fino a 5.000€** sui compensi da ASD/SSD
- 📉 **Dimezzamento 50%** base contributiva su eccedenza (fino 2027)
- ⚖️ **Ripartizione contributi:** 1/3 lavoratore - 2/3 società sportiva
- 🏢 Valido per: istruttori, allenatori, preparatori, collaboratori amministrativi
""")

st.markdown("---")

# ============================================================================
# LAYOUT A DUE COLONNE
# ============================================================================
col1, col2 = st.columns([1, 1])

# COLONNA SINISTRA - INPUT
with col1:
    st.header("📝 Dati Input")

    # Tipo di attività
    st.subheader("Tipo di collaborazione")
    tipo_attivita = st.selectbox(
        "Seleziona il tipo di attività",
        [
            "Istruttore/Allenatore sportivo",
            "Personal trainer",
            "Preparatore atletico",
            "Maestro di sport",
            "Collaboratore amministrativo-gestionale",
            "Altro collaboratore sportivo"
        ]
    )

    st.markdown("---")

    # Compenso lordo
    st.subheader("💰 Compenso annuo")

    compenso_lordo = st.number_input(
        "Compenso lordo annuo (€)",
        min_value=0,
        max_value=200000,
        value=18000,
        step=1000,
        help="Compenso lordo annuo pattuito con la società sportiva"
    )

    st.markdown("---")

    # Altra previdenza
    st.subheader("📊 Situazione previdenziale")

    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria",
        help="Se già pensionato o iscritto ad altra cassa, aliquota INPS ridotta al 24%"
    )

    st.markdown("---")

    # Addizionali IRPEF
    st.subheader("🏛️ Addizionali IRPEF (opzionale)")

    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input(
            "Add. Regionale (%)",
            min_value=0.0,
            max_value=3.33,
            value=1.23,
            step=0.1,
            help="Varia per regione (es. Puglia 1,23%)"
        )
    with col_add2:
        addizionale_com = st.number_input(
            "Add. Comunale (%)",
            min_value=0.0,
            max_value=0.8,
            value=0.5,
            step=0.1,
            help="Varia per comune (0-0,8%)"
        )

# COLONNA DESTRA - RISULTATI
with col2:
    st.header("📊 Risultati Simulazione")

    # Calcola risultati
    risultato = calcola_cococo_sportivo(
        compenso_lordo,
        tipo_attivita,
        altra_prev,
        addizionale_reg,
        addizionale_com
    )

    # Metriche principali
    st.subheader("💼 Panoramica")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(
            "Compenso Lordo",
            formatta_euro(risultato['compenso_lordo']),
            help="Compenso lordo annuo pattuito"
        )
    with col_b:
        st.metric(
            "Netto Lavoratore",
            formatta_euro(risultato['netto_lavoratore']),
            help="Quanto riceve effettivamente il lavoratore"
        )
    with col_c:
        st.metric(
            "Costo Società",
            formatta_euro(risultato['costo_totale_societa']),
            help="Costo totale per la società sportiva"
        )

    # Netto mensile e tax rate
    col_d, col_e = st.columns(2)
    with col_d:
        st.metric(
            "Netto Mensile",
            formatta_euro(risultato['netto_lavoratore']/12),
            help="Netto medio mensile lavoratore"
        )
    with col_e:
        st.metric(
            "Tax Rate Effettivo",
            formatta_percentuale(risultato['tax_rate']),
            help="% trattenute su compenso lordo"
        )

    # Dettaglio CONTRIBUTI
    st.markdown("---")
    st.subheader("💼 Dettaglio Contributi INPS")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")

    if risultato['franchigia_contributiva'] > 0:
        st.success(f"✅ **Esenzione contributiva:** -{formatta_euro(risultato['franchigia_contributiva'])} (primi 5.000€)")

    if risultato['base_contrib_grezza'] > 0:
        st.write(f"**Eccedenza:** {formatta_euro(risultato['base_contrib_grezza'])}")
        st.info(f"💡 **Dimezzamento 50%:** {formatta_euro(risultato['base_contrib_grezza'])} × 50% = {formatta_euro(risultato['base_contrib_ridotta'])} (agevolazione fino 2027)")

    st.write(f"**Aliquota IVS:** {formatta_percentuale(risultato['aliquota_ivs'], 0)} (calcolata sul 50%)")
    st.write(f"**Contributi IVS:** {formatta_euro(risultato['contributi_ivs'])}")

    st.write(f"**Aliquota aggiuntiva:** {formatta_percentuale(risultato['aliquota_aggiuntiva'])} (maternità, malattia, ecc.)")
    st.write(f"**Contributi aggiuntivi:** {formatta_euro(risultato['contributi_aggiuntivi'])}")

    st.markdown("---")
    st.write(f"**Totale contributi INPS:** {formatta_euro(risultato['totale_contributi'])}")

    # Ripartizione contributi
    st.markdown("---")
    st.subheader("⚖️ Ripartizione Contributi")

    col_ris1, col_ris2 = st.columns(2)
    with col_ris1:
        st.metric(
            "Quota Lavoratore (1/3)",
            formatta_euro(risultato['contributi_lavoratore']),
            help="Contributi a carico del lavoratore"
        )
    with col_ris2:
        st.metric(
            "Quota Società (2/3)",
            formatta_euro(risultato['contributi_societa']),
            help="Contributi a carico della società sportiva"
        )

    # Dettaglio FISCALE
    st.markdown("---")
    st.subheader("🧮 Dettaglio Fiscale (IRPEF)")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")

    if risultato['franchigia_fiscale'] > 0:
        st.success(f"✅ **Esenzione fiscale:** -{formatta_euro(risultato['franchigia_fiscale'])} (primi 15.000€ da ASD/SSD)")

    st.write(f"**Reddito imponibile:** {formatta_euro(risultato['reddito_imponibile'])}")
    st.write(f"**Contributi deducibili:** -{formatta_euro(risultato['contributi_lavoratore'])}")
    st.write(f"**Reddito imponibile netto:** {formatta_euro(risultato['reddito_imponibile_netto'])}")

    st.markdown("---")

    st.write(f"**IRPEF (scaglioni):** {formatta_euro(risultato['irpef'])}")
    if risultato['addizionale_regionale'] > 0:
        st.write(f"**Addizionale regionale ({formatta_percentuale(addizionale_reg, 2)}):** {formatta_euro(risultato['addizionale_regionale'])}")
    if risultato['addizionale_comunale'] > 0:
        st.write(f"**Addizionale comunale ({formatta_percentuale(addizionale_com, 2)}):** {formatta_euro(risultato['addizionale_comunale'])}")

    st.write(f"**Totale imposte:** {formatta_euro(risultato['totale_imposte'])}")

    # RIEPILOGO FINALE
    st.markdown("---")
    st.subheader("📋 Riepilogo Finale")

    st.write(f"**Compenso lordo:** {formatta_euro(risultato['compenso_lordo'])}")
    st.write(f"├─ Contributi INPS lavoratore: -{formatta_euro(risultato['contributi_lavoratore'])}")
    st.write(f"└─ Imposte (IRPEF + add.): -{formatta_euro(risultato['totale_imposte'])}")
    st.write(f"**= NETTO LAVORATORE:** {formatta_euro(risultato['netto_lavoratore'])}")

    st.markdown("---")

    st.write(f"**Costo per la società sportiva:**")
    st.write(f"├─ Compenso lordo: {formatta_euro(risultato['compenso_lordo'])}")
    st.write(f"└─ Contributi INPS società (2/3): +{formatta_euro(risultato['contributi_societa'])}")
    st.write(f"**= COSTO TOTALE SOCIETÀ:** {formatta_euro(risultato['costo_totale_societa'])}")

# ============================================================================
# TABELLA COMPARATIVA
# ============================================================================
st.markdown("---")
st.subheader("📊 Tabella Comparativa")

# Crea DataFrame per confronto
df_comparativo = pd.DataFrame({
    'Voce': [
        'Compenso Lordo',
        'Contributi Lavoratore (1/3)',
        'Imposte (IRPEF + add.)',
        'NETTO LAVORATORE',
        '',
        'Contributi Società (2/3)',
        'COSTO TOTALE SOCIETÀ'
    ],
    'Importo': [
        formatta_euro(risultato['compenso_lordo']),
        formatta_euro(risultato['contributi_lavoratore']),
        formatta_euro(risultato['totale_imposte']),
        formatta_euro(risultato['netto_lavoratore']),
        '',
        formatta_euro(risultato['contributi_societa']),
        formatta_euro(risultato['costo_totale_societa'])
    ],
    '% su Lordo': [
        '100%',
        formatta_percentuale((risultato['contributi_lavoratore']/compenso_lordo)*100),
        formatta_percentuale((risultato['totale_imposte']/compenso_lordo)*100),
        formatta_percentuale((risultato['netto_lavoratore']/compenso_lordo)*100),
        '',
        formatta_percentuale((risultato['contributi_societa']/compenso_lordo)*100),
        formatta_percentuale((risultato['costo_totale_societa']/compenso_lordo)*100)
    ]
})

st.table(df_comparativo)

# ============================================================================
# INFO AGGIUNTIVE
# ============================================================================
st.markdown("---")
st.subheader("📚 Informazioni Utili")

with st.expander("🎯 Come funzionano i contributi co.co.co sportivi?"):
    st.markdown("""
**Regole contributive 2025:**

✅ **Esenzione 5.000€:**
- I primi 5.000€ sono completamente esenti da contributi INPS

✅ **Dimezzamento 50% (fino 2027):**
- L'eccedenza oltre 5.000€ è ridotta al 50% per il calcolo
- Agevolazione temporanea fino al 31/12/2027

✅ **Aliquote INPS:**
- **25% IVS** (invalidità, vecchiaia, superstiti) sul 50% della base
- **2,03% aggiuntive** (maternità, malattia, ANF, DIS-COLL) sul 100% della base
- **24% IVS** se già pensionato o con altra previdenza

✅ **Ripartizione:**
- **1/3 (33,33%)** a carico del collaboratore sportivo
- **2/3 (66,67%)** a carico della società sportiva (ASD/SSD)

**Esempio:**
- Compenso: 18.000€
- Esenzione: 5.000€
- Eccedenza: 13.000€ → dimezzata = 6.500€
- Contributi IVS 25%: 6.500€ × 25% = 1.625€
- Contributi agg. 2,03%: 13.000€ × 2,03% = 264€
- Totale: 1.889€
- Lavoratore paga: 630€ (1/3)
- Società paga: 1.259€ (2/3)
""")

with st.expander("💰 Come funzionano le esenzioni fiscali?"):
    st.markdown("""
**Esenzione fiscale 15.000€:**

✅ **Chi ne beneficia:**
- Collaboratori sportivi con co.co.co da ASD/SSD
- Collaboratori amministrativo-gestionali sportivi
- Personal trainer, istruttori, allenatori

✅ **Come funziona:**
- I primi 15.000€ di compenso **non concorrono al reddito IRPEF**
- L'IRPEF si calcola solo sull'eccedenza oltre 15.000€
- Ma: i contributi del lavoratore sono comunque deducibili

**Esempio:**
- Compenso: 25.000€
- Esenzione: 15.000€
- Reddito imponibile: 10.000€
- Contributi deducibili: 800€
- Imponibile netto: 9.200€
- IRPEF 23%: 2.116€

Senza esenzione pagheresti IRPEF su 25.000€!
""")

with st.expander("⚖️ Differenze Co.Co.Co vs Partita IVA Forfettario"):
    st.markdown("""
**Confronto tra le due opzioni:**

| Aspetto | Co.Co.Co Sportivo | P.IVA Forfettario |
|---------|-------------------|-------------------|
| **Esenzione fiscale** | 15.000€ | No (ma aliquota 5-15%) |
| **Esenzione contributiva** | 5.000€ + 50% | No |
| **Contributi** | Ripartiti 1/3-2/3 | 100% a carico |
| **IRPEF** | Scaglioni normali | Imposta sostitutiva |
| **Limite ricavi** | Nessuno | 85.000€/anno |
| **Fatturazione** | Non necessaria | Obbligatoria |
| **Autonomia** | Coordinata | Piena autonomia |

**Quando conviene Co.Co.Co:**
- Compensi bassi (< 20.000€)
- Vuoi che società paghi parte contributi
- Non hai necessità di piena autonomia

**Quando conviene Forfettario:**
- Compensi alti (> 30.000€)
- Vuoi piena autonomia
- Hai più clienti
- Vuoi aliquota bassa fissa (5-15%)
""")

with st.expander("📋 Obblighi e adempimenti"):
    st.markdown("""
**Per il Lavoratore Sportivo:**

✅ **Autocertificazione:**
- Dichiarare di rientrare nei requisiti
- Fornire alla società sportiva

✅ **Dichiarazione dei redditi:**
- Compilare quadro RC (redditi collaborazione)
- Indicare compensi e contributi versati

✅ **Nessuna partita IVA necessaria**

**Per la Società Sportiva (ASD/SSD):**

✅ **Comunicazione RASD:**
- Registrazione collaboratore nel Registro Attività Sportive Dilettantistiche

✅ **Versamento contributi:**
- Entro il 16 del mese successivo
- Con modello F24

✅ **Certificazione Unica (CU):**
- Entro 16 marzo anno successivo
- Invio telematico all'Agenzia Entrate

✅ **Sostituto d'imposta:**
- Trattenere IRPEF se dovuta
- Versare ritenute con F24
""")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

st.warning("""
**⚠️ Disclaimer:** Questo simulatore è indicativo e basato sulla normativa vigente (D.Lgs. 36/2021 - Riforma dello Sport, 
Circolare INPS n. 27/2025). Per un calcolo preciso e personalizzato, contattaci per una consulenza specifica.
""")

st.markdown("---")
st.markdown("**Fisco Chiaro Consulting** | © 2025")
st.markdown("📧 info@fiscochiaroconsulting.it | 🌐 www.fiscochiaroconsulting.it")
st.markdown("⚽ Specializzati in consulenza fiscale per lavoratori sportivi")
