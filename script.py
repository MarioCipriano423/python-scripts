import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Cargar datos
with open("jan.json", "r") as f:
    data = json.load(f)

# Transformar datos a DataFrame
cirugias = []
for fecha, eventos in data.items():
    for ev in eventos:
        inicio = datetime.fromisoformat(ev["inicio"])
        fin = datetime.fromisoformat(ev["fin"])
        duracion_min = (fin - inicio).total_seconds() / 60
        cirugias.append({
            "fecha": inicio.date(),
            "duracion_min": duracion_min
        })

df = pd.DataFrame(cirugias)
df["dia_mes"] = df["fecha"].apply(lambda x: x.day)
df["duracion_hr"] = df["duracion_min"] / 60

# Agrupación por día
grupo = df.groupby("dia_mes")
cantidades = grupo.size()
promedios = grupo["duracion_hr"].mean()
desvios = grupo["duracion_hr"].std()

# Crear figura con dos subgráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# ----------------------
# Gráfica 1: Cantidad de cirugías por día
# ----------------------
ax1.bar(cantidades.index, cantidades.values, color='pink', label="Cantidad diaria")
promedio_mes = round(cantidades.mean())
ax1.axhline(promedio_mes, color='red', linestyle='--', label=f'Promedio mensual: {promedio_mes:.2f} Cx')
ax1.set_ylabel("Cx")
ax1.set_title("Cantidad de cirugías por día")
ax1.legend()
ax1.grid(axis='y', linestyle=':', alpha=0.6)

# ----------------------
# Gráfica 2: Duración promedio con barras de error
# ----------------------
ax2.errorbar(promedios.index, promedios.values, yerr=desvios.values,
             fmt='o-', ecolor='pink', capsize=5, color='deepskyblue',
             label="Promedio con dispersión")
promedio_mes = round(promedios.mean())
ax2.axhline(promedio_mes, color='red', linestyle='--', label=f'Promedio mensual: {promedio_mes:.2f} hrs')
ax2.set_ylabel("Duración (hrs)")
ax2.set_xlabel("[día]")
ax2.set_title("Duración promedio por día")
ax2.legend()
ax2.grid(axis='y', linestyle=':', alpha=0.6)

dias_presentes = sorted(df["dia_mes"].unique())
ax1.set_xticks(dias_presentes)
ax1.set_xticklabels(dias_presentes)
ax2.set_xticks(dias_presentes)
ax2.set_xticklabels(dias_presentes)

# Ajustar y guardar
plt.tight_layout()
plt.savefig("resumen_enero.png")
plt.close()
