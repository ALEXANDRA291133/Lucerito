#!/usr/bin/env bash
# Construye el modelo personalizado "lucerito" en Ollama a partir del Modelfile
# de este directorio. El modelo resultante ya trae "horneadas" las reglas de
# negocio y los parámetros de inferencia, así que cualquier cliente que lo
# invoque (Django, `ollama run`, otra app) hereda las mismas restricciones
# sin necesidad de reenviarlas en cada petición.
#
# Requisitos:
#   - Ollama instalado y corriendo (http://localhost:11434)
#   - Modelo base descargado: `ollama pull qwen2.5:1.5b`
#
# Uso:
#   cd Lucerito/ollama
#   ./build_model.sh
#
set -euo pipefail

MODEL_NAME="${1:-lucerito}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Verificando modelo base qwen2.5:1.5b..."
if ! ollama list | grep -q "qwen2.5:1.5b"; then
    echo "    No encontrado localmente, descargando..."
    ollama pull qwen2.5:1.5b
fi

echo "==> Construyendo modelo personalizado '${MODEL_NAME}'..."
ollama create "${MODEL_NAME}" -f "${SCRIPT_DIR}/Modelfile"

echo "==> Listo. Prueba con:  ollama run ${MODEL_NAME}"
echo "==> Recuerda ajustar OLLAMA_MODEL=${MODEL_NAME} en tu archivo .env"
