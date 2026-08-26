# Plan de migración de `legacy/TableTennisTests.mlx`

## 1. Objetivo de la migración

Reproducir en Python el comportamiento básico de la simulación MATLAB de una pelota de tenis de mesa: trayectoria 3D, velocidad lineal, giro, fuerzas de gravedad, arrastre y Magnus, rebote con la mesa, interacción simple con la red y visualización de la escena y de las series temporales. La primera migración debe conservar las decisiones del modelo original; no pretende todavía corregir ni ampliar su física.

## 2. Comportamiento del MATLAB original

El script simula 1.5 s de vuelo con pasos de `0.005 s`. Para cada instante calcula fuerza gravitatoria, arrastre lineal y fuerza de Magnus; actualiza aceleración, velocidad y posición. En paralelo amortigua la velocidad angular mediante un torque de arrastre y acumula el ángulo de rotación. Después de cada paso comprueba una colisión con la superficie de la mesa y otra con la red. Puede animar la pelota, sus vectores de velocidad/aceleración/giro y finalmente muestra gráficas de posición, velocidad, rotación acumulada y velocidad angular.

El sistema de coordenadas que se desprende del código es: `x` a lo largo de la mesa (0 a `table_length`), `y` a lo ancho (0 a `table_width`) y `z` vertical. La red está en `x = table_length / 2`.

## 3. Módulos Python propuestos y responsabilidades

| Módulo | Responsabilidad |
| --- | --- |
| `parameters.py` | Declarar las constantes del modelo y una forma única de agruparlas. Conservar los valores originales y documentar sus unidades y las pendientes de verificación. |
| `physics.py` | Implementar cálculos puros: fuerza total, aceleración lineal, torque de arrastre, aceleración angular y reglas de colisión. No debe gestionar bucles, gráficos ni estado global. |
| `simulation.py` | Crear las matrices/historiales de estado, aplicar condiciones iniciales, ejecutar el bucle temporal en el mismo orden que MATLAB y devolver tiempos, estados y, si corresponde, eventos de colisión. |
| `visualization.py` | Dibujar mesa, red, pelota y vectores; generar animación y gráficas de las series. Debe recibir datos ya calculados, sin modificar la simulación. |

## 4. Parámetros de simulación y unidades declaradas

Los valores siguientes son los declarados por el código original. Las unidades se transcriben de sus comentarios o se deducen del uso; no se deben reinterpretar durante la primera implementación.

| Parámetro | Valor | Unidad o significado indicado |
| --- | ---: | --- |
| `ball_mass` | 2.7 | g |
| `ball_radius` | 20.25 | mm |
| `ball_rot_inertia` | `2/3 * mass * radius^2` | g·mm² |
| `table_restitution` | 0.77 | adimensional |
| `net_restitution` | 0.5 | adimensional |
| `drag` | 2.7 | mN/(mm/s), según comentario |
| `rot_drag` | 350.0 | mN·mm/(rad/s), según comentario |
| `magnus` | 0.01 | mN/(mm/s²), según comentario |
| `table_friction` | 0.25 | proporción adimensional aplicada en el rebote |
| `table_length` | 2740 | mm |
| `table_width` | 1525 | mm |
| `table_height` | 760 | mm |
| `net_height` | 152.5 | mm |
| `net_extra` | 180 | mm |
| `g` | 9800 | mm/s² |
| `dt` | 0.005 | s |
| duración | 1.5 | s (`t = 0:dt:1.5`) |
| `plot_period` | 5 | pasos de simulación |
| `yaw` | -45 | grados, usado por la vista 3D |
| `pitch` | 23 (efecto práctico probable) | grados, pendiente de verificación por `pitch = 23,5` |

`animate` es un interruptor booleano de visualización. El literal `pitch = 23,5` no representa de forma inequívoca un decimal `23.5` en MATLAB: la coma separa expresiones, por lo que debe verificarse al ejecutar el Live Script antes de decidir si se migra como `23` o `23.5`.

## 5. Condiciones iniciales

Las matrices `x`, `v`, `a`, `theta`, `omega` y `alpha` tienen tres componentes y una columna por instante de tiempo. Inicialmente se asigna:

