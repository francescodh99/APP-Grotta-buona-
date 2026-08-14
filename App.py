import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Configurazione della pagina
st.set_page_config(page_title="Gestione Diga Grotta Campanaro", page_icon="🌊", layout="centered")

st.title("🌊 Diga Grotta Campanaro")
st.subheader("Monitoraggio Bilancio Idrico")

# Inizializzazione dello storico nella sessione
if "storico" not in st.session_state:
    st.session_state.storico = []

# Mappatura apertura paratoia (cm) -> scarico Q_out (l/s)
def get_qout(cm):
    tabella_qout = {0: 0, 1: 150, 2: 300, 3: 450, 4: 600, 5: 750, 6: 900}
    return tabella_qout.get(cm, cm * 150)

# Stima dell'apertura consigliata in cm per bilanciare Q_in
def get_cm_consigliati(q_in):
    return max(0, round(q_in / 150))

# Modulo di inserimento dati
st.markdown("### 📝 Nuova Rilevazione")
col1, col2 = st.columns(2)

with col1:
    data_input = st.date_input("Data", value=datetime.now().date())
    ora_input = st.time_input("Orario rilevazione", value=datetime.now().time())
    quota_input = st.number_input("Quota Attuale (mslm)", min_value=750.00, max_value=780.00, value=766.08, step=0.01, format="%.2f")

with col2:
    paratoia_input = st.number_input("Apertura Paratoia (cm)", min_value=0, max_value=50, value=4, step=1)
    
    modalita = st.radio(
        "Modalità Operativa",
        ["Mantenimento Quota Costante", "Raggiungi Quota Target"]
    )
    
    if modalita == "Raggiungi Quota Target":
        target_input = st.number_input("Quota Target Desiderata (mslm)", min_value=750.00, max_value=780.00, value=765.00, step=0.01, format="%.2f")
    else:
        target_input = None

if st.button("➕ Registra Lettura", use_container_width=True):
    dt_misure = datetime.combine(data_input, ora_input)
    q_out = get_qout(paratoia_input)
    
    nuovo_record = {
        "DataOra": dt_misure,
        "Quota": quota_input,
        "Paratoia_cm": paratoia_input,
        "Q_out": q_out,
        "Modalita": modalita,
        "QuotaTarget": target_input if modalita == "Raggiungi Quota Target" else "-"
    }
    
    st.session_state.storico.append(nuovo_record)
    st.session_state.storico = sorted(st.session_state.storico, key=lambda x: x["DataOra"])
    st.success("Rilevazione salvata!")

# Calcoli ed elaborazione dello storico
if len(st.session_state.storico) > 0:
    df = pd.DataFrame(st.session_state.storico)
    
    if len(df) >= 2:
        rec_prev = df.iloc[-2]
        rec_curr = df.iloc[-1]
        
        dt_sec = (rec_curr["DataOra"] - rec_prev["DataOra"]).total_seconds()
        
        if dt_sec > 0:
            d_quota = rec_prev["Quota"] - rec_curr["Quota"]
            d_vol = d_quota * 10000  # m3
            
            q_svuota = (d_vol / dt_sec) * 1000  # l/s
            q_in = rec_curr["Q_out"] - q_svuota
            vel_cm_ora = (d_quota * 100) / (dt_sec / 3600)
            
            st.markdown("---")
            st.markdown("### 📊 Risultati Ultima Rilevazione")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Afflusso $Q_{in}$", f"{q_in:.1f} l/s")
            
            # Variazione di livello
            if vel_cm_ora > 0:
                m2.metric("Tendenza", f"-{vel_cm_ora:.2f} cm/h")
            elif vel_cm_ora < 0:
                m2.metric("Tendenza", f"+{abs(vel_cm_ora):.2f} cm/h")
            else:
                m2.metric("Tendenza", "Stabile")

            # Output in base alla modalità selezionata
            if rec_curr["Modalita"] == "Mantenimento Quota Costante":
                cm_suggeriti = get_cm_consigliati(q_in)
                m3.metric("Stato", "Mantenimento")
                
                if abs(vel_cm_ora) < 0.2:
                    st.success(f"⚖️ **Invaso in equilibrio!** Per proseguire il mantenimento, lascia la paratoia a circa **{cm_suggeriti} cm** ($Q_{{out}} \\approx {q_in:.0f}$ l/s).")
                elif vel_cm_ora > 0:
                    st.warning(f"📉 **Invaso in discesa (-{vel_cm_ora:.2f} cm/h):** Per stabilizzare il livello, riduci lo scarico a circa **{cm_suggeriti} cm** ($Q_{{out}} \\approx {q_in:.0f}$ l/s).")
                else:
                    st.warning(f"📈 **Invaso in salita (+{abs(vel_cm_ora):.2f} cm/h):** Per stabilizzare il livello, aumenta lo scarico a circa **{cm_suggeriti} cm** ($Q_{{out}} \\approx {q_in:.0f}$ l/s).")

            else:
                # Modalità Raggiungi Quota Target
                target_attuale = rec_curr["QuotaTarget"]
                dislivello_target = rec_curr["Quota"] - target_attuale
                vol_da_scaricare = dislivello_target * 10000
                
                if dislivello_target > 0 and d_vol > 0:
                    ore_rimaste = vol_da_scaricare / (d_vol / (dt_sec / 3600))
                    ora_target = rec_curr["DataOra"] + timedelta(hours=ore_rimaste)
                    m3.metric(f"Tempo a {target_attuale:.2f}", f"{ore_rimaste:.1f} ore")
                    st.info(f"🎯 **Quota {target_attuale:.2f} mslm prevista per:** {ora_target.strftime('%d/%m/%Y alle %H:%M')}")
                elif dislivello_target < 0 and d_vol < 0:
                    ore_rimaste = abs(vol_da_scaricare) / (abs(d_vol) / (dt_sec / 3600))
                    ora_target = rec_curr["DataOra"] + timedelta(hours=ore_rimaste)
                    m3.metric(f"Tempo a {target_attuale:.2f}", f"{ore_rimaste:.1f} ore")
                    st.info(f"🎯 **Quota {target_attuale:.2f} mslm prevista per:** {ora_target.strftime('%d/%m/%Y alle %H:%M')}")
                elif dislivello_target == 0:
                    m3.metric("Stato Target", "Raggiunto")
                    st.success(f"🎉 Quota target {target_attuale:.2f} mslm raggiunta!")
                else:
                    m3.metric("Stato Target", "Tendenza opposta")

    # Tabella Storico
    st.markdown("---")
    st.markdown("### 📜 Storico Rilevazioni")
    
    df_display = df.copy()
    df_display["Orario"] = df_display["DataOra"].dt.strftime("%d/%m %H:%M")
    df_display = df_display[["Orario", "Quota", "Paratoia_cm", "Q_out", "Modalita", "QuotaTarget"]]
    df_display.columns = ["Ora/Data", "Quota (mslm)", "Paratoia (cm)", "Scarico Q_out (l/s)", "Modalità", "Target (mslm)"]
    
    st.dataframe(df_display.iloc[::-1], use_container_width=True)

    if st.button("🗑️ Svuota Storico"):
        st.session_state.storico = []
        st.rerun()
