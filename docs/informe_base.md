# Informe base - Tarea 3 Deep Learning

## 1. Introduccion

El objetivo de esta tarea fue comparar tres modelos de lenguaje ejecutados de
forma local en la generacion de datos sinteticos. Los modelos evaluados fueron
LLaMA, Phi y Mistral. Para mantener una comparacion justa, los tres modelos
recibieron los mismos cinco prompts, con el mismo topico, formato esperado,
cantidad de ejemplos y configuracion de generacion.

## 2. Entorno utilizado

| Campo | Valor |
|---|---|
| Sistema operativo | Windows 10 Pro 2009, 64 bits |
| CPU | Intel Core i5-10400 @ 2.90GHz |
| Procesadores logicos | 12 |
| GPU | NVIDIA GeForce RTX 2060 |
| VRAM reportada | 4 GB |
| RAM | 47.92 GB |
| Herramienta de ejecucion | Ollama 0.30.11 |
| Modelo LLaMA | llama3.2:3b |
| Modelo Phi | phi4-mini |
| Modelo Mistral | mistral:7b |
| Temperatura | 0.7 |
| top_p | 0.9 |
| Max tokens | 4096 |
| Seed | 3360 |

## 3. Topico seleccionado

El topico seleccionado fue consultas de estudiantes a soporte universitario. Se
escogio este dominio porque permite generar textos breves, realistas y
clasificables segun intencion y urgencia. El tema esta delimitado a mensajes
relacionados con matricula, pagos, horarios, plataforma, becas y certificados.

## 4. Diseno de prompts

Se disenaron cinco prompts. Cada prompt solicito 20 ejemplos en espanol, en
formato JSON, con los campos `id`, `texto`, `intencion` y `urgencia`. Las
intenciones permitidas fueron `matricula`, `pagos`, `horarios`, `plataforma`,
`becas` y `certificado`. Las urgencias permitidas fueron `baja`, `media` y
`alta`.

## 5. Dataset generado

Cada modelo genero 100 ejemplos, para un total de 300 registros sinteticos. El
formato de almacenamiento fue JSONL, donde cada linea contiene un registro
independiente.

| Modelo | Registros |
|---|---:|
| LLaMA | 100 |
| Phi | 100 |
| Mistral | 100 |
| Total | 300 |

El dataset final fue separado en 70% entrenamiento, 15% validacion y 15%
prueba:

| Split | Registros | Porcentaje |
|---|---:|---:|
| Train | 210 | 70% |
| Validation | 45 | 15% |
| Test | 45 | 15% |

## 6. Evaluacion cuantitativa

| Modelo | Formato valido | Longitud valida | Relevancia | Unique text | Distinct-1 | Distinct-2 |
|---|---:|---:|---:|---:|---:|---:|
| LLaMA | 0.8100 | 0.5200 | 0.6800 | 0.9100 | 0.1645 | 0.3561 |
| Phi | 0.7600 | 0.1200 | 0.6500 | 0.7900 | 0.2608 | 0.5940 |
| Mistral | 0.9600 | 0.0900 | 0.7300 | 0.9900 | 0.1600 | 0.3526 |

La metrica de formato valido mide si el registro contiene etiquetas permitidas
en `intencion` y `urgencia`. La longitud valida mide si el texto quedo entre 12
y 35 palabras, como se solicito en los prompts. La relevancia es una medida
lexical simple respecto al topico universitario. `Unique text` mide proporcion
de textos no duplicados. `Distinct-1` y `Distinct-2` miden diversidad lexica en
unigramas y bigramas.

## 7. Evaluacion cualitativa

### LLaMA

LLaMA produjo mensajes generalmente naturales y obtuvo una tasa intermedia de
formato valido. Su principal problema fue la aparicion de etiquetas no
permitidas, como `beka` o `beca`, y algunos registros sin intencion. Fue el
modelo que mejor respeto la restriccion de longitud relativa al resto.

Ejemplo correcto: "No puedo acceder a mis horarios de clase, como puedo
hacerlo?" con intencion `horarios` y urgencia `alta`.

### Phi

Phi-4 mini genero 100 registros sin errores de ejecucion y mostro la mayor
diversidad lexica, con `distinct-1` de 0.2608 y `distinct-2` de 0.5940. Sin
embargo, presento mas duplicacion de estructuras y una tasa menor de formato
valido que Mistral. En una prueba previa con Phi-3 mini se observaron errores
frecuentes de JSON, por lo que se uso Phi-4 mini como variante local de la
familia Phi.

Ejemplo correcto: "Necesito ayuda para actualizar mi horario en la plataforma
universitaria." con intencion `horarios` y urgencia `alta`.

### Mistral

Mistral fue el modelo con mejor cumplimiento de formato, con una tasa de 0.9600,
y tambien la mayor proporcion de textos unicos. Su principal debilidad fue no
respetar bien la longitud minima y maxima solicitada: muchas respuestas fueron
demasiado breves. En coherencia y relevancia general fue el modelo mas estable.

Ejemplo correcto: "Tengo dudas sobre mi pago de matricula, como puedo
solucionarlo?" con intencion `pagos` y urgencia `alta`.

## 8. Conclusion

El modelo mas conveniente para este dataset fue Mistral, porque obtuvo el mejor
cumplimiento de formato, buena relevancia respecto al topico y casi todos sus
textos fueron unicos. LLaMA fue competitivo y respeto mejor la longitud
solicitada, pero genero mas etiquetas fuera del conjunto permitido. Phi-4 mini
destaco por diversidad lexica, aunque tuvo menor consistencia en etiquetas y mas
duplicacion. Para una version final de produccion, se recomienda usar Mistral y
aplicar una etapa de validacion automatica posterior para corregir longitud y
etiquetas.

