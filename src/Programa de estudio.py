import random
import csv
import os
from datetime import datetime

# ── Datos del estudiante ──────────────────────────────
nombre_estudiante = input("Ingresa tu nombre completo: ")
materia = input("Ingresa la materia: ")

# ── Cargar preguntas ──────────────────────────────────
def cargar_preguntas(file_path):
    preguntas = []

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        dos_respuestas = "Respuesta2" in reader.fieldnames

        for row in reader:
            if not row.get("Pregunta", "").strip():
                continue
            if not row.get("Respuesta1", "").strip():
                continue

            r1 = row["Respuesta1"].strip().upper()
            r2 = row["Respuesta2"].strip().upper() if dos_respuestas else ""

            preguntas.append({
                "Pregunta": row["Pregunta"].strip(),
                "Opciones": [
                    f"A) {row['A'].strip()}",
                    f"B) {row['B'].strip()}",
                    f"C) {row['C'].strip()}",
                    f"D) {row['D'].strip()}",
                ],
                "respuestas": sorted([r1, r2]) if r2 else [r1],
                "dual": bool(r2),
            })

    return preguntas


# ── Lógica de cada pregunta ───────────────────────────
def hacer_preguntas(q):
    if q["dual"]:
        while True:
            raw = input("Tus dos respuestas (por ejemplo: A C): ").strip().upper().split()
            seleccionadas = sorted(set(raw))
            if len(seleccionadas) == 2 and all(c in "ABCD" for c in seleccionadas):
                break
            print("Por favor ingresa exactamente dos letras de A, B, C, D.")

        correct = q["respuestas"]
        hits = sum(1 for c in seleccionadas if c in correct)

        if hits == 2:
            print("¡Ambas son correctas! (+1)")
            return 1.0
        elif hits == 1:
            correct_opts = " y ".join(
                next(o for o in q["Opciones"] if o.startswith(a)) for a in correct
            )
            print(f"Una es correcta (+0.5). Ambas respuestas: {correct_opts}")
            return 0.5
        else:
            correct_opts = " y ".join(
                next(o for o in q["Opciones"] if o.startswith(a)) for a in correct
            )
            print(f"¡Incorrecto! Respuestas correctas: {correct_opts}")
            return 0.0

    else:
        while True:
            respuesta = input("Tu respuesta: ").strip().upper()
            if respuesta in ("A", "B", "C", "D"):
                break
            print("Por favor ingresa una letra de A, B, C, D.")

        if respuesta == q["respuestas"][0]:
            print("¡Correcto! (+1)")
            return 1.0
        else:
            correct_opt = next(o for o in q["Opciones"] if o.startswith(q["respuestas"][0]))
            print(f"¡Incorrecto! Respuesta correcta: {correct_opt}")
            return 0.0


# ── Un intento del cuestionario ───────────────────────
def correr_intento(preguntas, numero_intento, n=10):
    total = len(preguntas)
    n = min(n, total)

    print(f"\n{'='*45}")
    print(f"  INTENTO {numero_intento} DE 3")
    print(f"{'='*45}")
    print(f"  {n} preguntas aleatorias de {total}.")
    print(f"  Escribe A, B, C, o D para contestar.\n")

    selec = random.sample(preguntas, n)
    puntaje = 0.0
    errores = []

    for i, q in enumerate(selec, 1):
        print(f"\nPregunta {i} de {n}: {q['Pregunta']}")
        for opcion in q["Opciones"]:
            print(f"  {opcion}")

        puntos = hacer_preguntas(q)
        puntaje += puntos

        if puntos < 1.0:
            correct_display = (
                " y ".join(next(o for o in q["Opciones"] if o.startswith(a)) for a in q["respuestas"])
                if q["dual"]
                else next(o for o in q["Opciones"] if o.startswith(q["respuestas"][0]))
            )
            errores.append((q["Pregunta"], correct_display, puntos))

    puntaje_str = str(int(puntaje)) if puntaje == int(puntaje) else f"{puntaje:.1f}"
    print(f"\n  Puntaje de este intento: {puntaje_str} / {n}")

    if errores:
        print("\n--- Preguntas a repasar ---")
        for pregunta, correcta, pts in errores:
            marca = "◑ parcial" if pts == 0.5 else "✗ incorrecta"
            print(f"[{marca}] {pregunta}")
            print(f"  → {correcta}\n")

    return puntaje


# ── Guardar resultados en CSV ─────────────────────────
def guardar_resultados(historial, mejor, archivo="resultados.csv"):
    # Rellenar intentos no realizados con guión
    intentos = [str(int(p)) if p == int(p) else f"{p:.1f}" for p in historial]
    while len(intentos) < 3:
        intentos.append("-")

    mejor_str = str(int(mejor)) if mejor == int(mejor) else f"{mejor:.1f}"
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Si el archivo no existe, escribir encabezados primero
    archivo_nuevo = not os.path.exists(archivo)

    with open(archivo, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if archivo_nuevo:
            writer.writerow(["Nombre completo", "Materia", "Intento 1", "Intento 2", "Intento 3", "Calificacion final", "Fecha"])
        writer.writerow([nombre_estudiante, materia, intentos[0], intentos[1], intentos[2], mejor_str, fecha])

    print(f"\n  ✅ Resultados guardados en '{archivo}'")


# ── Reporte final ─────────────────────────────────────
def mostrar_reporte(historial):
    mejor = max(historial)
    mejor_str = str(int(mejor)) if mejor == int(mejor) else f"{mejor:.1f}"

    print(f"\n{'='*45}")
    print(f"  📊 REPORTE FINAL")
    print(f"{'='*45}")
    print(f"  Estudiante : {nombre_estudiante}")
    print(f"  Materia    : {materia}")
    print(f"  Intentos   : {len(historial)} de 3")
    print()

    for i, p in enumerate(historial, 1):
        p_str = str(int(p)) if p == int(p) else f"{p:.1f}"
        marca = " ⬅ mejor" if p == mejor else ""
        print(f"  Intento {i}: {p_str} / 10{marca}")

    print(f"\n  Calificación final: {mejor_str} / 10")

    if mejor / 10 == 1.0:   print("  🏆 ¡Perfecto!")
    elif mejor / 10 >= 0.8: print("  🌟 ¡Excelente!")
    elif mejor / 10 >= 0.6: print("  👍 ¡Bien!")
    elif mejor / 10 >= 0.4: print("  📚 Sigue estudiando.")
    else:                   print("  💪 ¡No te rindas!")
    print(f"{'='*45}\n")

    guardar_resultados(historial, mejor)


# ── Punto de entrada ──────────────────────────────────
MAX_INTENTOS = 3

preguntas = cargar_preguntas("/Users/zarco/Downloads/Preguntas_-_Hoja_1.csv")
historial = []

for intento in range(1, MAX_INTENTOS + 1):
    puntaje = correr_intento(preguntas, intento)
    historial.append(puntaje)

    if intento < MAX_INTENTOS:
        while True:
            otra = input(f"\n¿Deseas hacer otro intento? Te quedan {MAX_INTENTOS - intento}. (s/n): ").strip().lower()
            if otra in ("s", "n"):
                break
            print("Por favor ingresa 's' para sí o 'n' para no.")
        if otra == "n":
            break

mostrar_reporte(historial)