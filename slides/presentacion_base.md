# Tarea 3 - LLMs locales

## 1. Objetivo

Comparar LLaMA, Phi y Mistral ejecutados localmente en la generacion de datos
sinteticos para consultas de estudiantes a soporte universitario.

## 2. Entorno

- Windows 11 Pro Insider Preview 26H2, 64 bits.
- CPU: Intel Core i5-10400 @ 2.90GHz.
- GPU: NVIDIA GeForce RTX 2060.
- RAM: 47.92 GB.
- Herramienta: Ollama 0.30.11.
- Modelos: llama3.2:3b, phi4-mini, mistral:7b.

## 3. Topico y prompts

Topico: consultas de estudiantes a soporte universitario.

Se usaron cinco prompts iguales para los tres modelos. Cada prompt pidio 20
ejemplos en JSON con `id`, `texto`, `intencion` y `urgencia`.

## 4. Dataset

- 100 ejemplos por modelo.
- 300 ejemplos totales.
- Formato JSONL.
- Split: 210 train, 45 validation, 45 test.

## 5. Metricas

| Modelo | Formato | Longitud | Relevancia | Unique | D-1 | D-2 |
|---|---:|---:|---:|---:|---:|---:|
| LLaMA | 0.81 | 0.52 | 0.68 | 0.91 | 0.1645 | 0.3561 |
| Phi | 0.76 | 0.12 | 0.65 | 0.79 | 0.2608 | 0.5940 |
| Mistral | 0.96 | 0.09 | 0.73 | 0.99 | 0.1600 | 0.3526 |

## 6. Analisis cualitativo

- LLaMA: natural, pero con etiquetas fuera del set permitido.
- Phi: alta diversidad lexica, pero menor consistencia de formato.
- Mistral: mejor formato y textos unicos, pero muchos textos demasiado breves.

## 7. Conclusion

Mistral fue el modelo mas conveniente por su estabilidad, formato valido y alta
relevancia. LLaMA fue el mejor en longitud. Phi fue el mas diverso, aunque menos
consistente.
