#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VARIANT="${1:-jsf}"
case "$VARIANT" in
  jsf|struts) ;;
  *) echo "Uso: bash scripts/preparar.sh jsf|struts"; exit 1 ;;
esac
TASK_WORK="$LAB_ROOT/work"
if [ -e "$TASK_WORK" ]; then
  echo "Ya existe $TASK_WORK. Se conserva; usa esa copia o renómbrala para cambiar de variante."
  exit 1
fi
if [ ! -f "$LAB_ROOT/LAB.md" ]; then
  echo "No se encuentra la guía LAB.md junto al laboratorio." >&2
  exit 1
fi

# La guía es la única fuente de la plantilla de entrega.
LAB_REPORT_TMP="$(mktemp)"
trap 'rm -f "$LAB_REPORT_TMP"' EXIT
awk '
  $0 == "<!-- ROOMFLOW_INFORME_INICIO -->" { inside = 1; started = 1; next }
  $0 == "<!-- ROOMFLOW_INFORME_FIN -->" { inside = 0; finished = 1; next }
  inside && ($0 == "```markdown" || $0 == "```") { next }
  inside { print; lines++ }
  END { if (!started || !finished || !lines) exit 1 }
' "$LAB_ROOT/LAB.md" > "$LAB_REPORT_TMP"

mkdir -p "$TASK_WORK/docs" "$TASK_WORK/back" "$TASK_WORK/front"
cp -R "$LAB_ROOT/legacy-$VARIANT/." "$TASK_WORK/"
cat > "$TASK_WORK/.gitignore" <<'IGNORE'
target/
**/target/
**/node_modules/
**/dist/
**/playwright-report/
**/test-results/
.env
**/.env.local
.idea/
*.log
IGNORE
cp "$LAB_REPORT_TMP" "$TASK_WORK/docs/INFORME-FINAL.md"

echo "Variante: $VARIANT. Preparado: $TASK_WORK"
echo "Sigue LAB.md y abre work/ en Bob. Tu entrega está en work/docs/INFORME-FINAL.md."
echo "back/ y front/ son opcionales: úsalos solo si el wizard pide esos directorios."
