st.markdown("""
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================================
# CONFIGURAZIONE PAGINA
# =====================================================================
st.set_page_config(
    page_title="Simulatore Co.Co.Co Lavoratori Sportivi 2025",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .metric-green {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .metric-orange {
        background-color: #fff3cd;
        border-left-color: #ff9800;
    }
    .metric-red {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# FUNZIONI DI UTILITÀ
# =====================================================================
def formatta_euro(valore):
    """Formatta un numero in euro con separatori italiani."""
    return f"€ {valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatta_percentuale(valore, decimali=2):
    """Formatta una percentuale con virgola italiana."""
    return f"{valore:.{decimali}f}%".replace(".", ",")

def calcola_irpef(reddito_imponibile):
    """
    Calcola IRPEF con scaglioni 2025.
    - 0-28.000€: 23%
    - 28.001-50.000€: 35%
    - oltre 50.000€: 43%
    """
    if reddito_imponibile <= 0:
        return 0.0
    elif reddito_imponibile <= 28000:
        return reddito_imponibile * 0.23
    elif reddito_imponibile <= 50000:
        return 28000 * 0.23 + (reddito_imponibile - 28000) * 0.35
    else:
        return 28000 * 0.23 + 22000 * 0.35 + (reddito_imponibile - 50000) * 0.43

def calcola_cococo_sportivo(compenso_lordo, altra_previdenza=False, addizionali_reg=0.0, addizionali_com=0.0):
    """
    Calcola imposte, contributi e costi per collaboratore sportivo in Co.Co.Co.
    
    D.Lgs. 36/2021 - Riforma dello Sport
    - Esenzione fiscale: 15.000€
    - Esenzione contributiva: 5.000€
    - Dimezzamento base contributiva eccedenza: 50% fino al 31/12/2027
    - Ripartizione contributi: 1/3 lavoratore, 2/3 società
    """

    # Caso patologico: compenso nullo o negativo → tutto a zero
    if compenso_lordo <= 0:
        return {
            "compenso_lordo": 0.0,
            "franchigia_fiscale": 0.0,
            "franchigia_contributiva": 0.0,
            "base_contrib_grezza": 0.0,
            "base_contrib_ridotta": 0.0,
            "aliquota_ivs": 24.0 if altra_previdenza else 25.0,
            "aliquota_aggiuntiva": 2.03,
            "contributi_ivs": 0.0,
            "contributi_aggiuntivi": 0.0,
            "totale_contributi": 0.0,
            "contributi_lavoratore": 0.0,
            "contributi_societa": 0.0,
            "reddito_imponibile": 0.0,
            "reddito_imponibile_netto": 0.0,
            "irpef": 0.0,
            "addizionale_regionale": 0.0,
            "addizionale_comunale": 0.0,
            "totale_imposte": 0.0,
            "totale_trattenute_lavoratore": 0.0,
            "netto_lavoratore": 0.0,
            "costo_totale_societa": 0.0,
            "tax_rate": 0.0,
        }
    
    # FRANCHIGIE
    franchigia_fiscale = min(compenso_lordo, 15000.0)
    franchigia_contributiva = min(compenso_lordo, 5000.0)
    
    # BASE CONTRIBUTIVA
    base_contrib_grezza = max(0.0, compenso_lordo - franchigia_contributiva)
    base_contrib_ridotta = base_contrib_grezza * 0.50  # Dimezzamento 50%
    
    # ALIQUOTE INPS GESTIONE SEPARATA
    if altra_previdenza:
        aliquota_ivs = 24.0
    else:
        aliquota_ivs = 25.0
    aliquota_aggiuntiva = 2.03  # maternità, malattia, ANF, DIS-COLL
    
    # CALCOLO CONTRIBUTI
    contributi_ivs = base_contrib_ridotta * (aliquota_ivs / 100.0)
    contributi_aggiuntivi = base_contrib_grezza * (aliquota_aggiuntiva / 100.0)
    totale_contributi_inps = contributi_ivs + contributi_aggiuntivi
    
    contributi_lavoratore = totale_contributi_inps / 3.0
    contributi_societa = totale_contributi_inps * 2.0 / 3.0
    
    # BASE FISCALE
    reddito_imponibile = max(0.0, compenso_lordo - franchigia_fiscale)
    reddito_imponibile_netto = max(0.0, reddito_imponibile - contributi_lavoratore)
    
    # CALCOLO IMPOSTE
    irpef = calcola_irpef(reddito_imponibile_netto)
    addizionale_regionale = reddito_imponibile_netto * (addizionali_reg / 100.0)
    addizionale_comunale = reddito_imponibile_netto * (addizionali_com / 100.0)
    totale_imposte = irpef + addizionale_regionale + addizionale_comunale
    
    # RISULTATI FINALI
    totale_trattenute_lavoratore = contributi_lavoratore + totale_imposte
    netto_lavoratore = compenso_lordo - totale_trattenute_lavoratore
    costo_totale_societa = compenso_lordo + contributi_societa
    
    # Tax rate effettivo (bloccato tra 0 e 100 per evitare valori “fuori scala”)
    if compenso_lordo > 0:
        tax_rate_raw = (totale_trattenute_lavoratore / compenso_lordo * 100.0)
        tax_rate = max(0.0, min(100.0, tax_rate_raw))
    else:
        tax_rate = 0.0
    
    return {
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
        "totale_trattenute_lavoratore": totale_trattenute_lavoratore,
        "netto_lavoratore": netto_lavoratore,
        "costo_totale_societa": costo_totale_societa,
        "tax_rate": tax_rate,
    }

# =====================================================================
# HEADER
# =====================================================================
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1f77b4; margin-bottom: 5px;">⚽ Simulatore Co.Co.Co</h1>
        <h2 style="color: #555; font-size: 1.5em; margin-bottom: 10px;">Collaboratori Sportivi 2025</h2>
        <p style="color: #888; font-size: 1.1em;"><strong>by Fisco Chiaro Consulting</strong></p>
    </div>
""", unsafe_allow_html=True)

