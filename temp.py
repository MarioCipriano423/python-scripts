from datetime import datetime, timedelta
import json

def pedir_horas_para_dia(fecha_actual_str):
    fecha_actual = datetime.strptime(fecha_actual_str, "%Y-%m-%d")
    print(f"\n🗓️ Ingresando cirugías para el día {fecha_actual_str} (formato 24h)")

    while True:
        entrada_inicio = input(" → Hora de *inicio* (HH:MM) o 'cambiar' para otra fecha, 'fin' para terminar: ").strip().lower()
        if entrada_inicio == "fin":
            return False
        elif entrada_inicio == "cambiar":
            return True

        entrada_fin = input(" → Hora de *fin* (HH:MM): ").strip()

        try:
            hora_inicio = datetime.strptime(entrada_inicio, "%H:%M").time()
            hora_fin = datetime.strptime(entrada_fin, "%H:%M").time()

            dt_inicio = datetime.combine(fecha_actual.date(), hora_inicio)
            dt_fin = datetime.combine(fecha_actual.date(), hora_fin)

            if dt_fin <= dt_inicio:
                print("❌ La hora de fin debe ser posterior a la de inicio.")
                continue

            fecha_str = fecha_actual_str
            if fecha_str not in calendario:
                calendario[fecha_str] = []

            calendario[fecha_str].append({
                "inicio": dt_inicio.isoformat(),
                "fin": dt_fin.isoformat()
            })
            print(f"✔️ Agregado: {dt_inicio.strftime('%H:%M')} → {dt_fin.strftime('%H:%M')}")
        except ValueError:
            print("❌ Formato incorrecto. Usa HH:MM (ej. 08:30 o 14:15)")

def guardar_json(nombre_archivo="calendario_cirugias.json"):
    with open(nombre_archivo, "w") as f:
        json.dump(calendario, f, indent=4)
    print(f"\n🗂️ Calendario guardado como {nombre_archivo}")

# Estructura anidada por fecha
calendario = {}

if __name__ == "__main__":
    while True:
        fecha = input("\n📆 Introduce la fecha (YYYY-MM-DD) o 'fin' para salir: ").strip()
        if fecha.lower() == "fin":
            break

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            cambiar = pedir_horas_para_dia(fecha)
            if not cambiar:
                break
        except ValueError:
            print("❌ Formato de fecha inválido. Usa YYYY-MM-DD (ej. 2025-06-15)")

    guardar_json()
