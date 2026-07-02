# Explicacion del codigo de la Tarea 3

Este documento explica para que sirve cada archivo de codigo/configuracion de la
tarea y por que se uso dentro del flujo completo.

## Idea general

La tarea consiste en ejecutar localmente tres modelos de lenguaje:

- LLaMA
- Phi
- Mistral

Con esos modelos se generan datos sinteticos usando los mismos prompts. Luego se
evalua la calidad de los resultados y se deja el dataset final separado en
entrenamiento, validacion y prueba.

El flujo general es:

```text
config/models.json + prompts/prompts.json
        ↓
scripts/generate_dataset.py
        ↓
data/generated/*.jsonl
        ↓
scripts/evaluate_dataset.py
        ↓
reports/metrics_*.*
        ↓
scripts/split_dataset.py
        ↓
data/final/train-validation-test
```

## 1. `config/models.json`

Este archivo define los modelos locales que se usan con Ollama.

Modelos usados:

- `llama3.2:3b`
- `phi4-mini`
- `mistral:7b`

Tambien guarda la configuracion comun de generacion:

- `temperature: 0.7`: permite que las respuestas tengan variedad sin volverse
  demasiado aleatorias.
- `top_p: 0.9`: limita la generacion a opciones probables.
- `num_predict: 4096`: define el maximo de tokens que puede generar el modelo.
- `seed: 3360`: ayuda a que la generacion sea mas reproducible.

La razon de tener este archivo separado es que se pueden cambiar modelos o
parametros sin modificar el script principal.

## 2. `prompts/prompts.json`

Este archivo contiene los prompts usados para generar el dataset sintetico.

La pauta pide que los tres modelos sean evaluados con los mismos prompts. Por
eso todos los modelos reciben exactamente las mismas instrucciones.

Cada prompt pide:

- 20 ejemplos.
- Texto en espanol.
- Salida en formato JSON.
- Campos exactos: `id`, `texto`, `intencion`, `urgencia`.
- Intenciones permitidas:
  - `matricula`
  - `pagos`
  - `horarios`
  - `plataforma`
  - `becas`
  - `certificado`
- Urgencias permitidas:
  - `baja`
  - `media`
  - `alta`

Se usaron 5 prompts. Como cada prompt pide 20 ejemplos:

```text
5 prompts x 20 ejemplos = 100 ejemplos por modelo
```

Como son 3 modelos:

```text
100 ejemplos x 3 modelos = 300 ejemplos en total
```

## 3. `scripts/generate_dataset.py`

Este es el script principal de generacion de datos.

Su funcion es conectarse a Ollama de forma local y pedirle a cada modelo que
genere ejemplos sinteticos.

El script hace lo siguiente:

1. Lee los modelos desde `config/models.json`.
2. Lee los prompts desde `prompts/prompts.json`.
3. Llama a la API local de Ollama.
4. Extrae el JSON generado por cada modelo.
5. Normaliza cada registro.
6. Guarda un archivo por modelo en `data/generated/`.

Archivos generados:

- `data/generated/llama.jsonl`
- `data/generated/phi.jsonl`
- `data/generated/mistral.jsonl`

Tambien incluye una parte importante: si un modelo entrega menos ejemplos de los
esperados, el script intenta reparar la respuesta pidiendo solo los IDs
faltantes. Esto es util porque los modelos locales a veces no respetan perfecto
el formato solicitado.

## 4. `scripts/evaluate_dataset.py`

Este script evalua los datasets generados por los modelos.

La pauta pide comparar los modelos considerando criterios como:

- coherencia,
- relevancia,
- diversidad,
- cumplimiento del formato.

Este script calcula metricas cuantitativas para apoyar esa comparacion.

Metricas principales:

- `schema_valid_rate`: mide si el registro tiene las etiquetas validas.
- `length_valid_rate`: mide si el texto respeta la longitud pedida.
- `topic_relevance_rate`: mide si el texto contiene terminos relacionados con
  el contexto universitario.
- `unique_text_rate`: mide la proporcion de textos no repetidos.
- `duplicate_count`: cuenta textos repetidos.
- `distinct_1`: mide diversidad de palabras individuales.
- `distinct_2`: mide diversidad de pares de palabras.
- distribucion de `intencion`.
- distribucion de `urgencia`.

Archivos generados:

- `reports/metrics_summary.csv`
- `reports/metrics_detailed.json`
- `reports/analysis_template.md`

La idea es que la comparacion no dependa solo de una opinion, sino que se pueda
justificar con numeros.

## 5. `scripts/split_dataset.py`

Este script une los datos generados por los tres modelos y los separa en:

```text
70% entrenamiento
15% validacion
15% prueba
```

Aunque la pauta no pide entrenar un modelo, dejar este split hace que el dataset
quede mejor organizado y preparado para un posible uso posterior.

Con 300 registros, el resultado final fue:

- `train`: 210 ejemplos.
- `validation`: 45 ejemplos.
- `test`: 45 ejemplos.

Archivos generados:

- `data/final/train.jsonl`
- `data/final/validation.jsonl`
- `data/final/test.jsonl`
- `data/final/manifest.json`

El archivo `manifest.json` guarda el resumen del split: total de registros,
porcentajes usados y cantidad de ejemplos por particion.

## 6. `scripts/check_environment.ps1`

Este script sirve para documentar el entorno del computador.

La pauta pide indicar:

- sistema operativo,
- CPU,
- GPU,
- RAM,
- herramienta usada,
- modelos disponibles.

Este script obtiene esos datos desde Windows y Ollama. Sirve para demostrar que
los modelos fueron ejecutados localmente y para dejar documentado el ambiente de
trabajo.

## Resumen final

Cada archivo cumple una funcion dentro del flujo:

| Archivo | Funcion |
|---|---|
| `config/models.json` | Define modelos y parametros de generacion |
| `prompts/prompts.json` | Guarda los prompts iguales para todos los modelos |
| `scripts/generate_dataset.py` | Genera el dataset sintetico con Ollama |
| `scripts/evaluate_dataset.py` | Calcula metricas de comparacion |
| `scripts/split_dataset.py` | Separa el dataset en train, validation y test |
| `scripts/check_environment.ps1` | Documenta el computador y los modelos locales |

En conjunto, estos archivos hacen que la tarea sea:

- reproducible,
- comparable,
- ordenada,
- facil de explicar en el video,
- y defendible frente a la pauta.

