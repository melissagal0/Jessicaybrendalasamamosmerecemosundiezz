import csv
import os
from datetime import datetime
from collections import defaultdict

ARCHIVO = "resultados.csv"
LINE  = "─" * 50
DLINE = "═" * 50


def cargar_resultados(archivo):
    if not os.path.exists(archivo):
        print(f"\n  ❌ No se encontró '{archivo}'.")
        print(f"  Asegúrate de que esté en la misma carpeta que este script.\n")
        return []

    registros = []
    with open(archivo, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                registros.append({
                    "nombre":  row["Nombre completo"].strip(),
                    "materia": row["Materia"].strip(),
                    "intento1": float(row["Intento 1"]) if row["Intento 1"] != "-" else None,
                    "intento2": float(row["Intento 2"]) if row["Intento 2"] != "-" else None,
                    "intento3": float(row["Intento 3"]) if row["Intento 3"] != "-" else None,
                    "final":   float(row["Calificacion final"]),
                    "fecha":   row["Fecha"].strip(),
                    "dia":     row["Fecha"].strip().split(" ")[0],  # solo dd/mm/yyyy
                })
            except (ValueError, KeyError):
                continue  # saltar filas malformadas

    return registros


def promedio(lista):
    valores = [v for v in lista if v is not None]
    return sum(valores) / len(valores) if valores else 0.0


def fmt(num):
    """Formatea número: sin decimal si es entero, 2 decimales si no."""
    return str(int(num)) if num == int(num) else f"{num:.2f}"


def mostrar_reporte(registros):
    if not registros:
        print("  No hay datos para analizar.")
        return

    calificaciones_finales = [r["final"] for r in registros]

    print(f"\n{DLINE}")
    print(f"  📊 REPORTE DE RESULTADOS")
    print(f"{DLINE}")

    # ── 1. Total de estudiantes ───────────────────────
    # Contamos nombres únicos
    estudiantes_unicos = set(r["nombre"] for r in registros)
    print(f"\n  {'Total de estudiantes evaluados:':<35} {len(estudiantes_unicos)}")
    print(f"  {'Total de registros (intentos):':<35} {len(registros)}")

    # ── 2. Promedio general ───────────────────────────
    prom_general = promedio(calificaciones_finales)
    print(f"\n{LINE}")
    print(f"  📈 PROMEDIO GENERAL")
    print(f"{LINE}")
    print(f"  Promedio de calificaciones finales: {fmt(prom_general)} / 10")

    # ── 3. Promedio por materia ───────────────────────
    print(f"\n{LINE}")
    print(f"  📚 PROMEDIO POR MATERIA")
    print(f"{LINE}")
    por_materia = defaultdict(list)
    for r in registros:
        por_materia[r["materia"]].append(r["final"])

    for materia, califs in sorted(por_materia.items()):
        prom = promedio(califs)
        print(f"  {materia:<35} {fmt(prom)} / 10  ({len(califs)} registro{'s' if len(califs) != 1 else ''})")

    # ── 4. Promedio por fecha ─────────────────────────
    print(f"\n{LINE}")
    print(f"  📅 PROMEDIO POR FECHA")
    print(f"{LINE}")
    por_fecha = defaultdict(list)
    for r in registros:
        por_fecha[r["dia"]].append(r["final"])

    # Ordenar fechas cronológicamente
    def parse_fecha(f):
        try:
            return datetime.strptime(f, "%d/%m/%Y")
        except ValueError:
            return datetime.min

    for fecha in sorted(por_fecha.keys(), key=parse_fecha):
        califs = por_fecha[fecha]
        prom = promedio(califs)
        print(f"  {fecha:<20} Promedio: {fmt(prom)} / 10  ({len(califs)} registro{'s' if len(califs) != 1 else ''})")

    # ── 5. Mejor estudiante ───────────────────────────
    print(f"\n{LINE}")
    print(f"  🏆 MEJOR ESTUDIANTE")
    print(f"{LINE}")

    # Si un estudiante tiene varios registros, tomamos su mejor calificación final
    mejor_por_estudiante = {}
    for r in registros:
        nombre = r["nombre"]
        if nombre not in mejor_por_estudiante or r["final"] > mejor_por_estudiante[nombre]["final"]:
            mejor_por_estudiante[nombre] = r

    mejor = max(mejor_por_estudiante.values(), key=lambda r: r["final"])
    print(f"  Nombre   : {mejor['nombre']}")
    print(f"  Materia  : {mejor['materia']}")
    print(f"  Calif.   : {fmt(mejor['final'])} / 10")
    print(f"  Fecha    : {mejor['fecha']}")

    # ── 6. Tabla completa de estudiantes ─────────────
    print(f"\n{LINE}")
    print(f"  📋 DETALLE POR ESTUDIANTE")
    print(f"{LINE}")
    print(f"  {'Nombre':<25} {'Materia':<22} {'I1':>4} {'I2':>4} {'I3':>4} {'Final':>6}  Fecha")
    print(f"  {'-'*25} {'-'*22} {'-'*4} {'-'*4} {'-'*4} {'-'*6}  {'-'*16}")

    for r in registros:
        i1 = fmt(r["intento1"]) if r["intento1"] is not None else "-"
        i2 = fmt(r["intento2"]) if r["intento2"] is not None else "-"
        i3 = fmt(r["intento3"]) if r["intento3"] is not None else "-"
        print(f"  {r['nombre']:<25} {r['materia']:<22} {i1:>4} {i2:>4} {i3:>4} {fmt(r['final']):>6}  {r['fecha']}")

    print(f"\n{DLINE}\n")


# ── Punto de entrada ──────────────────────────────────
registros = cargar_resultados(ARCHIVO)
mostrar_reporte(registros)