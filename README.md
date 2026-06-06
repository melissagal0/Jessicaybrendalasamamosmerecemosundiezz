Instrucciones de cómo ejecutar el programa.


## 1. Registro del estudiante: 


1. El sistema te dará la bienvenida y te pedirá  ingresar tu **Nombre completo** en el programa. Escríbelo y presiona `enter`
   

2. Te pedirá la **Materia a evaluar** (Por ejemplo: `Cálculo`) Escríbela y presiona `enter`.
   

## 2. Responder el examen (Simulación de reactivos) 


El programa seleccionará de forma aleatoria **10 preguntas al azar** del banco de datos (`preguntas.csv`) sin repetir ninguna. Vas a ver pasar las preguntas una por una:


**Si la pregunta es de opción múltiple:** Verás el texto y sus opciones en la pantalla. Escribe únicamente la letra de la respuesta correcta (ej. `a`, `b`, `c`o `d`) y presiona `enter`.


**Si la pregunta es de Selección múltiple:** El programa  te va a mostrar un aviso en la pantalla. Debes ingresar tus dos opciones **separadas obligatoriamente por una coma**(ej. `a,b`o `b,d`) y presiona `enter`.


*Nota de la rúbrica para Selección múltiple:* Si ingresas sólo una bien obtendrás 0.5 puntos; si tienes las dos bien tendras 1.0 puntos; si te equivocas o pones de más tendrás 0.0 puntos


## 3. Gestión de intentos 


Al responder la pregunta 10, el programa calculará tu puntaje de forma inmediata y te mostrará tu calificación parcial sobre una escala de 10.0 puntos.


1. El sistema te preguntará en la pantalla si deseas realizar un intento extra para mejorar la calificación.


2. Verás 2 opciones en el programa:


   *Escribe `1` si deseas usar tu siguiente intenti (tienes un máximo de **3 intentos en total**. Al hacerlo, el programa borrará la pantalla y te lanzará un bloque completamente nuevo de 10 preguntas al azar.

   
   *Escribe `2`si decides quedarte con la calificación que obtuviste en ese momento y terminar el examen.

## 4. Cierre de sesión y guardado de datos automático 


*Cuando decidas terminar (o agotes tus 3 intentos), el programa calculará cuál fue **tu calificación más alta** de los intetnos que realizaste.


*El sistema guardará de froma automática una nueva fila en el archivo `datos/resultados.csv` registrando tu nombre, la calificaión de cada intento, tu calificación final definitivva y la fecha con hora exacta de tu aplicación.


*Nota de la rúbrica:* Si decidiste no usar el intento 2 o el intento 3, verás que le asigna automáticamente un guion (`-`) en el archivo final, cumpliendo con la resticción técnica del proyecto.

   
