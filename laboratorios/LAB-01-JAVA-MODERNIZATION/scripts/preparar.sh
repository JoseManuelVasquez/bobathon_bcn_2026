#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_WORK="$LAB_ROOT/work"
if [ -e "$TASK_WORK" ]; then
  echo "Ya existe $TASK_WORK. Se conserva; usa esa copia o renómbrala para repetir."
  exit 1
fi
mkdir -p "$TASK_WORK/docs"
cp -R "$LAB_ROOT/legacy/." "$TASK_WORK/"
cat > "$TASK_WORK/.gitignore" <<'IGNORE'
target/
.env
.idea/
*.log
IGNORE
cp "$LAB_ROOT/plantillas/INFORME-FINAL.md" "$TASK_WORK/docs/INFORME-FINAL.md"
echo "Preparado: $TASK_WORK"
echo "Abre esa carpeta en Bob. Inicializa Git y establece la compilación de referencia con JDK 8."
