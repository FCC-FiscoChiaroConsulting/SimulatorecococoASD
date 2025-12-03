
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulatore Co.Co.Co Sportivo 2025</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.95;
        }

        .info-box {
            background: #e3f2fd;
            border-left: 5px solid #1f77b4;
            padding: 20px;
            margin: 20px;
            border-radius: 8px;
            color: #0d47a1;
            font-size: 0.95em;
            line-height: 1.6;
        }

        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 40px;
        }

        .section {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .section-title {
            font-size: 1.4em;
            font-weight: 600;
            color: #1f77b4;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-group label {
            font-weight: 500;
            color: #333;
            font-size: 0.95em;
        }

        .form-group input,
        .form-group select {
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 1em;
            transition: all 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #1f77b4;
            box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
            background-color: #f5f9ff;
        }

        .form-group input[type="number"] {
            font-family: 'Courier New', monospace;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            background: #f9f9f9;
            border-radius: 6px;
        }

        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
            accent-color: #1f77b4;
        }

        .checkbox-group label {
            cursor: pointer;
            margin: 0;
            font-size: 0.95em;
        }

        .metric {
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .metric-title {
            font-size: 0.85em;
            opacity: 0.9;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .metric-value {
            font-size: 1.8em;
            font-weight: 700;
            font-family: 'Courier New', monospace;
        }

        .metric-sub {
            font-size: 0.75em;
            opacity: 0.8;
            margin-top: 5px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }

        .detail-box {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 3px solid #1f77b4;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            font-size: 0.95em;
        }

        .detail-row:last-child {
            border-bottom: none;
        }

        .detail-label {
            font-weight: 500;
            color: #333;
        }

        .detail-value {
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: #1f77b4;
        }

        .total-row {
            background: #e3f2fd;
            padding: 12px;
            border-radius: 4px;
            font-size: 1.05em;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
        }

        .success-value {
            color: #28a745;
            font-weight: 700;
        }

        .warning-value {
            color: #ff9800;
            font-weight: 700;
        }

        .error-value {
            color: #d62728;
            font-weight: 700;
        }

        .divider {
            height: 1px;
            background: #ddd;
            margin: 20px 0;
        }

        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #ddd;
        }

        .footer-disclaimer {
            background: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 20px;
            border-radius: 6px;
            color: #856404;
            font-size: 0.9em;
            line-height: 1.6;
        }

        @media (max-width: 1024px) {
            .content {
                grid-template-columns: 1fr;
            }

            .metrics-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 2em;
            }
        }

        .section-subtitle {
            font-size: 1.05em;
            font-weight: 600;
            color: #333;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        .help-text {
            font-size: 0.85em;
            color: #666;
            margin-top: 4px;
            font-style: italic;
        }

        .success-badge {
            display: inline-block;
            background: #d4edda;
            color: #155724;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .warning-badge {
            display: inline-block;
            background: #fff3cd;
            color: #856404;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ Simulatore Co.Co.Co</h1>
            <p>Collaboratori Sportivi 2025</p>
            <p style="font-size: 0.9em; margin-top: 10px;">D.Lgs. 36/2021 – Riforma dello Sport</p>
        </div>

        <div class="info-box">
            <strong>ℹ️ Collaborazioni Sportive (Co.Co.Co)</strong><br>
            • 🎯 Esenzione fiscale fino a 15.000€ sui compensi da ASD/SSD<br>
            • 💰 Esenzione contributiva fino a 5.000€ sui compensi da ASD/SSD<br>
            • 📉 Dimezzamento 50% della base contributiva sull'eccedenza fino al 31/12/2027<br>
            • ⚖️ Contributi ripartiti: 1/3 collaboratore – 2/3 ASD/SSD<br>
            • 🧾 La società sportiva è sostituto d'imposta
        </div>

        <div class="content">
            <!-- COLONNA SINISTRA: INPUT -->
            <div class="section">
                <h2 class="section-title">📝 Dati di Input</h2>

                <div class="form-group">
                    <label for="tipo_attivita">Tipo di collaborazione sportiva</label>
                    <select id="tipo_attivita" onchange="calcola()">
                        <option value="Istruttore/Allenatore">Collaboratore sportivo (istruttore/allenatore)</option>
                        <option value="Amministrativo-gestionale">Collaboratore amministrativo-gestionale</option>
                        <option value="Preparatore atletico">Preparatore atletico</option>
                        <option value="Maestro di sport">Maestro di sport</option>
                        <option value="Altro">Altro collaboratore sportivo</option>
                    </select>
                </div>

                <div class="divider"></div>

                <h3 class="section-subtitle">💰 Compensi Annui</h3>
                <div class="form-group">
                    <label for="compenso_lordo">Compenso lordo annuo Co.Co.Co (€)</label>
                    <input type="number" id="compenso_lordo" min="0" max="200000" value="18000" step="1000" onchange="calcola()" oninput="calcola()">
                    <span class="help-text">Totale compensi annui corrisposti da ASD/SSD</span>
                </div>

                <div class="divider"></div>

                <h3 class="section-subtitle">📊 Situazione Previdenziale</h3>
                <div class="checkbox-group">
                    <input type="checkbox" id="altra_prev" onchange="calcola()">
                    <label for="altra_prev">Ho già altra pensione o previdenza obbligatoria</label>
                </div>
                <span class="help-text" style="margin-left: 0;">Se pensionato o iscritto ad altra forma previdenziale, aliquota IVS ridotta al 24%</span>

                <div class="divider"></div>

                <h3 class="section-subtitle">🏛️ Addizionali IRPEF</h3>
                <div class="form-group">
                    <label for="addizionale_reg">Addizionale regionale (%)</label>
                    <input type="number" id="addizionale_reg" min="0" max="3.33" value="1.23" step="0.1" onchange="calcola()" oninput="calcola()">
                    <span class="help-text">Es. Puglia 1,23%, Lombardia 1,23%, etc.</span>
                </div>

                <div class="form-group">
                    <label for="addizionale_com">Addizionale comunale (%)</label>
                    <input type="number" id="addizionale_com" min="0" max="0.8" value="0.5" step="0.1" onchange="calcola()" oninput="calcola()">
                    <span class="help-text">Solitamente tra 0% e 0,8%</span>
                </div>
            </div>

            <!-- COLONNA DESTRA: RISULTATI -->
            <div class="section">
                <h2 class="section-title">📊 Risultati Calcolo</h2>

                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-title">Compenso Lordo</div>
                        <div class="metric-value" id="display_lordo">€ 0,00</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">Netto Lavoratore</div>
                        <div class="metric-value" id="display_netto">€ 0,00</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">Netto Mensile</div>
                        <div class="metric-value" id="display_netto_mese">€ 0,00</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">Tax Rate Effettivo</div>
                        <div class="metric-value" id="display_tax_rate">0,00%</div>
                    </div>
                </div>

                <div class="detail-box">
                    <div class="section-subtitle">💼 Panoramica Generale</div>
                    <div class="detail-row">
                        <span class="detail-label">Tipo collaborazione:</span>
                        <span class="detail-value" id="display_tipo">—</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Costo totale società:</span>
                        <span class="detail-value" id="display_costo_societa">€ 0,00</span>
                    </div>
                </div>

                <div class="divider"></div>

                <div class="detail-box">
                    <div class="section-subtitle">💼 Dettaglio Contributivo</div>
                    
                    <div id="esenz_contrib" style="display:none;">
                        <div class="success-badge">✅ Esenzione contributiva applicata</div>
                    </div>

                    <div class="detail-row">
                        <span class="detail-label">Compenso lordo:</span>
                        <span class="detail-value" id="contrib_lordo">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Franchigia (5.000€):</span>
                        <span class="detail-value success-value" id="contrib_franchigia">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Eccedenza contributiva:</span>
                        <span class="detail-value" id="contrib_eccedenza">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Base dimezzata 50% (agevolazione):</span>
                        <span class="detail-value warning-value" id="contrib_dimezzata">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Aliquota IVS:</span>
                        <span class="detail-value" id="contrib_aliquota">0,00%</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Contributi IVS:</span>
                        <span class="detail-value" id="contrib_ivs">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Contributi aggiuntivi (2,03%):</span>
                        <span class="detail-value" id="contrib_aggiuntivi">€ 0,00</span>
                    </div>
                    <div class="detail-row" style="border-bottom: 2px solid #1f77b4; padding-bottom: 10px; margin-bottom: 10px;">
                        <span class="detail-label"><strong>Totale contributi INPS:</strong></span>
                        <span class="detail-value" id="contrib_totale" style="color: #d62728;">€ 0,00</span>
                    </div>

                    <div class="detail-row">
                        <span class="detail-label">Quota lavoratore (1/3):</span>
                        <span class="detail-value" id="contrib_lavoratore">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Quota società (2/3):</span>
                        <span class="detail-value" id="contrib_societa">€ 0,00</span>
                    </div>
                </div>

                <div class="divider"></div>

                <div class="detail-box">
                    <div class="section-subtitle">🧮 Dettaglio Fiscale (IRPEF)</div>
                    
                    <div id="esenz_fiscal" style="display:none;">
                        <div class="success-badge">✅ Esenzione fiscale applicata</div>
                    </div>

                    <div class="detail-row">
                        <span class="detail-label">Franchigia fiscale (15.000€):</span>
                        <span class="detail-value success-value" id="fiscal_franchigia">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Reddito imponibile lordo:</span>
                        <span class="detail-value" id="fiscal_redd_lordo">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Contributi deducibili:</span>
                        <span class="detail-value" id="fiscal_contributi_ded">€ 0,00</span>
                    </div>
                    <div class="detail-row" style="border-bottom: 2px solid #1f77b4; padding-bottom: 10px; margin-bottom: 10px;">
                        <span class="detail-label"><strong>Reddito imponibile netto:</strong></span>
                        <span class="detail-value" id="fiscal_redd_netto">€ 0,00</span>
                    </div>

                    <div class="detail-row">
                        <span class="detail-label">IRPEF (scaglioni):</span>
                        <span class="detail-value error-value" id="fiscal_irpef">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Addizionale regionale:</span>
                        <span class="detail-value" id="fiscal_add_reg">€ 0,00</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Addizionale comunale:</span>
                        <span class="detail-value" id="fiscal_add_com">€ 0,00</span>
                    </div>
                    <div class="detail-row" style="border-bottom: 2px solid #1f77b4; padding-bottom: 10px; margin-bottom: 10px;">
                        <span class="detail-label"><strong>Totale imposte:</strong></span>
                        <span class="detail-value error-value" id="fiscal_totale">€ 0,00</span>
                    </div>
                </div>

                <div class="divider"></div>

                <div class="total-row">
                    <span>Compenso lordo:</span>
                    <span id="riepilogo_lordo">€ 0,00</span>
                </div>
                <div style="padding: 8px 0; display: flex; justify-content: space-between; font-size: 0.9em;">
                    <span>├─ Contributi INPS:</span>
                    <span id="riepilogo_contrib" style="color: #d62728;">€ 0,00</span>
                </div>
                <div style="padding: 8px 0; display: flex; justify-content: space-between; font-size: 0.9em;">
                    <span>└─ Imposte IRPEF + add.:</span>
                    <span id="riepilogo_imposte" style="color: #d62728;">€ 0,00</span>
                </div>
                <div class="total-row" style="background: #d4edda; color: #155724; margin-top: 10px;">
                    <span><strong>= NETTO LAVORATORE:</strong></span>
                    <span id="riepilogo_netto">€ 0,00</span>
                </div>

                <div class="divider"></div>

                <div class="total-row" style="background: #f5f5f5; color: #333;">
                    <span><strong>Costo TOTALE Società (ASD/SSD):</strong></span>
                    <span id="riepilogo_costo_societa">€ 0,00</span>
                </div>
            </div>
        </div>

        <div class="footer-disclaimer">
            <strong>⚠️ Disclaimer:</strong> Questo simulatore è indicativo e basato su regole generali della riforma dello sport (D.Lgs. 36/2021). 
            Non sostituisce una consulenza personalizzata che tenga conto di tutti i redditi, detrazioni e situazioni individuali. 
            Verifica sempre con un commercialista prima di firmare contratti.
        </div>

        <div class="footer">
            <p><strong>⚽ Fisco Chiaro Consulting</strong></p>
            <p>Simulatore Co.Co.Co Sportivo 2025 | © 2025</p>
            <p style="margin-top: 10px; opacity: 0.7;">Specializzati in collaborazioni sportive e riforma del lavoro sportivo</p>
        </div>
    </div>

    <script>
        function formattaEuro(valore) {
            return new Intl.NumberFormat('it-IT', {
                style: 'currency',
                currency: 'EUR',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(valore);
        }

        function calcolaIRPEF(redditoImponibile) {
            if (redditoImponibile <= 0) return 0;
            if (redditoImponibile <= 28000) {
                return redditoImponibile * 0.23;
            }
            if (redditoImponibile <= 50000) {
                return 28000 * 0.23 + (redditoImponibile - 28000) * 0.35;
            }
            return 28000 * 0.23 + 22000 * 0.35 + (redditoImponibile - 50000) * 0.43;
        }

        function calcola() {
            // INPUT
            const compensoLordo = parseFloat(document.getElementById('compenso_lordo').value) || 0;
            const altraPrevidenza = document.getElementById('altra_prev').checked;
            const additionalReg = parseFloat(document.getElementById('addizionale_reg').value) || 0;
            const additionalCom = parseFloat(document.getElementById('addizionale_com').value) || 0;
            const tipoAttivita = document.getElementById('tipo_attivita').value;

            // FRANCHIGIE
            const franchiGiaFiscale = Math.min(compensoLordo, 15000);
            const franchiGiaContributiva = Math.min(compensoLordo, 5000);

            // BASE CONTRIBUTIVA
            const baseContribGretta = Math.max(0, compensoLordo - franchiGiaContributiva);
            const baseContribRidotta = baseContribGretta * 0.50;

            // ALIQUOTE INPS
            const aliquotaIvs = altraPrevidenza ? 24 : 25;
            const aliquotaAggiuntiva = 2.03;

            // CONTRIBUTI
            const contributiIvs = baseContribRidotta * (aliquotaIvs / 100);
            const contributiAggiuntivi = baseContribGretta * (aliquotaAggiuntiva / 100);
            const totaleContributiInps = contributiIvs + contributiAggiuntivi;

            const contributiLavoratore = totaleContributiInps / 3;
            const contributiSocieta = totaleContributiInps * 2 / 3;

            // BASE FISCALE
            const redditoImponibile = Math.max(0, compensoLordo - franchiGiaFiscale);
            const redditoImponibileNetto = Math.max(0, redditoImponibile - contributiLavoratore);

            // IMPOSTE
            const irpef = calcolaIRPEF(redditoImponibileNetto);
            const additionalRegionale = redditoImponibileNetto * (additionalReg / 100);
            const additionalComunale = redditoImponibileNetto * (additionalCom / 100);
            const totaleImposte = irpef + additionalRegionale + additionalComunale;

            // RISULTATI FINALI
            const totaleTrattenute = contributiLavoratore + totaleImposte;
            const nettoLavoratore = compensoLordo - totaleTrattenute;
            const costoTotaleSocieta = compensoLordo + contributiSocieta;
            const taxRate = compensoLordo > 0 ? (totaleTrattenute / compensoLordo * 100) : 0;

            // AGGIORNA DISPLAY - METRICHE PRINCIPALI
            document.getElementById('display_lordo').textContent = formattaEuro(compensoLordo);
            document.getElementById('display_netto').textContent = formattaEuro(nettoLavoratore);
            document.getElementById('display_netto_mese').textContent = formattaEuro(nettoLavoratore / 12);
            document.getElementById('display_tax_rate').textContent = taxRate.toFixed(2).replace('.', ',') + '%';
            document.getElementById('display_tipo').textContent = tipoAttivita;
            document.getElementById('display_costo_societa').textContent = formattaEuro(costoTotaleSocieta);

            // DETTAGLIO CONTRIBUTIVO
            document.getElementById('contrib_lordo').textContent = formattaEuro(compensoLordo);
            document.getElementById('contrib_franchigia').textContent = formattaEuro(franchiGiaContributiva);
            document.getElementById('contrib_eccedenza').textContent = formattaEuro(baseContribGretta);
            document.getElementById('contrib_dimezzata').textContent = formattaEuro(baseContribRidotta);
            document.getElementById('contrib_aliquota').textContent = aliquotaIvs.toFixed(0) + '%';
            document.getElementById('contrib_ivs').textContent = formattaEuro(contributiIvs);
            document.getElementById('contrib_aggiuntivi').textContent = formattaEuro(contributiAggiuntivi);
            document.getElementById('contrib_totale').textContent = formattaEuro(totaleContributiInps);
            document.getElementById('contrib_lavoratore').textContent = formattaEuro(contributiLavoratore);
            document.getElementById('contrib_societa').textContent = formattaEuro(contributiSocieta);

            // MOSTRA BADGE ESENZIONE
            document.getElementById('esenz_contrib').style.display = franchiGiaContributiva > 0 ? 'block' : 'none';

            // DETTAGLIO FISCALE
            document.getElementById('fiscal_franchigia').textContent = formattaEuro(franchiGiaFiscale);
            document.getElementById('fiscal_redd_lordo').textContent = formattaEuro(redditoImponibile);
            document.getElementById('fiscal_contributi_ded').textContent = formattaEuro(contributiLavoratore);
            document.getElementById('fiscal_redd_netto').textContent = formattaEuro(redditoImponibileNetto);
            document.getElementById('fiscal_irpef').textContent = formattaEuro(irpef);
            document.getElementById('fiscal_add_reg').textContent = formattaEuro(additionalRegionale);
            document.getElementById('fiscal_add_com').textContent = formattaEuro(additionalComunale);
            document.getElementById('fiscal_totale').textContent = formattaEuro(totaleImposte);

            // MOSTRA BADGE ESENZIONE FISCALE
            document.getElementById('esenz_fiscal').style.display = franchiGiaFiscale > 0 ? 'block' : 'none';

            // RIEPILOGO FINALE
            document.getElementById('riepilogo_lordo').textContent = formattaEuro(compensoLordo);
            document.getElementById('riepilogo_contrib').textContent = formattaEuro(contributiLavoratore);
            document.getElementById('riepilogo_imposte').textContent = formattaEuro(totaleImposte);
            document.getElementById('riepilogo_netto').textContent = formattaEuro(nettoLavoratore);
            document.getElementById('riepilogo_costo_societa').textContent = formattaEuro(costoTotaleSocieta);
        }

        // Calcolo al caricamento
        calcola();
    </script>
</body>
</html>
