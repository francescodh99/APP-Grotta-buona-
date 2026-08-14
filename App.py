import datetime
import numpy as np
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Gestione Diga Grotta Campanaro", page_icon="🌊"
)

st.title("Monitoraggio Bilancio Idrico")
st.caption("Diga Grotta Campanaro — Controllo Invaso e Scarichi")

# --- TABELLE DI INTERPOLAZIONE (Valori di esempio modificabili) ---
# Quota mslm -> Volume m³
QUOTE_TABELLA = [764.00, 765.00, 766.00, 767.00]
VOLUMI_TABELLA = [0.0, 100000.0, 200000.0, 350000.0]

# Apertura paratoia cm -> Portata scaricata Qout l/s
APERTURE_TABELLA = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0]
PORTATE_TABELLA = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 1000.0]


def get_volume(quota):
  """Calcola il volume interpolando la scala d'invaso."""
  return float(np.interp(quota, QUOTE_TABELLA, VOLUMI_TABELLA))


def get_qout(apertura_cm):
  """Calcola la Qout interpolando la tabella della paratoia."""
  return float(np.interp(apertura_cm, APERTURE_TABELLA, PORTATE_TABELLA))


# --- SEZIONE: NUOVA RILEVAZIONE (UNICO FORM INPUT) ---
st.subheader("📝 Nuova Rilevazione")

col1, col2 = st.columns(2)

with col1:
  data_rilevazione = st.date_input("Data", value=datetime.date.today())
  ora_rilevazione = st.time_input(
      "Orario rilevazione", value=datetime.datetime.now().time()
  )
  quota_attuale = st.number_input(
      "Quota Attuale (mslm)",
      value=766.08,
      min_value=700.00,
      max_value=800.00,
      step=0.01,
      format="%.2f",
  )

with col2:
  # UNICO CAMPO PARATOIA (Supporta decimali come 4.1, 4.2 cm)
  apertura = st.number_input(
      "Apertura Paratoia (cm)",
      value=4.0,
      min_value=0.0,
      max_value=50.0,
      step=0.1,
      format="%.1f",
  )

  modalita = st.radio(
      "Modalità Operativa",
      ["Mantenimento Quota Costante", "Raggiungi Quota Target"],
  )

# --- CALCOLI IN TEMPO REALE ---
q_out = get_qout(apertura)
vol_attuale = get_volume(quota_attuale)
quota_target = 765.00
vol_target = get_volume(quota_target)

st.markdown("---")
st.subheader("📊 Calcoli e Stato Invaso")

col_a, col_b, col_c = st.columns(3)
col_a.metric(label="Portata Scaricata (Qout)", value=f"{q_out:.1f} l/s")
col_b.metric(label="Volume Attuale Stimato", value=f"{vol_attuale:,.0f} m³")
col_c.metric(label="Quota Target", value=f"{quota_target:.2f} mslm")

# Indicazioni operative per la quota target
delta_vol = vol_attuale - vol_target

if modalita == "Raggiungi Quota Target":
  if delta_vol > 0:
    st.info(
        f"Volume rimanente da scaricare per il target ({quota_target:.2f}"
        f" mslm): **{delta_vol:,.0f} m³**"
    )
  elif delta_vol == 0:
    st.success("Quota target raggiunta!")
  else:
    st.warning("La quota attuale è inferiore alla quota target.")

# Pulsante per registrare il dato
if st.button("➕ Registra Lettura", use_container_width=True):
  st.success(
      f"Rilevazione salvata: Quota {quota_attuale:.2f} mslm | Paratoia"
      f" {apertura:.1f} cm ({q_out:.1f} l/s)"
  )
