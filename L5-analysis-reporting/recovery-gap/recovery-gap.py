import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)

# --- PARAMETRI ---
t_total_minutes = 15
sample_interval = 5  # secondi
n_samples = t_total_minutes * 60 // sample_interval

time = pd.date_range(start="10:00:00", periods=n_samples, freq=f"{sample_interval}s")

# --- EVENTI CHIAVE ---
fault_idx = n_samples // 4
restart_duration_seconds = 90  # durata del restart pod
restore_duration_seconds = 180  # durata del restore dati

T0 = time[fault_idx]  # Fault
T_restart_end = T0 + pd.Timedelta(seconds=restart_duration_seconds)  # Fine restart pod
T2 = T_restart_end + pd.Timedelta(seconds=restore_duration_seconds)  # Fine restore dati
T_bia = T0 + pd.Timedelta(minutes=2)  # soglia BIA

# --- AVAILABILITY DEL PROCESSO CRITICO ---
availability_data = np.ones(n_samples)
# resta 0 fino al completamento del restore (T2)
availability_data[fault_idx:np.searchsorted(time, T2)] = 0

# --- PLOT ---
fig, ax = plt.subplots(figsize=(13, 5))

# Availability effettiva
ax.step(time, availability_data, where="post", linewidth=2, label="Availability processo critico")

# Linee verticali
ax.axvline(T0, color="black", linestyle=":", linewidth=2, label="T0 – Fault")
ax.axvline(T_bia, color="red", linestyle="--", linewidth=2, label="Soglia BIA")
ax.axvline(T_restart_end, color="blue", linestyle=":", linewidth=2, label="Fine restart pod")
ax.axvline(T2, color="green", linestyle=":", linewidth=2, label="Restore completato")

# Aree colorate per le fasi
ax.axvspan(T0, T_restart_end, color="orange", alpha=0.15, label="Restart pod (self-healing)")
ax.axvspan(T_restart_end, T2, color="purple", alpha=0.15, label="Restore DB")

# Annotazioni temporali con frecce
ax.annotate("", xy=(T_bia, 0.2), xytext=(T0, 0.2), arrowprops=dict(arrowstyle="<->"))
#ax.text(T0 + (T_bia-T0)/2, 0.25, "Tempo massimo accettabile\n(T_bia − T0)", ha="center")

ax.annotate("", xy=(T2, 0.4), xytext=(T_bia, 0.4), arrowprops=dict(arrowstyle="<->"))
ax.text(T_bia + (T2-T_bia)/2, 0.45, "Recovery gap\n(T2 − T_bia)", ha="center")

# Etichette sotto l'asse
y_pos_labels = -0.10
#y_pos_
ax.text(T0, y_pos_labels, "T0", ha="center", va="top", fontsize=10, fontweight='bold')
ax.text(T_bia, y_pos_labels, "T_bia", ha="center", va="top", fontsize=10, color="red")
#ax.text(T_restart_end, y_pos_labels, "Fine restart\npod", ha="center", va="top", fontsize=10, color="blue")
ax.text(T2, y_pos_labels, "T2", ha="center", va="top", fontsize=10, color="green")

# Assi e titolo
ax.set_ylim(-0.1, 1.1)
ax.set_yticks([0, 1])
ax.set_yticklabels(["Unavailable", "Available"])
ax.set_xlabel("Tempo", labelpad=40)
ax.set_ylabel("Stato del servizio")
ax.set_title("Recovery Timeline – TC-02 (Restart pod + Restore DB)")

# Legenda fuori dal plot
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, fontsize=10)
#ax.legend(loc='lower right', bbox_to_anchor=(1, 0), frameon=True, fontsize=10)
ax.legend(
    loc='lower right', 
    bbox_to_anchor=(1.25, 0), # 1.25 spinge la legenda molto a destra
    frameon=True, 
    fontsize=10
)

# Regoliamo i margini per assicurarci che ci sia spazio a destra e in basso
plt.subplots_adjust(bottom=0.25, right=0.80)
plt.show()
