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
    if reddito_imponibile <= 0:
        return 0.0
    elif reddito_imponibile <= 28000:
        return reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000:
        return 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else:
        return 28000 * 0.23 + 22000 * 0.35 + (reddito_imponibile - 50000) * 0.43

def calcola_cococo_sportivo(compenso_lordo,
                            altra_previdenza=False,
                            addizionali_reg=0.0,
                            addizionali_com=0.0):
    """
    Calcola imposte, contributi e costi per collaboratore sportivo in Co.Co.Co

    Ipotesi:
    - Compenso interamente da ASD/SSD
    - Franchigia fiscale 15.000 €
    - Franchigia contributiva 5.000 €
    - Dimezzamento base contributiva eccedenza (50%) fino al 2027
    - Ripartizione contributi 1/3 lavoratore, 2/3 società
    """

    # FRANCHIGIE
    franchigia_fiscale = min(compenso_lordo, 15000)
    franchigia_contributiva = min(compenso_lordo, 5000)

    # BASE CONTRIBUTIVA
    base_contrib_grezza = max(0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50  # agevolazione 50%

    # ALIQUOTE INPS GESTIONE SEPARATA
    if altra_previdenza:
        aliquota_ivs = 24.0
    else:
        aliquota_ivs = 25.0
    aliquota_aggiuntiva = 2.03  # maternità, malattia, ANF, DIS-COLL

    # CONTRIBUTI
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

# ============================================================================
# HEADER CON LOGO
# ============================================================================

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

# Info box con novità riforma sport
st.info("""
**ℹ️ Collaborazioni Sportive (Co.Co.Co) – Riforma dello Sport (D.Lgs. 36/2021)**

- 🎯 **Esenzione fiscale fino a 15.000€** sui compensi da ASD/SSD  
- 💰 **Esenzione contributiva fino a 5.000€** sui compensi da ASD/SSD  
- 📉 **Dimezzamento 50% della base contributiva** sull’eccedenza fino al 31/12/2027  
- ⚖️ **Contributi ripartiti:** 1/3 a carico del collaboratore, 2/3 a carico dell’ASD/SSD  
- 🧾 La società è sostituto d’imposta: gestisce ritenute, versamenti e CU
""")

st.markdown("---")

# ============================================================================
# LAYOUT A DUE COLONNE
# ============================================================================
col1, col2 = st.columns([1, 1])

# COLONNA SINISTRA - INPUT
with col1:
    st.header("📝 Dati Input")

    st.subheader("Tipo di collaborazione sportiva")
    tipo_attivita = st.selectbox(
        "Seleziona la tua attività",
        [
            "Collaboratore sportivo (istruttore/allenatore)",
            "Collaboratore amministrativo-gestionale",
            "Preparatore atletico",
            "Maestro di sport",
            "Altro collaboratore sportivo"
        ]
    )

    st.markdown("---")

    st.subheader("💰 Compensi annui")

    compenso_lordo = st.number_input(
        "Compenso lordo annuo Co.Co.Co (€)",
        min_value=0,
        max_value=200000,
        value=18000,
        step=1000,
        help="Totale compensi annui corrisposti da ASD/SSD con contratto di collaborazione coordinata e continuativa"
    )

    st.markdown("---")

    st.subheader("📊 Situazione previdenziale")
    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria",
        help="Se sei pensionato o iscritto ad altra forma previdenziale obbligatoria (es. cassa professionale), l'aliquota IVS è ridotta al 24%"
    )

    st.subheader("🏛️ Addizionali IRPEF (opzionale)")
    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input(
            "Addizionale regionale (%)",
            min_value=0.0,
            max_value=3.33,
            value=1.23,
            step=0.1,
            help="Aliquota addizionale regionale IRPEF (es. Puglia 1,23%)"
        )
    with col_add2:
        addizionale_com = st.number_input(
            "Addizionale comunale (%)",
            min_value=0.0,
            max_value=0.8,
            value=0.5,
            step=0.1,
            help="Aliquota addizionale comunale IRPEF (0–0,8%)"
        )

