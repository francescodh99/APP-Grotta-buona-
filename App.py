import datetime
import numpy as np
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Gestione Diga Grotta Campanaro", page_icon="🌊", layout="wide"
)

st.title("🌊 Monitoraggio Bilancio Idrico — Diga Grotta Campanaro")
st.caption("Sistema integrato di calcolo invaso e scarichi da tabelle ufficiali")

# ==============================================================================
# 1. TABELLA SCALA D'INVASO (GROTTA CAMPANARO)
# ==============================================================================
QUOTE_INVASO = np.array([
    764.00,
    765.00,
    766.00,
    767.00,
    768.00,
    768.90,
    769.00,
    770.00,
    771.00,
    772.00,
    773.00,
    774.00,
    774.80,
    775.00,
    776.00,
    777.00,
    778.00,
    779.00,
    780.00,
    780.80,
    781.00,
    782.00,
    783.00,
])

VOLUMI_INVASO = np.array([
    0,
    15000,
    38000,
    68000,
    105000,
    137000,
    141000,
    183000,
    228000,
    277000,
    331000,
    389000,
    438000,
    451000,
    518000,
    590000,
    667000,
    749000,
    836000,
    910000,
    929000,
    1027000,
    1130000,
])


def get_volume_da_quota(quota_mslm):
  """Interpolazione della scala d'invaso per ottenere il volume in m³."""
  return float(np.interp(quota_mslm, QUOTE_INVASO, VOLUMI_INVASO))


# ==============================================================================
# 2. TABELLA SCARICO PARATOIA DI FONDO
# ==============================================================================
APERTURE_M = np.array([
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
])

QUOTE_PARATOIA = np.array([
    764.00,
    764.50,
    765.00,
    765.50,
    766.00,
    767.00,
    768.00,
    769.00,
    770.00,
    771.00,
    772.00,
    773.00,
    774.00,
    775.00,
    776.00,
    777.00,
    778.00,
    779.00,
    780.00,
    781.00,
    782.00,
    783.00,
    784.00,
    785.00,
])

