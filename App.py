import datetime
import numpy as np
import pandas as pd
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Gestione Diga Grotta Campanaro", page_icon="🌊", layout="wide"
)

st.title("🌊 Monitoraggio Bilancio Idrico — Diga Grotta Campanaro")
st.caption("Sistema integrato di calcolo invaso, scarichi e bilancio idrico")

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
  """Calcola la portata scaricata (l/s) in base a quota e apertura."""
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


def get_apertura_consigliata_cm(quota_mslm, q_target_ls):
  """Calcola i centimetri di apertura necessari per scaricare esattamente la Qin."""
  q_target_m3s = q_target_ls / 1000.0
  quota_mslm = np.clip(quota_mslm, QUOTE_PARATOIA[0], QUOTE_PARATOIA[-1])

  idx = np.searchsorted(QUOTE_PARATOIA, quota_mslm)
  if idx == 0:
    q_array = PORTATE_M3S[0]
  elif idx == len(QUOTE_PARATOIA):
    q_array = PORTATE_M3S[-1]
  else:
    q0, q1 = QUOTE_PARATOIA[idx - 1], QUOTE_PARATOIA[idx]
    t = (quota_mslm - q0) / (q1 - q0) if q1 != q0 else 0
    q_array = PORTATE_M3S[idx - 1] + t * (PORTATE_M3S[idx] - PORTATE_M3S[idx - 1])

  apertura_m = np.interp(q_target_m3s, q_array, APERTURE_M)
  return (
      float(apertura_m * 100.0),
      float(q_array[0] * 1000.0),
      float(q_array[-1] * 1000.0),
  )


# ==============================================================================
# 3. STATO SESSIONE (STORICO)
# ==============================================================================
if "storico" not in st.session_state:
  st.session_state.storico = []

# ==============================================================================
# 4. INTERFACCIA UTENTE
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

  # MODIFICA 2: Quota Target impostabile liberamente dall'utente
  quota_target = st.number_input(
      "Quota Target (mslm)",
      value=765.00,
      min_value=764.00,
      max_value=785.00,
      step=0.01,
      format="%.2f",
  )