- Posición: `x0 = [0, table_width * 4/8, table_height + 2 * net_height] = [0, 762.5, 1065] mm`.
- Velocidad: `v0 = [7000, -3000, -3000] mm/s`.
- Velocidad angular: `omega0 = [0, 0, 75] * 2π rad/s`.
- Aceleración lineal, ángulo de rotación y aceleración angular: vectores cero por la preasignación. La aceleración del primer instante no se recalcula antes de la primera gráfica.

## 6. Variables y salidas esperadas

La simulación debe producir, al menos:

- `t`: vector temporal de 0 a 1.5 s, inclusivo.
- `x`, `v`, `a`: posición (mm), velocidad (mm/s) y aceleración usada por el código (esperada como mm/s²).
- `theta`, `omega`, `alpha`: ángulo acumulado (rad), velocidad angular (rad/s) y aceleración angular (rad/s²).
- Datos suficientes para la animación: estado instantáneo de la pelota y vectores `v`, `a` y `omega`.
- Series para gráficas: `x/1000` (m), `v/1000` (m/s), `theta/(2π)` (revoluciones) y `omega/(2π)` (rev/s).

Como salida adicional útil para verificación, Python puede registrar los índices de pasos donde se aplicó la regla de mesa o de red. Este registro no altera el modelo original.

## 7. Integración numérica original

El orden exacto por paso es importante:

1. Con el estado lineal anterior calcula `F = g·m·[0,0,-1] - drag·v + magnus·cross(omega, v)` y `a = F/m`.
2. Actualiza `v_k = v_(k-1) + a_k·dt`.
3. Actualiza `x_k = x_(k-1) + v_k·dt`.
4. Con `omega_(k-1)` calcula `tau = -rot_drag·omega_(k-1)` y `alpha = tau/I`.
5. Actualiza `omega_k = omega_(k-1) + alpha_k·dt` y `theta_k = theta_(k-1) + omega_k·dt`.
6. Aplica, finalmente, las reglas de mesa y red al estado del paso actual.

Es un Euler explícito para las aceleraciones evaluadas en el estado anterior, con actualización de posición y ángulo usando las velocidades ya actualizadas (Euler semiexplícito/simpléctico para esas variables). No se debe sustituir por un integrador distinto sin comparar primero los resultados.

## 8. Tratamiento de colisiones

### Mesa

Se activa si el centro de la pelota está dentro del rectángulo estricto de la mesa en `x` e `y` y `z < table_height + ball_radius`. La posición vertical se corrige a `table_height + ball_radius`. Después:

- calcula `delta_lin_rot = cross(omega, [0,0,ball_radius]) - [v_x,v_y,0]`;
- actualiza `v` con `v + table_friction * delta_lin_rot`;
- actualiza `omega` con `omega + table_friction * cross(delta_lin_rot,[0,0,1])/ball_radius`;
- invierte y reduce solo `v_z`: `v_z = -table_restitution * v_z`.

La regla se aplica por posición, sin comprobar que la pelota se esté acercando a la mesa; este detalle debe preservarse inicialmente y marcarse para una posible mejora posterior.

### Red

Se activa si el centro está a una distancia horizontal de hasta un radio de `x = table_length/2`, dentro del intervalo extendido de `y`, y entre `table_height + ball_radius` y `table_height + net_height + ball_radius` en `z`. La respuesta es deliberadamente simple: `omega` se multiplica por `net_restitution` y `v_x` se refleja y amortigua (`-net_restitution * v_x`). El propio MATLAB anota que esta colisión «requiere mejora».

## 9. Criterios mínimos de verificación

- Con los parámetros y estado inicial originales, Python debe generar el mismo número de muestras temporales que `0:0.005:1.5` (301, pendiente de confirmar con la ejecución de MATLAB si hubiera redondeo de punto flotante).
- Antes de una colisión, comprobar en muestras seleccionadas que las actualizaciones siguen las ecuaciones y el orden de cálculo descritos arriba.
- En cada rebote de mesa, verificar que `z = table_height + ball_radius` y que `v_z` cambia de signo con el factor `0.77` aplicado.
- En cada colisión de red, verificar que `v_x` cambia de signo y se escala por `0.5`, y que toda `omega` se escala por `0.5`.
- Verificar que las dimensiones de todos los historiales son `(3, len(t))` o su equivalente documentado en Python.
- Comparar visualmente trayectoria, lado de la red donde ocurre el primer contacto, rebotes y tendencia decreciente de giro con una ejecución de referencia de MATLAB. Las tolerancias numéricas exactas quedan pendientes mientras no se exporte una referencia del Live Script.