PORTATE_M3S = np.array([
    [
        0.2,
        0.3,
        0.5,
        0.6,
        0.8,
        0.9,
        1.1,
        1.2,
        1.4,
        1.5,
        3.0,
        4.5,
        6.1,
        7.6,
        9.1,
        10.6,
        12.2,
        13.7,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.6,
        0.8,
        0.9,
        1.1,
        1.2,
        1.4,
        1.5,
        3.1,
        4.6,
        6.1,
        7.7,
        9.2,
        10.8,
        12.3,
        13.9,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.6,
        0.8,
        0.9,
        1.1,
        1.2,
        1.4,
        1.5,
        3.1,
        4.7,
        6.2,
        7.8,
        9.4,
        10.9,
        12.5,
        14.1,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.6,
        0.8,
        0.9,
        1.1,
        1.3,
        1.4,
        1.6,
        3.1,
        4.7,
        6.3,
        7.9,
        9.5,
        11.1,
        12.7,
        14.3,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.6,
        0.8,
        0.9,
        1.1,
        1.3,
        1.4,
        1.6,
        3.2,
        4.8,
        6.4,
        8.0,
        9.6,
        11.2,
        12.8,
        14.5,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.7,
        0.8,
        1.0,
        1.1,
        1.3,
        1.5,
        1.6,
        3.3,
        4.9,
        6.5,
        8.2,
        9.8,
        11.5,
        13.1,
        14.8,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.7,
        0.8,
        1.0,
        1.2,
        1.3,
        1.5,
        1.7,
        3.3,
        5.0,
        6.7,
        8.3,
        10.0,
        11.7,
        13.4,
        15.1,
    ],
    [
        0.2,
        0.3,
        0.5,
        0.7,
        0.9,
        1.0,
        1.2,
        1.4,
        1.5,
        1.7,
        3.4,
        5.1,
        6.8,
        8.5,
        10.2,
        11.9,
        13.6,
        15.3,
    ],
    [
        0.2,
        0.4,
        0.5,
        0.7,
        0.9,
        1.1,
        1.2,
        1.4,
        1.6,
        1.8,
        3.5,
        5.2,
        7.0,
        8.7,
        10.5,
        12.2,
        14.0,
        15.7,
    ],
    [
        0.2,
        0.4,
        0.5,
        0.7,
        0.9,
        1.1,
        1.3,
        1.4,
        1.6,
        1.8,
        3.6,
        5.3,
        7.1,
        8.9,
        10.7,
        12.5,
        14.3,
        16.1,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.7,
        0.9,
        1.1,
        1.3,
        1.5,
        1.6,
        1.8,
        3.6,
        5.4,
        7.2,
        9.1,
        10.9,
        12.8,
        14.6,
        16.4,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.7,
        0.9,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        3.7,
        5.5,
        7.3,
        9.2,
        11.0,
        12.9,
        14.7,
        16.6,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        0.9,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        3.8,
        5.6,
        7.5,
        9.4,
        11.3,
        13.2,
        15.1,
        17.0,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        3.8,
        5.7,
        7.6,
        9.5,
        11.4,
        13.4,
        15.3,
        17.2,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.0,
        3.9,
        5.8,
        7.8,
        9.8,
        11.7,
        13.7,
        15.7,
        17.6,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.0,
        4.0,
        5.9,
        7.9,
        9.9,
        11.8,
        13.8,
        15.8,
        17.8,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.0,
        4.0,
        6.0,
        8.0,
        10.0,
        12.0,
        14.0,
        16.1,
        18.1,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.1,
        4.1,
        6.1,
        8.1,
        10.2,
        12.2,
        14.3,
        16.3,
        18.4,
    ],
    [
        0.2,
        0.4,
        0.6,
        0.8,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        2.1,
        4.2,
        6.3,
        8.4,
        10.5,
        12.6,
        14.7,
        16.8,
        18.9,
    ],
    [
        0.2,
        0.4,
        0.7,
        0.9,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        2.2,
        4.3,
        6.5,
        8.6,
        10.8,
        13.0,
        15.1,
        17.3,
        19.4,
    ],
    [
        0.2,
        0.4,
        0.7,
        0.9,
        1.1,
        1.3,
        1.5,
        1.7,
        1.9,
        2.2,
        4.4,
        6.6,
        8.8,
        11.0,
        13.2,
        15.4,
        17.7,
        19.9,
    ],
    [
        0.2,
        0.4,
        0.4,
        0.9,
        1.1,
        1.3,
        1.5,
        1.8,
        2.0,
        2.2,
        4.4,
        6.6,
        8.9,
        11.1,
        13.3,
        15.5,
        17.8,
        20.0,
    ],
    [
        0.2,
        0.4,
        0.4,
        0.9,
        1.1,
        1.3,
        1.5,
        1.8,
        2.0,
        2.2,
        4.4,
        6.6,
        8.9,
        11.1,
        13.3,
        15.5,
        17.8,
        20.0,
    ],
    [
        0.2,
        0.4,
        0.4,
        0.9,
        1.1,
        1.3,
        1.5,
        1.8,
        2.0,
        2.2,
        4.4,
        6.6,
        8.9,
        11.1,
        13.3,
        15.5,
        17.8,
        20.0,
    ],
])


def get_qout_ls(quota_mslm, apertura_cm):
  """Interpolazione bilineare con NumPy per calcolare la portata scaricata in l/s."""
  apertura_m = apertura_cm / 100.0
  apertura_m = np.clip(apertura_m, APERTURE_M[0], APERTURE_M[-1])
  quota_mslm = np.clip(quota_mslm, QUOTE_PARATOIA[0], QUOTE_PARATOIA[-1])

  idx = np.searchsorted(QUOTE_PARATOIA, quota_mslm)
  if idx == 0:
    q_m3s = np.interp(apertura_m, APERTURE_M, PORTATE_M3S[0])
  elif idx == len(QUOTE_PARATOIA):
    q_m3s = np.interp(apertura_m, APERTURE_M, PORTATE_M3S[-1])
  else:
    q0, q1 = QUOTE_PARATOIA[idx - 1], QUOTE_PARATOIA[idx]
    v0 = np.interp(apertura_m, APERTURE_M, PORTATE_M3S[idx - 1])
    v1 = np.interp(apertura_m, APERTURE_M, PORTATE_M3S[idx])
    t = (quota_mslm - q0) / (q1 - q0) if q1 != q0 else 0
    q_m3s = v0 + t * (v1 - v0)

  return float(q_m3s * 1000.0)