# Info box
st.info(
    "**ℹ️ Collaborazioni Sportive (Co.Co.Co) – Riforma dello Sport (D.Lgs. 36/2021)**\n\n"
    "🎯 **Esenzione fiscale:** fino a 15.000€ sui compensi da ASD/SSD\n"
    "💰 **Esenzione contributiva:** fino a 5.000€ sui compensi da ASD/SSD\n"
    "📉 **Dimezzamento 50%** della base contributiva sull'eccedenza fino al 31/12/2027\n"
    "⚖️ **Contributi ripartiti:** 1/3 collaboratore – 2/3 ASD/SSD\n"
    "🧾 **La società sportiva è sostituto d'imposta:** ritenute, versamenti e Certificazione Unica"
)

st.markdown("---")

# =====================================================================
# LAYOUT A DUE COLONNE
# =====================================================================
col_input, col_risultati = st.columns(2)

# =====================================================================
# COLONNA SINISTRA - INPUT
# =====================================================================
with col_input:
    st.header("📝 Dati di Input")
    
    st.subheader("Tipo di collaborazione sportiva")
    tipo_attivita = st.selectbox(
        "Seleziona la tua attività",
        [
            "Collaboratore sportivo (istruttore/allenatore)",
            "Collaboratore amministrativo-gestionale",
            "Preparatore atletico",
            "Maestro di sport",
            "Altro collaboratore sportivo",
        ],
        key="tipo_attivita"
    )
    
    st.markdown("---")
    
    st.subheader("💰 Compensi annui")
    
    compenso_lordo = st.number_input(
        "Compenso lordo annuo Co.Co.Co (€)",
        min_value=0,
        max_value=200000,
        value=18000,
        step=500,
        key="compenso_cococo",
        help="Totale compensi annui corrisposti da ASD/SSD con contratto di collaborazione coordinata e continuativa."
    )
    
    if compenso_lordo == 0:
        st.warning("Inserisci un compenso lordo annuo maggiore di zero per ottenere il calcolo completo.")
    
    st.markdown("---")
    
    st.subheader("📊 Situazione previdenziale")
    altra_prev = st.checkbox(
        "Ho già altra pensione o previdenza obbligatoria",
        value=False,
        key="altra_prev",
        help="Se sei pensionato o iscritto ad altra forma previdenziale obbligatoria, l'aliquota IVS è ridotta al 24%."
    )
    
    st.markdown("---")
    
    st.subheader("🏛️ Addizionali IRPEF (opzionale)")
    
    col_add1, col_add2 = st.columns(2)
    with col_add1:
        addizionale_reg = st.number_input(
            "Addizionale regionale (%)",
            min_value=0.0,
            max_value=3.33,
            value=1.23,
            step=0.05,
            key="addizionale_reg",
            help="Aliquota addizionale regionale IRPEF (es. Puglia 1,23%)"
        )
    
    with col_add2:
        addizionale_com = st.number_input(
            "Addizionale comunale (%)",
            min_value=0.0,
            max_value=0.8,
            value=0.5,
            step=0.05,
            key="addizionale_com",
            help="Aliquota addizionale comunale IRPEF (0–0,8%)"
        )
    
    st.markdown("---")
    
    st.info("ℹ️ I calcoli si aggiornano automaticamente mentre digiti")

