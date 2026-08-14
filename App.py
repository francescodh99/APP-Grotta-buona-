import datetime
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Gestione Diga Grotta Campanaro", page_icon="🌊", layout="wide"
)

st.title("🌊 Monitoraggio Bilancio Idrico — Diga Grotta Campanaro")

# ==============================================================================
# 1. TABELLE E FUNZIONI DI INTERPOLAZIONE
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
        0.7,
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
        0.7,
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
        0.7,
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

interpolatore_paratoia = RegularGridInterpolator(
    (QUOTE_PARATOIA, APERTURE_M), PORTATE_M3S, method="linear"
)


def get_volume_da_quota(quota_mslm):
  return float(np.interp(quota_mslm, QUOTE_INVASO, VOLUMI_INVASO))


def get_quota_da_volume(vol_m3):
  vol_m3 = np.clip(vol_m3, VOLUMI_INVASO[0], VOLUMI_INVASO[-1])
  return float(np.interp(vol_m3, VOLUMI_INVASO, QUOTE_INVASO))


def get_qout_ls(quota_mslm, apertura_cm):
  apertura_m = np.clip(apertura_cm / 100.0, APERTURE_M[0], APERTURE_M[-1])
  quota_mslm = np.clip(quota_mslm, QUOTE_PARATOIA[0], QUOTE_PARATOIA[-1])
  return float(interpolatore_paratoia((quota_mslm, apertura_m))) * 1000.0


def get_apertura_suggerita(quota_mslm, q_out_desiderata_ls):
  """Trova l'apertura in cm che genera la portata Qout richiesta alla quota data."""
  grid_cm = np.linspace(1.0, 90.0, 891)
  portate_grid = [get_qout_ls(quota_mslm, a) for a in grid_cm]
  return float(np.interp(q_out_desiderata_ls, portate_grid, grid_cm))


# ==============================================================================
# 2. INSERIMENTO DATI RILEVAZIONE
# ==============================================================================
st.subheader("📝 Dati della Rilevazione")

col_a, col_b, col_c = st.columns(3)

with col_a:
  data_rilevazione = st.date_input("Data", value=datetime.date.today())
  ora_rilevazione = st.time_input("Ora Rilevazione", value=datetime.time(10, 44))

with col_b:
  quota_attuale = st.number_input(
      "Quota Attuale (mslm)",
      value=766.08,
      min_value=764.00,
      max_value=783.00,
      step=0.01,
      format="%.2f",
  )
  apertura = st.number_input(
      "Apertura Paratoia (cm)",
      value=4.0,
      min_value=1.0,
      max_value=90.0,
      step=0.1,
      format="%.1f",
  )

with col_c:
  modalita = st.radio(
      "Modalità Operativa",
      ["Mantenimento Quota Costante", "Raggiungi Quota Target"],
  )
  qin_stimata = st.number_input(
      "Portata in Entrata Qin (l/s)",
      value=545.0,
      min_value=0.0,
      step=5.0,
      format="%.1f",
  )

# --- CALCOLI BASE ---
q_out_attuale = get_qout_ls(quota_attuale, apertura)
vol_attuale = get_volume_da_quota(quota_attuale)
delta_q_ls = qin_stimata - q_out_attuale  # l/s netti
delta_vol_ora_m3 = (delta_q_ls / 1000.0) * 3600.0  # m³/ora

# Calcolo Delta Quota orario
vol_ora_successiva = vol_attuale + delta_vol_ora_m3
quota_ora_successiva = get_quota_da_volume(vol_ora_successiva)
delta_quota_ora_cm = (quota_ora_successiva - quota_attuale) * 100.0

# Definizione Trend
if delta_q_ls > 5.0:
  trend_testo = f"⬆️ In Salita (+{abs(delta_quota_ora_cm):.1f} cm/h)"
  trend_color = "inverse"
elif delta_q_ls < -5.0:
  trend_testo = f"⬇️ In Discesa (-{abs(delta_quota_ora_cm):.1f} cm/h)"
  trend_color = "normal"
else:
  trend_testo = "➡️ Stabile (0.0 cm/h)"
  trend_color = "off"

st.markdown("---")