with col2:
  apertura = st.number_input(
      "Apertura Paratoia Impostata (cm)",
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

# ==============================================================================
# 5. MODIFICA 1: CALCOLO AUTOMATICO PORTATA IN ENTRATA (Qin)
# ==============================================================================
st.markdown("---")
st.subheader("💧 Calcolo Automatico Portata in Entrata ($Q_{in}$)")

q_out_ls = get_qout_ls(quota_attuale, apertura)
vol_attuale = get_volume_da_quota(quota_attuale)

use_manual_prev = st.checkbox(
    "Inserisci manualmente i dati della lettura precedente per calcolare Qin",
    value=not bool(st.session_state.storico),
)

if use_manual_prev or not st.session_state.storico:
  col_p1, col_p2 = st.columns(2)
  with col_p1:
    quota_prev = st.number_input(
        "Quota Precedente (mslm)",
        value=quota_attuale,
        min_value=764.00,
        max_value=785.00,
        step=0.01,
        format="%.2f",
    )
  with col_p2:
    ore_trascorse = st.number_input(
        "Ore trascorse dalla rilevazione precedente",
        value=1.0,
        min_value=0.01,
        max_value=168.0,
        step=0.5,
        format="%.2f",
    )

  vol_prev = get_volume_da_quota(quota_prev)
  delta_vol = vol_attuale - vol_prev  # in m³
  delta_t_sec = ore_trascorse * 3600.0
  # Qin = (dV / dt in m³/s * 1000) + Qout
  q_in_ls = max(0.0, (delta_vol / delta_t_sec) * 1000.0 + q_out_ls)

else:
  ultima_lettura = st.session_state.storico[-1]
  str_dt_prev = f"{ultima_lettura['Data']} {ultima_lettura['Ora']}"
  try:
    dt_prev = datetime.datetime.strptime(str_dt_prev, "%Y-%m-%d %H:%M:%S")
  except ValueError:
    dt_prev = datetime.datetime.combine(data_rilevazione, ora_rilevazione)

  dt_curr = datetime.datetime.combine(data_rilevazione, ora_rilevazione)
  delta_t_sec = (dt_curr - dt_prev).total_seconds()

  if delta_t_sec > 0:
    vol_prev = ultima_lettura["Volume (m³)"]
    q_out_prev = ultima_lettura["Qout (l/s)"]
    q_out_medio = (q_out_ls + q_out_prev) / 2.0
    delta_vol = vol_attuale - vol_prev
    q_in_ls = max(0.0, (delta_vol / delta_t_sec) * 1000.0 + q_out_medio)
  else:
    q_in_ls = q_out_ls

st.info(
    f"🌊 **Portata in Entrata Calcolata ($Q_{{in}}$): {q_in_ls:.1f} l/s** "
    f"(stimata in base alla variazione del volume e lo scarico nel tempo)."
)

# ==============================================================================
# 6. BILANCIO IDRICO E SUGGERIMENTI OPERATIVI
# ==============================================================================
vol_target = get_volume_da_quota(quota_target)
bilancio_delta_q = q_in_ls - q_out_ls

st.markdown("---")
st.subheader("📊 Bilancio e Suggerimenti Operativi")

c1, c2, c3, c4 = st.columns(4)
c1.metric(label="Portata Entrante (Qin Calcolata)", value=f"{q_in_ls:.1f} l/s")
c2.metric(label="Portata Scaricata (Qout)", value=f"{q_out_ls:.1f} l/s")
c3.metric(label="Bilancio Netto (ΔQ)", value=f"{bilancio_delta_q:+.1f} l/s")
c4.metric(label="Volume Attuale", value=f"{vol_attuale:,.0f} m³")

if modalita == "Mantenimento Quota Costante":
  apertura_rec_cm, min_q, max_q = get_apertura_consigliata_cm(
      quota_attuale, q_in_ls
  )

  st.markdown("#### 🎯 Suggerimento Paratoia per Mantenimento Quota")
  if q_in_ls < min_q:
    st.error(
        f"La portata in entrata ({q_in_ls:.1f} l/s) è inferiore alla portata"
        f" minima di scarico ({min_q:.1f} l/s) alla quota attuale."
    )
  elif q_in_ls > max_q:
    st.error(
        f"La portata in entrata ({q_in_ls:.1f} l/s) supera la capacità massima"
        f" della paratoia ({max_q:.1f} l/s) alla quota attuale."
    )
  else:
    st.success(
        f"👉 Per mantenere la quota costante a **{quota_attuale:.2f} mslm** con"
        f" un'affluenza calcolata di **{q_in_ls:.1f} l/s**, imposta la paratoia"
        f" a **{apertura_rec_cm:.1f} cm**."
    )

  if abs(apertura - apertura_rec_cm) > 0.1:
    delta_cm = apertura_rec_cm - apertura
    azione = "aumentare" if delta_cm > 0 else "ridurre"
    st.info(
        f"Differenza rispetto all'impostazione attuale ({apertura:.1f} cm):"
        f" {azione} di **{abs(delta_cm):.1f} cm**."
    )

elif modalita == "Raggiungi Quota Target":
  st.markdown("#### ⏱️ Stima Tempi di Raggiungimento Target")
  delta_vol = vol_attuale - vol_target
  net_flow_m3s = (q_out_ls - q_in_ls) / 1000.0

  if delta_vol > 0:  # Svaso
    st.write(
        f"Volume da svasare per raggiungere la quota target ({quota_target:.2f}"
        f" mslm): **{delta_vol:,.0f} m³**"
    )
    if net_flow_m3s <= 0:
      st.error(
          "⚠️ Qout è inferiore o uguale a Qin. L'invaso non si sta svasando:"
          " aumenta l'apertura della paratoia."
      )
    else:
      time_sec = delta_vol / net_flow_m3s
      hours = int(time_sec // 3600)
      minutes = int((time_sec % 3600) // 60)
      st.success(
          f"⏱️ Tempo stimato di svaso: **{hours} ore e {minutes} minuti** (a"
          " portata e afflusso costanti)."
      )

  elif delta_vol < 0:  # Riempimento
    st.write(
        f"Volume da accumulare per raggiungere la quota target"
        f" ({quota_target:.2f} mslm): **{abs(delta_vol):,.0f} m³**"
    )
    if net_flow_m3s >= 0:
      st.error(
          "⚠️ Qout è superiore o uguale a Qin. L'invaso non si sta riempendo:"
          " riduci l'apertura della paratoia."
      )
    else:
      time_sec = abs(delta_vol) / abs(net_flow_m3s)
      hours = int(time_sec // 3600)
      minutes = int((time_sec % 3600) // 60)
      st.success(
          f"⏱️ Tempo stimato di riempimento: **{hours} ore e {minutes} minuti**"
          " (a portata e afflusso costanti)."
      )
  else:
    st.success("La quota attuale coincide già con la quota target.")

# --- REGISTRAZIONE LETTURA ---
if st.button("➕ Registra Lettura nello Storico", use_container_width=True):
  ora_formatted = ora_rilevazione.strftime("%H:%M:%S")
  nuova_lettura = {
      "Data": str(data_rilevazione),
      "Ora": ora_formatted,
      "Quota (mslm)": quota_attuale,
      "Qin (l/s)": round(q_in_ls, 1),
      "Apertura (cm)": apertura,
      "Qout (l/s)": round(q_out_ls, 1),
      "ΔQ (l/s)": round(bilancio_delta_q, 1),
      "Volume (m³)": vol_attuale,
      "Modalità": modalita,
  }
  st.session_state.storico.append(nuova_lettura)
  st.success("Lettura registrata con successo!")

# --- SEZIONE GRAFICO E STORICO ---
st.markdown("---")
col_g1, col_g2 = st.columns([1, 1])

with col_g1:
  st.subheader("📈 Curva di Invaso (Grotta Campanaro)")
  df_curve = pd.DataFrame(
      {"Quota (mslm)": QUOTE_INVASO, "Volume (m³)": VOLUMI_INVASO}
  )
  st.line_chart(df_curve, x="Quota (mslm)", y="Volume (m³)", color="#0083B0")

with col_g2:
  st.subheader("📋 Storico Rilevazioni")
  if st.session_state.storico:
    df_hist = pd.DataFrame(st.session_state.storico)
    st.dataframe(df_hist, use_container_width=True)

    csv_data = df_hist.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Scarica Report CSV",
        data=csv_data,
        file_name=f"report_diga_{datetime.date.today()}.csv",
        mime="text/csv",
        use_container_width=True,
    )
  else:
    st.info("Nessuna rilevazione salvata nella sessione corrente.")