# =====================================================================
# COLONNA DESTRA - RISULTATI
# =====================================================================
with col_risultati:
    st.header("📊 Risultati Calcolo")
    
    # Eseguire il calcolo
    risultato = calcola_cococo_sportivo(
        compenso_lordo=compenso_lordo,
        altra_previdenza=altra_prev,
        addizionali_reg=addizionale_reg,
        addizionali_com=addizionale_com
    )
    
    # ===== PANORAMICA GENERALE =====
    st.subheader("💼 Panoramica Generale")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(
            label="Compenso Lordo",
            value=formatta_euro(risultato["compenso_lordo"]),
            help="Compenso lordo annuo pattuito"
        )
    
    with col_m2:
        st.metric(
            label="Netto Lavoratore",
            value=formatta_euro(risultato["netto_lavoratore"]),
            help="Quanto arriva al collaboratore"
        )
    
    with col_m3:
        st.metric(
            label="Costo Società",
            value=formatta_euro(risultato["costo_totale_societa"]),
            help="Costo complessivo per ASD/SSD"
        )
    
    col_m4, col_m5 = st.columns(2)
    
    with col_m4:
        netto_mensile = max(0.0, risultato["netto_lavoratore"] / 12.0)
        st.metric(
            label="Netto Mensile",
            value=formatta_euro(netto_mensile),
            help="Media su 12 mensilità"
        )
    
    with col_m5:
        st.metric(
            label="Tax Rate Effettivo",
            value=formatta_percentuale(risultato["tax_rate"]),
            help="Incidenza di contributi e imposte"
        )
    
    # ===== DETTAGLIO CONTRIBUTIVO =====
    st.markdown("---")
    st.subheader("💼 Dettaglio Calcolo Contributivo")
    
    st.write(f"**Compenso lordo:** {formatta_euro(compenso_lordo)}")
    
    if risultato["franchigia_contributiva"] > 0:
        st.success(
            f"✅ **Esenzione contributiva (5.000€):** "
            f"-{formatta_euro(risultato['franchigia_contributiva'])}"
        )
    
    if risultato["base_contrib_grezza"] > 0:
        st.write(f"**Eccedenza contributiva:** {formatta_euro(risultato['base_contrib_grezza'])}")
        st.info(
            f"💡 **Dimezzamento 50% (agevolazione fino al 31/12/2027):** "
            f"{formatta_euro(risultato['base_contrib_grezza'])} × 50% = "
            f"{formatta_euro(risultato['base_contrib_ridotta'])}"
        )
    
    st.write(
        f"**Aliquota IVS:** {formatta_percentuale(risultato['aliquota_ivs'], 0)} "
        f"(applicata sulla base dimezzata)"
    )
    
    if altra_prev:
        st.info("✅ Aliquota IVS ridotta (24%) per altra previdenza/pensione")
    
    st.write(f"**Contributi IVS:** {formatta_euro(risultato['contributi_ivs'])}")
    st.write(
        f"**Aliquota aggiuntiva:** {formatta_percentuale(risultato['aliquota_aggiuntiva'])} "
        f"(applicata sulla base piena)"
    )
    st.write(f"**Contributi aggiuntivi:** {formatta_euro(risultato['contributi_aggiuntivi'])}")
    
    st.write(f"**Totale contributi INPS:** {formatta_euro(risultato['totale_contributi'])}")
    
    # Ripartizione
    st.markdown("---")
    st.subheader("⚖️ Ripartizione Contributi")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric(
            "Quota lavoratore (1/3)",
            formatta_euro(risultato["contributi_lavoratore"]),
            help="Trattenuti al collaboratore"
        )
    with col_r2:
        st.metric(
            "Quota società (2/3)",
            formatta_euro(risultato["contributi_societa"]),
            help="A carico di ASD/SSD"
        )
    
    # ===== DETTAGLIO FISCALE =====
    st.markdown("---")
    st.subheader("🧮 Dettaglio Calcolo Fiscale (IRPEF)")
    
    if risultato["franchigia_fiscale"] > 0:
        st.success(
            f"✅ **Esenzione fiscale (15.000€):** "
            f"-{formatta_euro(risultato['franchigia_fiscale'])}"
        )
    
    st.write(f"**Reddito imponibile lordo:** {formatta_euro(risultato['reddito_imponibile'])}")
    st.write(
        f"**Contributi deducibili (1/3):** -{formatta_euro(risultato['contributi_lavoratore'])}"
    )
    st.write(
        f"**Reddito imponibile netto IRPEF:** {formatta_euro(risultato['reddito_imponibile_netto'])}"
    )
    
    st.write(f"**IRPEF (scaglioni 23-35-43%):** {formatta_euro(risultato['irpef'])}")
    
    if risultato["addizionale_regionale"] > 0:
        st.write(
            f"**Addizionale regionale ({formatta_percentuale(addizionale_reg)}):** "
            f"{formatta_euro(risultato['addizionale_regionale'])}"
        )
    
    if risultato["addizionale_comunale"] > 0:
        st.write(
            f"**Addizionale comunale ({formatta_percentuale(addizionale_com)}):** "
            f"{formatta_euro(risultato['addizionale_comunale'])}"
        )
    
    st.write(f"**Totale imposte:** {formatta_euro(risultato['totale_imposte'])}")
    
    # ===== RIEPILOGO FINALE =====
    st.markdown("---")
    st.subheader("📋 Riepilogo Finale Completo")
    
    st.write(f"**Compenso lordo annuo:** {formatta_euro(risultato['compenso_lordo'])}")
    st.write(f"├─ Contributi INPS lavoratore: -{formatta_euro(risultato['contributi_lavoratore'])}")
    st.write(f"└─ Imposte (IRPEF + addizionali): -{formatta_euro(risultato['totale_imposte'])}")
    
    st.success(f"**= NETTO LAVORATORE ANNUALE:** {formatta_euro(risultato['netto_lavoratore'])}")
    st.success(f"**= NETTO LAVORATORE MENSILE:** {formatta_euro(netto_mensile)}")
    
    st.markdown("---")
    st.write("**Costo complessivo per la società sportiva (ASD/SSD):**")
    st.write(f"├─ Compenso lordo: {formatta_euro(risultato['compenso_lordo'])}")
    st.write(f"└─ Contributi INPS società (2/3): +{formatta_euro(risultato['contributi_societa'])}")
    
    st.warning(f"**= COSTO TOTALE SOCIETÀ:** {formatta_euro(risultato['costo_totale_societa'])}")

