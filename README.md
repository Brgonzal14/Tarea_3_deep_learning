# Tarea 3 - Deep Learning: LLMs locales

Proyecto para generar y evaluar datos sinteticos usando tres modelos locales:
LLaMA, Phi y Mistral.

## Tema escogido

Consultas de estudiantes a soporte universitario.

Cada ejemplo representa un mensaje breve escrito por un estudiante que necesita
ayuda. El dataset queda etiquetado con:

- `intencion`: matricula, pagos, horarios, plataforma, becas, certificado.
- `urgencia`: baja, media, alta.

Este tema esta delimitado, es realista para un contexto universitario y permite
evaluar si los modelos generan ejemplos coherentes, diversos y con formato
controlado.

## Estructura

```text
config/models.json          Modelos locales a comparar
prompts/prompts.json        Prompts identicos para los tres modelos
scripts/generate_dataset.py Generacion usando Ollama
scripts/evaluate_dataset.py Evaluacion cuantitativa
scripts/split_dataset.py    Separacion train/validation/test
data/raw/                   Respuestas crudas de cada modelo
data/generated/             JSONL limpio por modelo
data/final/                 Dataset unido y particionado
reports/                    Metricas y resumen para el informe
slides/                     Guion/base para la presentacion
```

## Paso 1: instalar herramienta local

Instalar Ollama desde:

https://ollama.com/download

Luego abrir PowerShell y verificar:

```powershell
ollama --version
```

## Paso 2: descargar los modelos

Modelos sugeridos para equipos personales:

```powershell
ollama pull llama3.2:3b
ollama pull phi4-mini
ollama pull mistral:7b
```

Si el computador tiene poca RAM, se puede usar una variante mas pequena, pero se
debe dejar anotado en el informe.

## Paso 3: generar datos sinteticos

El plan base genera 5 lotes de 20 ejemplos por modelo, es decir:

- 100 ejemplos con LLaMA.
- 100 ejemplos con Phi.
- 100 ejemplos con Mistral.
- 300 ejemplos en total.

Ejecutar:

```powershell
python scripts/generate_dataset.py --models config/models.json --prompts prompts/prompts.json
```

Para una prueba rapida sin gastar tanto tiempo:

```powershell
python scripts/generate_dataset.py --models config/models.json --prompts prompts/prompts.json --limit-prompts 1
```

## Paso 4: evaluar resultados

```powershell
python scripts/evaluate_dataset.py --input data/generated --output reports
```

El script calcula metricas comparables:

- porcentaje de ejemplos validos.
- cumplimiento del formato solicitado.
- cumplimiento de longitud.
- relevancia lexical respecto al topico.
- diversidad `distinct-1` y `distinct-2`.
- distribucion de etiquetas.
- duplicados aproximados por texto normalizado.

## Paso 5: unir y separar dataset

Aunque la pauta no pide entrenar un modelo, se deja un split ordenado para uso
posterior:

- 70% entrenamiento.
- 15% validacion.
- 15% prueba.

```powershell
python scripts/split_dataset.py --input data/generated --output data/final --train 0.70 --validation 0.15 --test 0.15
```

## Paso 6: completar informe/video

Usar `slides/presentacion_base.md` como guion para las diapositivas y el video.
La entrega final debe incluir:

- repositorio GitHub con este codigo y datasets generados.
- video de maximo 20 minutos.
- presentacion usada en el video.

## Datos del entorno documentado

| Campo | Valor |
|---|---|
| Sistema operativo | Windows 10 Pro 2009, 64 bits |
| CPU | Intel Core i5-10400 @ 2.90GHz |
| GPU | NVIDIA GeForce RTX 2060 |
| RAM | 47.92 GB |
| Herramienta | Ollama |
| Modelos | llama3.2:3b, phi4-mini, mistral:7b |
| Temperatura | 0.7 |
| top_p | 0.9 |
| Max tokens | 4096 |