# COLONNA DESTRA - RISULTATI
with col2:
    st.header("📊 Risultati")

    # Calcolo
    risultato = calcola_cococo_sportivo(
        compenso_lordo=compenso_lordo,
        altra_previdenza=altra_prev,
        addizionali_reg=addizionale_reg,
        addizionali_com=addizionale_com
    )

    # Metriche principali
    st.subheader("💼 Panoramica generale")
    st.write(f"**Tipo di collaborazione:** {tipo_attivita}")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(
            "Compenso Lordo",
            formatta_euro(risultato['compenso_lordo']),
            help="Compenso lordo annuo pattuito con ASD/SSD"
        )
    with col_b:
        st.metric(
            "Netto Lavoratore",
            formatta_euro(risultato['netto_lavoratore']),
            help="Quanto arriva effettivamente al collaboratore dopo contributi e imposte"
        )
    with col_c:
        st.metric(
            "Costo Totale Società",
            formatta_euro(risultato['costo_totale_societa']),
            help="Costo complessivo per ASD/SSD (compenso + contributi a carico società)"
        )

    col_d, col_e = st.columns(2)
    with col_d:
        st.metric(
            "Netto Mensile",
            formatta_euro(risultato['netto_lavoratore']/12) if risultato['netto_lavoratore'] > 0 else "€ 0,00",
            help="Netto medio mensile (12 mensilità)"
        )
    with col_e:
        st.metric(
            "Tax Rate Effettivo",
            formatta_percentuale(risultato['tax_rate']),
            help="Incidenza complessiva di contributi e imposte sul compenso lordo"
        )

    # Dettaglio contributivo
    st.markdown("---")
    st.subheader("💼 Dettaglio Calcolo Contributivo")

    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")

    if risultato['franchigia_contributiva'] > 0:
        st.success(
            f"✅ **Esenzione contributiva:** -{formatta_euro(risultato['franchigia_contributiva'])} "
            "(primi 5.000€ da ASD/SSD)"
        )

    if risultato['base_contrib_grezza'] > 0:
        st.write(f"**Eccedenza contributiva:** {formatta_euro(risultato['base_contrib_grezza'])}")
        st.info(
            f"💡 **Dimezzamento 50% dell’eccedenza:** "
            f"{formatta_euro(risultato['base_contrib_grezza'])} × 50% = {formatta_euro(risultato['base_contrib_ridotta'])} "
            "(agevolazione fino al 31/12/2027)"
        )

    st.write(
        f"**Aliquota IVS:** {formatta_percentuale(risultato['aliquota_ivs'], 0)} "
        f"(applicata sulla base dimezzata)"
    )
    if altra_prev:
        st.info("✅ Aliquota IVS ridotta (24%) per presenza di altra previdenza/pensione")

    st.write(f"**Contributi IVS:** {formatta_euro(risultato['contributi_ivs'])}")
    st.write(
        f"**Aliquota aggiuntiva:** {formatta_percentuale(risultato['aliquota_aggiuntiva'])} "
        "(maternità, malattia, ANF, DIS-COLL – applicata sull’eccedenza piena)"
    )
    st.write(f"**Contributi aggiuntivi:** {formatta_euro(risultato['contributi_aggiuntivi'])}")
    st.write(f"**Totale contributi INPS:** {formatta_euro(risultato['totale_contributi'])}")

    st.markdown("---")
    st.subheader("⚖️ Ripartizione contributi")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric(
            "Quota lavoratore (1/3)",
            formatta_euro(risultato['contributi_lavoratore']),
            help="Contributi INPS trattenuti al collaboratore"
        )
    with col_r2:
        st.metric(
            "Quota società (2/3)",
            formatta_euro(risultato['contributi_societa']),
            help="Contributi INPS a carico di ASD/SSD"
        )

    # Dettaglio fiscale
    st.markdown("---")
    st.subheader("🧮 Dettaglio Calcolo Fiscale (IRPEF)")

    if risultato['franchigia_fiscale'] > 0:
        st.success(
            f"✅ **Esenzione fiscale:** -{formatta_euro(risultato['franchigia_fiscale'])} "
            "(primi 15.000€ di compensi da ASD/SSD)"
        )

    st.write(f"**Reddito imponibile lordo:** {formatta_euro(risultato['reddito_imponibile'])}")
    st.write(
        f"**Contributi deducibili (quota lavoratore):** -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(
        f"**Reddito imponibile netto IRPEF:** {formatta_euro(risultato['reddito_imponibile_netto'])}"
    )

    st.write(f"**IRPEF (scaglioni):** {formatta_euro(risultato['irpef'])}")
    if risultato['addizionale_regionale'] > 0:
        st.write(
            f"**Addizionale regionale ({formatta_percentuale(addizionale_reg, 2)}):** "
            f"{formatta_euro(risultato['addizionale_regionale'])}"
        )
    if risultato['addizionale_comunale'] > 0:
        st.write(
            f"**Addizionale comunale ({formatta_percentuale(addizionale_com, 2)}):** "
            f"{formatta_euro(risultato['addizionale_comunale'])}"
        )

    st.write(f"**Totale imposte:** {formatta_euro(risultato['totale_imposte'])}")

    # Riepilogo finale
    st.markdown("---")
    st.subheader("📋 Riepilogo Finale")

    st.write(f"**Compenso lordo:** {formatta_euro(risultato['compenso_lordo'])}")
    st.write(
        f"├─ Contributi INPS lavoratore: -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(
        f"└─ Imposte (IRPEF + addizionali): -{formatta_euro(risultato['totale_imposte'])}"
    )
    st.write(f"**= NETTO LAVORATORE:** {formatta_euro(risultato['netto_lavoratore'])}")

    st.markdown("---")
    st.write("**Costo per la società sportiva (ASD/SSD):**")
    st.write(f"├─ Compenso lordo: {formatta_euro(risultato['compenso_lordo'])}")
    st.write(
        f"└─ Contributi INPS società (2/3): +{formatta_euro(risultato['contributi_societa'])}"
    )
    st.write(
        f"**= COSTO TOTALE SOCIETÀ:** {formatta_euro(risultato['costo_totale_societa'])}"
    )

