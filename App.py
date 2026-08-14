# ==============================================================================
# 5. CALCOLO AUTOMATICO E STABILIZZATO PORTATA IN ENTRATA (Qin)
# ==============================================================================
st.markdown("---")
st.subheader("💧 Calcolo Automatico Portata in Entrata ($Q_{in}$)")

q_out_ls = get_qout_ls(quota_attuale, apertura)
vol_attuale = get_volume_da_quota(quota_attuale)

use_manual_prev = st.checkbox(
    "Inserisci manualmente i dati della lettura precedente per calcolare Qin",
    value=not bool(st.session_state.storico),
)

q_in_raw = 0.0
delta_t_ore = 0.0

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
        min_value=0.1,
        max_value=168.0,
        step=0.5,
        format="%.2f",
    )

  vol_prev = get_volume_da_quota(quota_prev)
  delta_vol = vol_attuale - vol_prev
  delta_t_sec = ore_trascorse * 3600.0
  delta_t_ore = ore_trascorse
  q_in_raw = max(0.0, (delta_vol / delta_t_sec) * 1000.0 + q_out_ls)

else:
  ultima_lettura = st.session_state.storico[-1]
  str_dt_prev = f"{ultima_lettura['Data']} {ultima_lettura['Ora']}"
  try:
    dt_prev = datetime.datetime.strptime(str_dt_prev, "%Y-%m-%d %H:%M:%S")
  except ValueError:
    dt_prev = datetime.datetime.combine(data_rilevazione, ora_rilevazione)

  dt_curr = datetime.datetime.combine(data_rilevazione, ora_rilevazione)
  delta_t_sec = (dt_curr - dt_prev).total_seconds()
  delta_t_ore = delta_t_sec / 3600.0

  if delta_t_sec > 0:
    vol_prev = ultima_lettura["Volume (m³)"]
    q_out_prev = ultima_lettura["Qout (l/s)"]
    q_out_medio = (q_out_ls + q_out_prev) / 2.0
    delta_vol = vol_attuale - vol_prev
    q_in_raw = max(0.0, (delta_vol / delta_t_sec) * 1000.0 + q_out_medio)
  else:
    q_in_raw = q_out_ls

# --- FILTRAGGIO MEDIA MOBILE PER EVITARE VALORI IRREALI ---
if st.session_state.storico and not use_manual_prev:
  # Estrae le ultime letture di Qin per calcolare la media mobile
  qin_history = [
      item["Qin (l/s)"]
      for item in st.session_state.storico[-3:]
      if "Qin (l/s)" in item
  ]
  qin_history.append(q_in_raw)
  q_in_ls = float(np.mean(qin_history))
else:
  q_in_ls = q_in_raw

# Avvisi di affidabilità idraulica
if delta_t_ore < 0.5 and delta_t_ore > 0:
  st.warning(
      f"⚠️ Intervallo temporale ridotto ({delta_t_ore*60:.0f} min). Piccole"
      " variazioni di quota possono generare fluttuazioni elevate su Qin."
  )

st.info(
    f"🌊 **Portata in Entrata Stabile ($Q_{{in}}$): {q_in_ls:.1f} l/s** "
    f"(Istogramma istantaneo: {q_in_raw:.1f} l/s | $\Delta t$: {delta_t_ore:.2f} h)"
)