# ==============================================================================
# 3. INTERFACCIA UTENTE STREAMLIT
# ==============================================================================
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
      min_value=764.00,
      max_value=785.00,
      step=0.01,
      format="%.2f",
  )

  # NUOVO CAMPO: Portata Entrante Qin
  q_in_ls = st.number_input(
      "Portata in Entrata Qin (l/s)",
      value=545.0,
      min_value=0.0,
      max_value=50000.0,
      step=5.0,
      format="%.1f",
  )

with col2:
  apertura = st.number_input(
      "Apertura Paratoia (cm)",
      value=4.0,
      min_value=1.0,
      max_value=90.0,
      step=0.1,
      format="%.1f",
  )

  modalita = st.radio(
      "Modalità Operativa",
      ["Mantenimento Quota Costante", "Raggiungi Quota Target"],
  )

# --- CALCOLI IN TEMPO REALE ---
q_out_ls = get_qout_ls(quota_attuale, apertura)
vol_attuale = get_volume_da_quota(quota_attuale)
quota_target = 765.00
vol_target = get_volume_da_quota(quota_target)
bilancio_delta_q = q_in_ls - q_out_ls

st.markdown("---")
st.subheader("📊 Calcoli e Bilancio Idrico")

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    label="Portata Entrante (Qin)",
    value=f"{q_in_ls:.1f} l/s",
    delta=f"{q_in_ls/1000:.3f} m³/s",
)
c2.metric(
    label="Portata Scaricata (Qout)",
    value=f"{q_out_ls:.1f} l/s",
    delta=f"{q_out_ls/1000:.3f} m³/s",
)
c3.metric(
    label="Bilancio Netto (ΔQ)",
    value=f"{bilancio_delta_q:+.1f} l/s",
    delta_color="normal",
)
c4.metric(label="Volume Attuale Stimato", value=f"{vol_attuale:,.0f} m³")

# --- INDICAZIONI OPERATIVE IN BASE ALLA MODALITÀ ---
if modalita == "Mantenimento Quota Costante":
  st.markdown("#### 🎯 Analisi Mantenimento Quota")
  if abs(bilancio_delta_q) < 1.0:
    st.success(
        "**Invaso in perfetto equilibrio.** La portata scaricata eguaglia la"
        " portata in entrata. La quota rimarrà costante."
    )
  elif bilancio_delta_q > 0:
    st.warning(
        f"**Invaso in riempimento (+{bilancio_delta_q:.1f} l/s).** Per"
        f" mantenere la quota attuale ({quota_attuale:.2f} mslm), la"
        " paratoia dovrebbe scaricare **"
        f"{q_in_ls:.1f} l/s**."
    )
  else:
    st.info(
        f"**Invaso in svaso ({bilancio_delta_q:.1f} l/s).** La paratoia sta"
        " scaricando più di quanto entra. Per mantenere la quota attuale,"
        f" ridurre lo scarico a **{q_in_ls:.1f} l/s**."
    )

elif modalita == "Raggiungi Quota Target":
  st.markdown("#### 🎯 Analisi Raggiungimento Target")
  delta_vol = vol_attuale - vol_target
  if delta_vol > 0:
    st.info(
        f"Volume rimanente da scaricare per la quota target ({quota_target:.2f}"
        f" mslm): **{delta_vol:,.0f} m³**"
    )
  elif delta_vol == 0:
    st.success("Quota target raggiunta!")
  else:
    st.warning("La quota attuale è inferiore alla quota target.")

if st.button("➕ Registra Lettura", use_container_width=True):
  st.success(
      f"Registrato: Quota {quota_attuale:.2f} mslm | Qin: {q_in_ls:.1f} l/s |"
      f" Paratoia {apertura:.1f} cm (Qout: {q_out_ls:.1f} l/s)"
  )