# ============================================================================
# INFO AGGIUNTIVE
# ============================================================================
st.markdown("---")
st.subheader("📚 Informazioni Utili")

with st.expander("🎯 Chi rientra tra i collaboratori sportivi Co.Co.Co?"):
    st.markdown("""
Sono inquadrati come **collaboratori sportivi** (Co.Co.Co) ai sensi della riforma dello sport:

- Istruttori e allenatori di discipline sportive dilettantistiche  
- Preparatori atletici  
- Collaboratori amministrativo-gestionali di ASD/SSD  
- Altri collaboratori che svolgono mansioni riconducibili all’attività sportiva dilettantistica

Il rapporto deve essere **coordinato e continuativo**, senza vincolo di subordinazione.
""")

with st.expander("💰 Esenzioni fiscali e contributive – riepilogo"):
    st.markdown("""
**Esenzione fiscale 15.000 €**

- I primi **15.000 €** di compensi annui da ASD/SSD **non concorrono al reddito IRPEF**  
- L’IRPEF si calcola solo sulla parte eccedente  

**Esenzione contributiva 5.000 € + dimezzamento**

- I primi **5.000 €** di compensi annui da ASD/SSD sono **esenti da contributi INPS**  
- La parte eccedente è assoggettata a contributi, ma la **base è dimezzata (50%) fino al 31/12/2027**  
- I contributi sono ripartiti **1/3 lavoratore – 2/3 ASD/SSD**
""")

with st.expander("⚖️ Co.Co.Co sportivo vs Partita IVA forfettaria"):
    st.markdown("""
**Co.Co.Co sportivo**

- Esenzioni dedicate (15.000 € fiscali, 5.000 € contributivi + base dimezzata)  
- Contributi in parte a carico della società  
- Nessuna gestione IVA, fatturazione, registri contabili  
- La società sportiva fa da **sostituto d’imposta**

**Partita IVA forfettaria**

- Nessuna esenzione specifica per compensi sportivi (ma aliquota sostitutiva 5–15%)  
- Contributi interamente a carico del titolare  
- Obblighi fiscali e contabili (fatture, dichiarazioni, ecc.)  
- Maggiore autonomia ma anche maggiore responsabilità gestionale
""")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])

with col_footer1:
    try:
        logo_footer = Image.open("FCC-LOGO.jpg")
        st.image(logo_footer, width=120)
    except:
        pass

with col_footer2:
    st.warning("""
**⚠️ Disclaimer:** Questo simulatore è indicativo e basato su regole generali della riforma dello sport.  
Non sostituisce una consulenza personalizzata che tenga conto di tutti i redditi, detrazioni e situazioni individuali.
""")

with col_footer3:
    st.markdown("**📞 Contatti**")
    st.markdown("**Fisco Chiaro Consulting**")
    st.markdown("📧 info@fiscochiaroconsulting.it")
    st.markdown("🌐 www.fiscochiaroconsulting.it")

st.markdown("---")
st.markdown("**Fisco Chiaro Consulting** | © 2025")
st.markdown("⚽ Specializzati in collaborazioni sportive e riforma del lavoro sportivo")