# ==============================================================================
# 3. MODALITÀ MANTENIMENTO QUOTA COSTANTE
# ==============================================================================
if modalita == "Mantenimento Quota Costante":
  st.subheader("🎯 Modalità: Mantenimento Quota Costante")

  apertura_suggerita = get_apertura_suggerita(quota_attuale, qin_stimata)

  m1, m2, m3 = st.columns(3)
  m1.metric("Portata Scaricata (Qout)", f"{q_out_attuale:.1f} l/s")
  m2.metric("Portata in Entrata (Qin)", f"{qin_stimata:.1f} l/s")
  m3.metric("Trend Quota", trend_testo)

  c1, c2 = st.columns(2)
  with c1:
    st.info(
        f"⚙️ **Apertura Suggerita per Quota Stabile:** **{apertura_suggerita:.1f} cm**\n\n"
        f"Regolando la paratoia a **{apertura_suggerita:.1f} cm**, la portata scaricata ($Q_{{out}}$) "
        f"uguaglierà la portata in entrata ($Q_{{in}} = {qin_stimata:.1f}$ l/s)."
    )
  with c2:
    st.metric(
        "Delta Quota Previsto ogni Ora",
        f"{delta_quota_ora_cm:+.1f} cm/ora",
        help="Variazione di quota calcolata con l'apertura paratoia attuale",
    )

# ==============================================================================
# 4. MODALITÀ RAGGIUNGI QUOTA TARGET
# ==============================================================================
else:
  st.subheader("🎯 Modalità: Raggiungi Quota Target")

  col_t1, col_t2 = st.columns(2)

  with col_t1:
    quota_target = st.number_input(
        "Quota Target (mslm)",
        value=765.00,
        min_value=764.00,
        max_value=783.00,
        step=0.05,
        format="%.2f",
    )

  with col_t2:
    ore_target = st.number_input(
        "In quante ore vuoi raggiungere il target?",
        value=12.0,
        min_value=0.5,
        max_value=168.0,
        step=0.5,
        format="%.1f",
    )

  # Calcoli operativi Target
  vol_target = get_volume_da_quota(quota_target)
  delta_vol_totale = vol_target - vol_attuale  # m³ da variare

  # Portata netta richiesta in l/s per raggiungere il target nel tempo specificato
  q_netta_richiesta_ls = (delta_vol_totale / (ore_target * 3600.0)) * 1000.0
  q_out_richiesta_ls = qin_stimata - q_netta_richiesta_ls

  # Calcolo apertura suggerita
  apertura_suggerita_target = get_apertura_suggerita(
      quota_attuale, max(0.0, q_out_richiesta_ls)
  )

  # Ora presunta di arrivo
  dt_rilevazione = datetime.datetime.combine(data_rilevazione, ora_rilevazione)
  ora_presunta_arrivo = dt_rilevazione + datetime.timedelta(hours=ore_target)

  # Delta quota medio ogni ora per raggiungere il target
  delta_quota_totale_cm = (quota_target - quota_attuale) * 100.0
  delta_quota_ora_target_cm = delta_quota_totale_cm / ore_target

  # Indicatori principali
  t1, t2, t3 = st.columns(3)
  t1.metric("Portata Scaricata (Qout)", f"{q_out_attuale:.1f} l/s")
  t2.metric("Portata in Entrata (Qin)", f"{qin_stimata:.1f} l/s")
  t3.metric("Trend Quota Attuale", trend_testo)

  st.markdown("---")

  r1, r2, r3 = st.columns(3)
  r1.metric(
      "Apertura Suggerita Paratoia",
      f"{apertura_suggerita_target:.1f} cm",
      delta=f"Qout req: {q_out_richiesta_ls:.1f} l/s",
  )
  r2.metric(
      "Ora Presunta Arrivo al Target",
      ora_presunta_arrivo.strftime("%H:%M (%d/%m)"),
  )
  r3.metric(
      "Delta Quota Previsto ogni Ora",
      f"{delta_quota_ora_target_cm:+.1f} cm/ora",
  )

  if q_out_richiesta_ls < 0:
    st.warning(
        "⚠️ Per raggiungere il target nel tempo impostato, l'afflusso naturale non è sufficiente "
        "nemmeno chiudendo completamente la paratoia (Qout = 0 l/s)."
    )
  elif q_out_richiesta_ls > 20000:
    st.error(
        "⚠️ Portata di scarico richiesta superiore alla capacità massima della paratoia."
    )
