# Paso a paso de la Tarea 3

## 1. Leer la pauta

La tarea no pide entrenar un modelo de deep learning. Pide ejecutar tres LLMs
locales, generar datos sinteticos con los mismos prompts y comparar los
resultados. Por orden, se debe entregar:

1. Entorno documentado.
2. Topico definido y justificado.
3. Prompts iguales para LLaMA, Phi y Mistral.
4. Dataset sintetico generado por cada modelo.
5. Comparacion cualitativa y cuantitativa.
6. Video de maximo 20 minutos.
7. Presentacion y GitHub con el material.

## 2. Preparar entorno local

Instalar Ollama y verificar:

```powershell
ollama --version
```

Descargar los modelos:

```powershell
ollama pull llama3.2:3b
ollama pull phi4-mini
ollama pull mistral:7b
```

Verificar que esten disponibles:

```powershell
ollama list
```

## 3. Documentar el computador

Ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_environment.ps1
```

Copiar esos datos a la tabla del `README.md` y a la presentacion.

## 4. Generar un lote pequeno de prueba

Antes de generar todo, probar con un solo prompt:

```powershell
python scripts/generate_dataset.py --models config/models.json --prompts prompts/prompts.json --limit-prompts 1
```

Esperado:

- `data/generated/llama.jsonl`
- `data/generated/phi.jsonl`
- `data/generated/mistral.jsonl`
- archivos crudos en `data/raw/`

Si un modelo falla, revisar que Ollama este abierto y que el modelo aparezca en
`ollama list`.

## 5. Generar el dataset completo

```powershell
python scripts/generate_dataset.py --models config/models.json --prompts prompts/prompts.json
```

Resultado esperado:

- 100 ejemplos por modelo.
- 300 ejemplos en total.

## 6. Evaluar cuantitativamente

```powershell
python scripts/evaluate_dataset.py --input data/generated --output reports
```

Archivos generados:

- `reports/metrics_summary.csv`
- `reports/metrics_detailed.json`
- `reports/analysis_template.md`

Estas metricas sirven para la parte cuantitativa de la pauta.

## 7. Hacer split train/validation/test

Aunque no se entrena un modelo en esta tarea, se deja el dataset preparado:

```powershell
python scripts/split_dataset.py --input data/generated --output data/final --train 0.70 --validation 0.15 --test 0.15
```

Con 300 ejemplos, el resultado aproximado sera:

- 210 entrenamiento.
- 45 validacion.
- 45 prueba.

## 8. Analisis cualitativo

Abrir algunos ejemplos de cada modelo y completar:

- Coherencia: el mensaje se entiende y parece escrito por un estudiante.
- Relevancia: el contenido pertenece al contexto universitario.
- Diversidad: no repite siempre la misma estructura.
- Formato: respeta JSON, etiquetas y campos solicitados.

Se recomienda elegir 2 ejemplos buenos y 1 ejemplo problematico por modelo para
mostrarlos en el video. En esta ejecucion final se uso `phi4-mini`, porque la
prueba inicial con `phi3:mini` genero varios errores de JSON y no permitio
obtener la misma cantidad de registros que los otros modelos.

## 9. Video

Estructura recomendada para 15 a 18 minutos:

1. Objetivo y pauta: 1 min.
2. Entorno y modelos: 2 min.
3. Topico y prompts: 3 min.
4. Generacion del dataset: 3 min.
5. Resultados cuantitativos: 3 min.
6. Analisis cualitativo: 3 min.
7. Conclusion: 1 a 2 min.

## 10. GitHub

Subir:

- codigo.
- prompts.
- datasets generados si no pesan demasiado.
- reportes.
- presentacion.
- README con instrucciones.