## 10. Riesgos conocidos de la migración

- **Unidades:** las etiquetas de `drag`, `rot_drag` y la fuerza gravitatoria mezclan g, mm, s y mN. En particular, la conversión dimensional entre `g·mm/s²` y mN no está explícita. Hay que conservar la aritmética inicial, documentar esta inconsistencia y validar magnitudes frente a MATLAB antes de normalizar unidades.
- **MATLAB y NumPy:** MATLAB usa vectores columna `(3,1)` y `cross` opera sobre esa convención; NumPy suele usar `(3,)`. Debe evitarse el *broadcasting* accidental y especificarse el eje en `np.cross` si se procesan lotes de estados.
- **Integración temporal:** cambiar el orden de las actualizaciones, usar `v` anterior para posición o aplicar colisiones antes de integrar cambia la trayectoria y el instante de impacto.
- **Colisiones:** son comprobaciones discretas de solapamiento y pueden atravesar una superficie si el paso temporal es grande. Los límites son una mezcla de desigualdades estrictas e inclusivas que debe mantenerse.
- **Efecto Magnus:** el orden del producto vectorial es `omega × v`; invertirlo cambia el signo de la desviación lateral. La unidad de `omega` debe permanecer en rad/s para mantener la magnitud original.
- **Visualización:** MATLAB usa `surf`, `sphere(25)`, `quiver3`, ejes iguales, límites fijos y `view([yaw pitch])`. Matplotlib u otra librería no reproducirá automáticamente perspectiva, escalas ni apariencia.
- **Signos y orientación:** `z` positivo es hacia arriba y la gravedad va en `-z`; la red es perpendicular a `x`; la velocidad inicial va hacia `+x`, `-y`, `-z`. Hay que mantener `cross(omega, [0,0,radius])` y `cross(delta_lin_rot,[0,0,1])` en ese orden.

## 11. Limitaciones conocidas del modelo físico original

- Arrastre y torque rotacional lineales, sin dependencia cuadrática de la velocidad ni coeficientes ajustados documentados.
- Fuerza de Magnus simplificada mediante un único coeficiente, sin validación experimental incluida.
- No hay detección continua de impactos ni cálculo del instante exacto de colisión.
- La mesa no tiene bordes, espesor ni respuesta ante impactos fuera de su rectángulo; tampoco se controla explícitamente que el impacto sea descendente.
- La red se modela como una zona plana y su respuesta solo modifica `v_x` y `omega`; no corrige posición ni modela deformación, rozamiento o componentes `v_y` y `v_z`.
- No se incluyen contactos con paleta, suelo, postes, aire variable ni pérdidas de energía adicionales.
- `theta` se integra, pero la orientación no se usa para geometría, aerodinámica ni colisiones.

## 12. Orden recomendado de implementación

1. Declarar en `parameters.py` las constantes originales sin cambiar valores ni unidades etiquetadas.
2. Definir una representación inequívoca del estado 3D y pruebas unitarias de productos vectoriales en `physics.py`.
3. Implementar fuerza, torque y las dos reglas de colisión de forma aislada.
4. Implementar en `simulation.py` la preasignación de historiales, condiciones iniciales y el bucle con el orden MATLAB.
5. Añadir las comprobaciones mínimas de dimensiones, rebotes y reglas de red.
6. Construir en `visualization.py` las gráficas de series y después la escena 3D/animación.
7. Ejecutar una comparación contra resultados exportados desde MATLAB y resolver las pendientes de `pitch`, unidades y tolerancias antes de cualquier mejora física.

## Pendientes de verificación con MATLAB

- El valor intencional de `pitch` (`23` frente a `23.5`).
- Las unidades coherentes y la escala numérica real de las fuerzas y del torque.
- Una trayectoria de referencia exportada para establecer tolerancias cuantitativas.
- Si el primer impacto con la red/mesa y cualquier reactivación de colisión concuerdan con la ejecución del Live Script en la versión de MATLAB objetivo.
