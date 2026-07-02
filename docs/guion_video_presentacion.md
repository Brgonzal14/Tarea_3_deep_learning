# Guion para el video de la Tarea 3

Este guion esta pensado para acompanar la presentacion
`outputs/tarea3_llms_locales.pptx`. No es necesario leerlo palabra por palabra;
la idea es usarlo como apoyo para explicar cada diapositiva de forma natural.

## Diapositiva 1 - Portada

Hola, en esta presentacion vamos a mostrar la Tarea 3 de Deep Learning, enfocada
en el uso de modelos de lenguaje locales para generar datos sinteticos.

El objetivo principal fue comparar tres modelos: LLaMA, Phi y Mistral. Todos
fueron ejecutados localmente con Ollama. En total generamos 300 ejemplos
sinteticos y luego los separamos en entrenamiento, validacion y prueba.

## Diapositiva 2 - Objetivo

La tarea pedia trabajar con tres LLMs locales y comparar su desempeno en una
tarea de generacion de datos sinteticos.

Para hacerlo de forma justa, usamos los mismos prompts para los tres modelos.
Asi evitamos que un modelo tuviera una ventaja por recibir instrucciones mas
claras o mas completas.

El flujo general fue: primero disenar los prompts, luego generar los datos,
validar el formato, calcular metricas y finalmente preparar el dataset final.

## Diapositiva 3 - Entorno local

Los modelos se ejecutaron localmente en un computador con Windows 11 Pro Insider
Preview 26H2. El equipo tiene un procesador Intel Core i5-10400, una GPU NVIDIA
RTX 2060 y 47.92 GB de RAM.

La herramienta utilizada fue Ollama, version 0.30.11. Los modelos usados fueron
`llama3.2:3b`, `phi4-mini` y `mistral:7b`.

La configuracion de generacion fue la misma para todos: temperatura 0.7,
`top_p` 0.9 y seed 3360. Esto permite que la comparacion sea mas ordenada.

## Diapositiva 4 - Dataset

El topico escogido fue consultas de estudiantes a soporte universitario.

Elegimos este tema porque es un dominio concreto y facil de delimitar. Los
textos generados representan mensajes de estudiantes que necesitan ayuda con
temas como matricula, pagos, horarios, plataforma, becas o certificados.

Cada ejemplo tiene cuatro campos: `id`, `texto`, `intencion` y `urgencia`.

Generamos 100 ejemplos por modelo, para un total de 300 registros. Luego el
dataset fue separado en 70% entrenamiento, 15% validacion y 15% prueba. Eso dio
210 ejemplos para entrenamiento, 45 para validacion y 45 para prueba.

## Diapositiva 5 - Resultados cuantitativos

En esta diapositiva se muestran las principales metricas.

La metrica de formato mide si el modelo respeto las etiquetas permitidas en los
campos `intencion` y `urgencia`. En este punto, Mistral fue el mejor, con 96%.

La longitud valida mide si el texto quedo dentro del rango pedido. Aqui LLaMA
fue el mejor, aunque ningun modelo cumplio perfecto esta restriccion.

La relevancia mide si el texto generado se relaciona con el topico
universitario. Mistral tambien tuvo el mejor resultado en esta metrica.

Por otro lado, Phi tuvo los valores mas altos en diversidad lexica, especialmente
en `distinct-1` y `distinct-2`.

## Diapositiva 6 - Analisis cualitativo

Ademas de las metricas, revisamos cualitativamente los textos generados.

LLaMA produjo textos bastante naturales, pero a veces genero etiquetas fuera del
conjunto permitido, por ejemplo variaciones como `beca` o errores como `beka`.

Phi genero textos con mayor diversidad lexica, pero tuvo menor consistencia en
el formato y mas repeticiones.

Mistral fue el modelo mas estable en formato y relevancia. Su principal problema
fue que muchas respuestas eran demasiado breves, aunque igualmente se mantenian
relacionadas con el tema.

## Diapositiva 7 - Hallazgos

El hallazgo principal es que no basta con pedirle a un modelo que genere datos.
Tambien hay que validar automaticamente la salida.

Aunque los modelos son buenos generando texto, no siempre respetan exactamente
el formato, las etiquetas o la longitud solicitada.

Por eso agregamos scripts para revisar JSON, etiquetas, longitud, duplicados y
diversidad. Esto permite comparar los modelos con evidencia y no solo con una
impresion subjetiva.

Tambien fue importante cambiar de Phi-3 mini a Phi-4 mini, porque la primera
variante genero mas problemas de formato y no permitia obtener de forma limpia
los 100 registros esperados.

## Diapositiva 8 - Conclusion

Como conclusion, el modelo recomendado para esta tarea fue Mistral.

La razon es que tuvo el mejor equilibrio entre formato valido, relevancia y
cantidad de textos unicos. LLaMA fue competitivo, especialmente en longitud, pero
tuvo mas problemas con etiquetas invalidas. Phi destaco por diversidad lexica,
pero fue menos consistente.

Para mejorar el trabajo en una siguiente version, se podria ajustar mejor los
prompts, balancear las etiquetas y agregar una revision humana de algunos
ejemplos.

Con esto queda generado un dataset sintetico de 300 registros, con codigo,
metricas, informe y presentacion listos para la entrega.