# =====================================================================
# SEZIONE INFO AGGIUNTIVE
# =====================================================================
st.markdown("---")
st.subheader("📚 Informazioni Utili")

with st.expander("🎯 Chi rientra tra i collaboratori sportivi Co.Co.Co?"):
    st.markdown("""
Sono inquadrati come **collaboratori sportivi** (Co.Co.Co) ai sensi della riforma dello sport:

- **Istruttori e allenatori** di discipline sportive dilettantistiche
- **Preparatori atletici**
- **Collaboratori amministrativo-gestionali** di ASD/SSD
- **Maestri di sport** e altri collaboratori con mansioni sportive dilettantistiche

Il rapporto deve essere **coordinato e continuativo**, senza vincolo di subordinazione.
    """)

with st.expander("💰 Esenzioni fiscali e contributive – riepilogo completo"):
    st.markdown("""
**Esenzione fiscale 15.000€**
- I primi **15.000€** di compensi annui da ASD/SSD **non concorrono al reddito IRPEF**
- L'IRPEF si calcola solo sulla parte eccedente
- Fonte: Art. 36, comma 6 D.Lgs. 36/2021

**Esenzione contributiva 5.000€ + dimezzamento 50%**
- I primi **5.000€** di compensi annui da ASD/SSD sono **esenti da contributi INPS**
- La parte eccedente è assoggettata a contributi, ma la **base è dimezzata (50%)** fino al 31/12/2027
- I contributi sono ripartiti **1/3 lavoratore – 2/3 ASD/SSD**
- Fonte: Art. 28 e 38 D.Lgs. 36/2021

**Ritenuta d'acconto**
- Effettuata dalla società sportiva (sostituto d'imposta)
- Aliquota: 20% sui compensi lordi
- Versamento: entro il 16 del mese successivo
    """)

