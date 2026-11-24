#!/usr/bin/env python3
"""Lee por stdin el JSON de: java -jar target/assetdesk.jar demo."""
import json
import sys


def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    result = json.load(sys.stdin)
    check(result["application"] == "AssetDesk", "Aplicación inesperada.")
    for name, available, assigned in (("initialSummary", 3, 1), ("afterAssignment", 2, 2), ("afterRelease", 3, 1)):
        summary = result[name]
        check(summary == {"total": 4, "available": available, "assigned": assigned}, "Resumen incorrecto: " + name)
    check(result["assignment"]["status"] == "ASSIGNED", "La asignación no se refleja.")
    check(result["assignment"]["assignedTo"] == "Equipo Demo", "El equipo no coincide.")
    check(result["release"]["status"] == "AVAILABLE", "La devolución no se refleja.")
    check(result["release"]["assignedTo"] is None, "El recurso conserva una asignación.")
    check(len(result["resources"]) == 4, "Faltan recursos.")
    print("OK AssetDesk: catálogo, asignación, devolución y resúmenes correctos.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("FALLO: " + str(error), file=sys.stderr)
        sys.exit(1)