with st.expander("⚖️ Co.Co.Co sportivo vs Partita IVA forfettaria"):
    st.markdown("""
| Aspetto | Co.Co.Co Sportivo | Partita IVA Forfettaria |
|---------|------------------|------------------------|
| **Esenzione IRPEF** | Sì, fino a 15.000€ | No |
| **Esenzione INPS** | Sì, fino a 5.000€ | No |
| **Base contributiva** | Dimezzata 50% (eccedenza) | Intera |
| **Contributi a carico** | 1/3 collaboratore, 2/3 società | 100% collaboratore |
| **Gestione IVA** | No | Sì, ordinaria o forfettaria |
| **Fatturazione** | No | Sì, obbligatoria |
| **Sostituto d'imposta** | ASD/SSD | Collaboratore |
| **Contabilità** | Semplificata | Ordinaria o semplificata |
| **Complessità** | Bassa | Alta |
    """)

with st.expander("📋 Obblighi fiscali e scadenze 2025"):
    st.markdown("""
**Obblighi della Società Sportiva (ASD/SSD):**
- ✅ **Comunicazione RASD:** Entro 30 giorni dalla stipula del contratto
- ✅ **Versamento ritenute IRPEF:** Entro il 16 del mese seguente (F24 con codice tributo 1040)
- ✅ **Versamento contributi INPS:** Entro il 16 del mese seguente (F24 con codice tributo 4104)
- ✅ **Certificazione Unica (CU):** Entro il 31 gennaio dell'anno successivo
- ✅ **Tracciabilità:** Pagamento su conto corrente intestato alla ASD (vietato contante)

**Obblighi del Collaboratore:**
- ✅ **Conservazione documenti:** 5 anni (contratti, ricevute, CU)
- ✅ **Dichiarazione dei redditi:** Se la CU della società non è completa
- ✅ **Aggiornamenti RASD:** Se cambiamenti contrattuali

**Termini principali:**
- **Versamenti:** Entro il 16 del mese seguente
- **Certificazione Unica:** 31 gennaio anno successivo
- **Conservazione:** 5 anni
    """)

# =====================================================================
# FOOTER / DISCLAIMER
# =====================================================================
st.markdown("---")

col_footer1, col_footer2 = st.columns([1, 1])

with col_footer1:
    st.warning("""
⚠️ **DISCLAIMER IMPORTANTE**

Questo simulatore ha finalità **esclusivamente informative** e non sostituisce una consulenza fiscale personalizzata.

- ✅ I calcoli sono basati su norme vigenti (D.Lgs. 36/2021 e aggiornamenti 2025)
- ⚠️ La situazione fiscale dipende da molteplici fattori individuali
- 🔄 Verificare sempre aggiornamenti normativi in corso d'anno
- 📞 Consultare sempre un **commercialista qualificato** per decisioni operative
    """)

with col_footer2:
    st.info("""
**📞 Supporto e Contatti**

**Fisco Chiaro Consulting**
- 📧 info@fiscochiaroconsulting.it
- 🌐 www.fiscochiaroconsulting.it
- 📱 Specializzati in collaborazioni sportive
- ⚽ Riforma dello sport e lavoro dilettantistico

**Versione:** 1.1 – Dicembre 2025
**Normativa:** D.Lgs. 36/2021 + aggiornamenti 2025
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; margin-top: 30px;">
    <p>⚽ <strong>Simulatore Co.Co.Co Sportivo</strong> | Fisco Chiaro Consulting</p>
    <p>Basato su D.Lgs. 36/2021 (Riforma dello Sport) e IRPEF 2025</p>
    <p>© 2025 – Tutti i diritti riservati</p>
</div>
""", unsafe_allow_html=True)
