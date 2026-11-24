# ChatGPT Desktop Access for NVDA

ChatGPT Desktop Access es compatible tanto con el modo ChatGPT como con el modo Codex en la aplicación de Windows. Se vuelve a vincular automáticamente tras cambiar de modo o regresar desde la página de uso; no es necesario reiniciar NVDA.

[![Validar complemento de NVDA](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml/badge.svg)](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml)

ChatGPT Desktop Access for NVDA proporciona anuncios de actividad en vivo, braille, sonidos de progreso, navegación y acciones de chat, y foco del sistema accesible en los cuadros de diálogo tanto en modo exploración como en modo foco. Anteriormente se llamaba Codex Access Toolkit y Codex Status Announcer; el identificador interno del complemento permanece sin cambios para que la configuración existente y las asignaciones en Gestos de entrada sigan funcionando.

## Descarga

Nota de compatibilidad de la compilación de desarrollo: los análisis de transcripción de Chromium UIA ahora utilizan un movimiento nativo masivo de puntos finales en lugar del recorrido carácter por carácter de la navegación web. El historial, la revisión de mensajes recientes y la capacidad de respuesta al inicio aún requieren verificación en vivo con la aplicación actualizada antes de que esta compilación sea aprobada para su lanzamiento.

Descargue los paquetes probados desde la [página de GitHub Releases](https://github.com/jcoffin1/chatgpt-desktop-access/releases). El proyecto se está preparando para la Tienda de complementos oficial de NVDA, pero aún no figura en ella.

## Opciones

Abra **Menú NVDA > Preferencias > Opciones > ChatGPT Desktop Access**. El panel se divide en ocho páginas accesibles mediante el teclado: **General**, **Voz y braille**, **Sonidos**, **Salida de actividad**, **Redacción y vista previa**, **Acceso al navegador**, **Avanzado**, y **Soporte**.

Pulse Control+Tab o Shift+Control+Tab para desplazarse entre las páginas. Cada control interactivo tiene una tecla de acceso rápido Alt distinta dentro de su página. General contiene las opciones principales de salida, y Salida de actividad contiene los tiempos en segundo plano y el Enrutamiento por categorías.

Avanzado contiene controles técnicos de compatibilidad. Soporte contiene acciones relacionadas con la cuenta, la documentación, la solución de problemas y los archivos de configuración.

Las opciones incluyen:

- Un interruptor en la página General para la lista nativa de mensajes de conversación, activado por defecto.
- Etiquetas de progreso Mínimo o Completo (Completo es el predeterminado).
- Perfil de voz Mínimo Esencial, Equilibrado o Informativo. Equilibrado es el predeterminado; Esencial limita la voz a estados críticos, mientras que Informativo añade nombres de archivo seguros, recuentos y tiempos útiles sin exponer los comandos completos.
- Perfiles de voz Completa Estándar, Desarrollador o Sin procesar. Estándar anuncia una acción con destinos concisos, recuentos y tiempos útiles; Desarrollador conserva los comandos normalizados completos y el progreso; Sin procesar conserva la redacción exacta expuesta. El braille completo permanece íntegro independientemente del perfil de voz.
- Voz y braille configurables de forma independiente.
- Nivel de detalle braille Conciso, Informativo o Completo independiente de la verbosidad de la voz.
- Una protección opcional de lectura de la conversación evita que el progreso rutinario del complemento y las actualizaciones ordinarias en vivo de respuestas transmitidas interrumpan la voz, reemplacen la línea braille actual o reubiquen la lectura en modo exploración en ChatGPT. La salida de respuestas en modo foco, los resultados importantes, los cuadros de diálogo de permisos y las alertas urgentes continúan con normalidad.
- Al regresar a una tarea que sigue activa, un foco obsoleto en una tarjeta de actividad de Chromium se corrige al encabezado de respuesta más reciente en modo exploración si le sigue una salida más nueva. Esto mueve únicamente la posición de lectura virtual de NVDA, nunca el foco del sistema de Windows, y cualquier pulsación de tecla del usuario cancela la corrección.
- Interrupción opcional de la voz actual de NVDA para permisos urgentes y fallos.
- Ocultación opcional de posibles secretos y datos personales.
- El intervalo para las actualizaciones del tiempo de trabajo transcurrido.
- Un pulso recurrente «Sigue trabajando en segundo plano» en los modos Mínimo y Completo, con suaves sonidos alternos de dos notas.
- Categorías de progreso individuales. Cada elemento de categoría indica si está activado y su ruta de salida actual, como «Comandos: activado; solo voz».
- Actualizaciones de comentarios de Codex en lenguaje sencillo tanto en modo Mínimo como en modo Completo.
- Sonidos de finalización y registro de diagnóstico depurado.
- Sonidos inmediatos y opcionales de Petición enviada con un retraso configurable antes de que comiencen los sonidos continuos de Trabajo.
- Detección de Petición de envío para Intro y el botón Enviar, detección de cancelación de petición, supresión de eventos duplicados y estado aislado entre tareas de Codex.
- La detección inmediata de envío observa la tecla Intro sin modificar del teclado y el punto 8 independiente (Intro) de una pantalla braille antes de que ChatGPT reemplace su contenido de Petición editable. El observador nunca intercepta ni reenvía el gesto; Shift+Intro y todas las demás entradas conservan su comportamiento nativo.
- La protección de escritura de petición suspende los análisis completos de compatibilidad de Chromium mientras se introduce texto. Las comprobaciones de estado locales de petición se retardan hasta que se hace una pausa al escribir, dejando el hilo principal de NVDA disponible para la traducción braille, la retroalimentación del editor y el procesamiento normal de teclas.
- Una ventana cancelable de estabilización de finalización evita que un comentario se confunda con el final de una tarea cuando le sigue un trabajo diferido de herramientas.
- Elección entre sonidos originales de clic suave o tonos musicales para cada anuncio, incluso mientras la voz está activada. Los clics son la opción predeterminada.
- Diecisiete firmas de clic percusivas distintas. Los comandos, ediciones de código, búsquedas, pruebas, herramientas, comentarios, atención, finalización, fallo, envío, trabajo en segundo plano y cambios de foco utilizan diferentes ritmos, direcciones de tono y texturas.
- Frecuencia de sondeo en inactividad.
- Niveles de clic Suave, Normal o Alto, con un selector de acciones y botones de vista previa separados para solo sonido y solo voz.
- Redacción de anuncios editable para cada acción, con un botón de restauración y los marcadores de posición `{message}`, `{activity}`, `{seconds}`, y `{duration}` para detalles en vivo.
- Enrutamiento por categoría a todos los canales activados, voz, sonido, braille o desactivado.
- Reparación de configuración, autoprueba de compatibilidad, diagnósticos de soporte depurados, informe de soporte depurado en un archivo elegido por el usuario, importación/exportación de configuración y restablecimiento focalizado del perfil de voz.
- El informe de soporte depurado incluye los tiempos últimos y máximos de análisis de conversación y sondeo de modo en segundo plano, además de recuentos de operaciones lentas. Los tiempos lentos se registran como máximo una vez por minuto y por operación; no se registra ningún texto de mensaje en estas mediciones. Utilice la lista de verificación reproducible en `tests/performance-scenarios.md` al comprobar chats grandes, escritura braille, cambios de modo o el reinicio de NVDA.
- Controles de puntuación de comandos y longitud máxima hablada. Los comandos largos completos siguen estando disponibles para braille y para una acción asignable al portapapeles.
- Recuentos de resultados de búsqueda y actualización para las listas de tareas Recientes y Archivadas.
- Un tiempo de espera máximo de actividad en segundo plano.
- Alertas de alta prioridad de permisos y entrada del usuario.
- Alertas de alta prioridad de límite de uso que detienen la retroalimentación de Trabajo, omiten las URL sin procesar del panel de control e informan de cualquier hora de restablecimiento expuesta, opción de actualización de plan y opción de compra de créditos.
- Nombres de procesos de aplicación configurables para futuros hosts de Codex.
- Un sonido continuo opcional de Trabajo mientras Codex está ocupado. Su intervalo es configurable, comienza tras un retraso de inicio configurable y se pospone ante otros sonidos de progreso para evitar solapamientos. Sigue el estilo seleccionado de Clics o Tonos musicales. Una señal de envío opcional independiente suena inmediatamente cuando se envía una petición con contenido mediante Intro o Enviar.
- Clics ascendentes y descendentes opcionales cuando ChatGPT/Codex gana o pierde el foco. Cuando Alt+F4 cierra ChatGPT sin un evento final de foco de Windows, la señal de inactividad sigue sonando y la voz y el braille de NVDA regresan a la aplicación enfocada anteriormente sin requerir otro Alt+Tab, incluso cuando ChatGPT se cierra durante el inicio antes de que la supervisión de la conversación termine de vincularse. Si esa aplicación también se ha cerrado, el complemento pasa a la ventana de aplicación utilizable más alta restante en lugar de dejar a NVDA en un objeto de ChatGPT inactivo.
- Acceso nativo al navegador integrado que deja sin cambios los roles, estados, acciones, foco, Intro, Espacio, Tab, Shift+Tab, NVDA+Espacio, navegación rápida y listas de elementos de Chromium. No hay ninguna capa de comandos de navegador independiente que aprender.
- Mensajes opcionales de voz y braille **Cargando página** y **Carga completa**. Se utilizan los estados nativos de ocupación del documento y los eventos de progreso cuando están disponibles, con un respaldo acotado para las páginas que no exponen ningún evento final. La retroalimentación nunca analiza la página ni mueve el foco.
- Un botón **Abrir uso y créditos** para el panel oficial de la cuenta de ChatGPT, donde el usuario puede revisar el uso y las opciones de compra disponibles. El complemento nunca realiza una compra automáticamente.

El botón **Probar salidas de anuncios actuales** verifica los canales de voz y braille seleccionados, incluidos los sonidos de progreso.

El botón **Probar sonido de progreso de comando** reproduce directamente el sonido de comando seleccionado, independientemente de la configuración actual de voz.

Elija una acción en **Acción de vista previa** y luego utilice **Vista previa del sonido seleccionado** o **Vista previa de la voz seleccionada** para escuchar solo esa salida. Las vistas previas nunca ejecutan toda la colección de sonidos automáticamente.

Para personalizar un anuncio, seleccione su acción, introduzca la redacción deseada en **Texto del anuncio** y guarde las opciones. Deje el campo en blanco —o elija **Restaurar el anuncio integrado**— para utilizar la redacción estándar del complemento. Por ejemplo, `Sigue ocupado con {activity} después de {duration}` conserva los detalles en vivo del progreso en segundo plano. Utilice `{message}` dondequiera que deba aparecer el texto original de comando o progreso del modo Completo en una redacción personalizada.

La exportación de configuración propone `chatgpt-desktop-access-settings.json` como nombre de archivo; el usuario puede elegir un nombre o ubicación diferente. Los informes de soporte siguen utilizando un nombre de archivo de texto con marca de tiempo. Ningún archivo se crea hasta que el usuario aprueba su cuadro de diálogo Guardar.

Después de que cada versión recién instalada se inicie por primera vez, NVDA abre un resumen conciso de la versión actual y coloca el foco en la parte superior. **Ver notas de la versión actual…** y **Ver historial completo de versiones…** también están disponibles en el panel de Opciones del complemento.

## Gestos de Entrada

Todas las acciones del complemento aparecen en **Menú NVDA > Preferencias > Gestos de Entrada > ChatGPT Desktop Access**. Allí se puede cambiar o eliminar un gesto predeterminado, y se puede asignar un gesto a una acción no asignada si se desea.

### Revisión de mensajes recientes

Control+1 hasta Control+0 revisan los diez mensajes más recientes del usuario o de ChatGPT:

- Control+1 lee el mensaje más reciente.
- Control+2 lee el segundo mensaje más reciente.
- La secuencia continúa hasta Control+0, que lee el décimo mensaje más reciente.

Cada posición es una acción con nombre independiente. Estos atajos funcionan tanto en modo foco como en modo exploración. En conversaciones bifurcadas y laterales, la revisión sigue la rama visible actualmente. El complemento mantiene una pequeña caché de la rama activa para que un comando de revisión no vuelva a analizar todo el árbol de accesibilidad de Chromium.

Para obtener una lista nativa en lugar de la vista web de la conversación, asigne **Abrir los mensajes de la conversación actual en una lista nativa** en Gestos de entrada de NVDA y luego utilice esa asignación mientras ChatGPT tenga el foco. No hay ninguna tecla asignada de forma predeterminada; NVDA+Alt+Shift+R ya es utilizada por NVDA para la compatibilidad de complementos.

La página General de opciones puede habilitar o deshabilitar la lista; está habilitada de forma predeterminada. El cuadro de diálogo muestra hasta los 100 turnos visibles más recientes, del más antiguo al más reciente. Desplácese con las flechas por la lista; Intro mueve al texto completo de solo lectura del mensaje seleccionado. La búsqueda y la actualización están disponibles; Actualizar solicita un nuevo análisis sin bloquear el cuadro de diálogo. Escape cierra el cuadro de diálogo. Los turnos más antiguos permanecen en la vista de conversación de ChatGPT. La lista no envía, edita ni activa mensajes.

### Modo de voz

NVDA+Alt+V inicia o finaliza el modo de voz de ChatGPT. **Silenciar o activar el micrófono de ChatGPT** no tiene un gesto predeterminado; asigne uno en Gestos de Entrada si lo desea.

Versiones anteriores asignaban NVDA+Alt+M a la acción del micrófono. Esa tecla es el comando predeterminado de NVDA **Interactuar con contenido matemático**, por lo que el complemento ya no la reclama. Una asignación de micrófono existente creada por el usuario sigue siendo configurable en Gestos de Entrada.

### Chat y Trabajo

Encima del campo de mensaje de un nuevo chat, ChatGPT tiene un interruptor de **Chat** y **Trabajo**. Las dos configuraciones ofrecen diferentes herramientas y un menú diferente de **Añadir archivos y más**. NVDA+Alt+W informa cuál está seleccionado, por ejemplo «Trabajo seleccionado. Pulsa dos veces rápidamente para cambiar a Chat». Pulsa NVDA+Alt+W dos veces rápidamente para cambiar. La acción se llama **Informar si el campo de mensaje de ChatGPT está configurado en Chat o Trabajo; pulsar dos veces para cambiar**. Si el interruptor no se muestra, como dentro de una conversación existente o en Codex, NVDA lo indica.

### Qué está adjunto al mensaje

NVDA+Alt+A dice qué archivos y herramientas están adjuntos al mensaje que está escribiendo, por ejemplo «Adjunto: informe.pdf. Herramientas: Búsqueda web», o «No hay nada adjunto al mensaje». Herramientas como Búsqueda web, Crear imagen e Investigación profunda aparecen dentro del campo de mensaje, donde NVDA de otro modo solo las lee como un objeto sin etiqueta. La acción se llama **Informar de los archivos y herramientas adjuntos al mensaje de ChatGPT**. Para eliminar un archivo, pulse Tab o muévase en modo exploración hasta su botón **Eliminar** encima del campo de mensaje.

### Selector de modo de ChatGPT y Codex

NVDA+acento grave —la tecla normalmente etiquetada como comilla invertida (`` ` ``)— abre y enfoca el selector de modo nativo de ChatGPT. La acción se llama **Abrir y enfocar el selector de modo de ChatGPT y Codex**.

El comando funciona sin navegar hasta la parte superior de la página. NVDA anuncia el modo actual. Utilice Flecha arriba o Flecha abajo para elegir ChatGPT o Codex y luego pulse Intro.

### Alcance de los gestos y acciones adicionales

Los diez comandos de revisión de mensajes, el comando de modo de voz, la acción del micrófono, el comando del selector de modo, el comando de Chat y Trabajo y el informe de archivos adjuntos están implementados por el módulo de aplicación de ChatGPT. Los gestos predeterminados y asignados por el usuario solo se reclaman mientras ChatGPT o Codex tiene el foco. Fuera de ambos, NVDA y otros complementos siguen teniendo libertad para usar las mismas pulsaciones de teclas.

Las acciones adicionales no asignadas incluyen:

- Repetir la última actividad o desplazarse por el historial de anuncios.
- Mostrar o borrar el historial de anuncios.
- Pausar o reanudar los anuncios.
- Alternar entre salida Mínima y Completa o la ocultación de privacidad.
- Mostrar o copiar diagnósticos y guardar un informe de soporte depurado. El informe nombra la versión instalada de la aplicación ChatGPT, que cambia con cada actualización de ChatGPT.
- Abrir uso y créditos en el panel oficial de la cuenta de ChatGPT.
- Abrir el historial de chat de ChatGPT o Codex con función de búsqueda.

Asigne únicamente los comandos adicionales que desee. El navegador integrado deliberadamente no añade acciones de Gestos de Entrada; utilice en su lugar los comandos normales de navegación web de NVDA.

### Historial de chat

**Abrir historial de chat de ChatGPT o Codex con búsqueda y navegación por flechas** abre un cuadro de diálogo receptivo y específico del modo desde el modo foco o el modo exploración. Escriba para buscar, pulse Tab para pasar de Chats recientes a Chats archivados, utilice Flecha arriba y Flecha abajo para navegar y pulse Intro para abrir el chat seleccionado.

En un chat reciente, Shift+F10 abre un menú contextual de Windows. El foco comienza en **Fijar o desfijar chat**; pulse Flecha abajo para **Archivar chat** y luego pulse Intro para ejecutar la acción nativa seleccionada de ChatGPT. En un chat archivado, Shift+F10 ofrece **Abrir chat archivado**.

Si dos chats recientes tienen el mismo título, el complemento no puede identificar uno de forma segura basándose únicamente en el título. Abrir, Fijar y Archivar le pedirán entonces que elija el chat deseado de la lista nativa de Recientes de ChatGPT; ningún chat se modifica automáticamente.

La región nativa de Recientes de ChatGPT combina chats de ChatGPT y tareas de Codex. El complemento separa esa región utilizando el índice activo de sesiones locales de Codex, de modo que el historial de ChatGPT excluye los títulos de tareas de Codex y el historial de Codex conserva solo los títulos de tareas de Codex.

El complemento lee el control de modo actual expuesto por ChatGPT porque el documento de la aplicación en sí sigue llamándose ChatGPT en ambos modos. Tras un cambio de modo, espera a que la barra lateral unificada se estabilice y confirma dos instantáneas coincidentes antes de separar las entradas. Si el historial se abre demasiado pronto, NVDA informa de que la lista se está actualizando en lugar de mostrar una lista sin clasificar.

Los títulos archivados de Codex se leen desde los metadatos de sesión JSONL locales. Los títulos archivados de ChatGPT provienen únicamente de la vista accesible de Chats archivados de ChatGPT. Si esa vista aún no se ha expuesto, el cuadro de diálogo explica cómo cargarla.

Los controles de mensajes y los paneles de fuentes —incluidos Compartir, Copiar, Leer en voz alta, valoraciones de respuestas, Fuentes, Salidas y Más acciones— se excluyen de ambas listas de historial.

Cuando Recientes ofrece **Mostrar más**, abrir el historial activa ese control nativo de una página en una y espera a que crezca el recuento de elementos accesibles. Cada solicitud está limitada a 20 páginas de diez elementos; vuelva a abrir el historial para continuar si quedan más páginas.

Esta expansión utiliza únicamente el control **Mostrar más** de ChatGPT. No simula el desplazamiento en un diseño de desplazamiento infinito, se detiene si el foco abandona ChatGPT y nunca cambia el estado de archivo simplemente por abrir el historial.

### Controles de la barra de herramientas de petición

El complemento mejora **Añadir archivos y más**, el control de **modelo** y **Cambiar permisos** sin añadir comandos ni gestos. Llegue a ellos mediante la navegación normal con Tab o en modo exploración.

El selector de productos de la aplicación de escritorio cambia entre ChatGPT y Codex. Dentro de ChatGPT, el interruptor separado Chat/Trabajo aparece encima del redactor de un nuevo chat. En Trabajo y Codex, el control de modelo y razonamiento aparece debajo del redactor. El complemento reconoce tanto los nombres completos de modelos con prefijo GPT como etiquetas más cortas como **6 Sol Light** sin mantener una lista fija de modelos. La cuenta y la aplicación determinan qué opciones están disponibles; el complemento no elige un modelo ni un nivel de razonamiento automáticamente.

NVDA otorga a cada control reconocido una descripción concisa mientras conserva su nombre, estado y acción nativos. Para los menús de modelo y permisos, utilice Intro o Espacio para abrir, las teclas de flecha para navegar, Intro para elegir y Escape para cerrar.

El botón **Añadir archivos y más** abre una ventana emergente que ChatGPT añade al final de la página. ChatGPT devuelve entonces el foco del teclado a la petición, donde las teclas de flecha mueven un resaltado que nunca se anuncia, y Tab o Intro elige la opción resaltada sin decir cuál era.

Las opciones de la ventana emergente dependen de dónde se encuentre. En Codex, y en ChatGPT con **Trabajo** seleccionado, enumera elementos como Archivos y carpetas, Objetivo, Modo Plan, Boceto y complementos, y puede terminar con **Escriba para buscar archivos o chats**. En ChatGPT con **Chat** seleccionado, donde el campo de mensaje se llama **Pregunta a ChatGPT**, enumera elementos como Añadir fotos y archivos, Añadir desde la biblioteca, Crear imagen, Búsqueda web, Investigación profunda y Boceto. El complemento gestiona ambos.

Cuando activa **Añadir archivos y más** con las teclas Intro, Espacio o Entrada braille, el complemento lee la ventana emergente y abre una lista de **Añadir archivos y más**. Cada opción aparece primero con el título, luego su descripción y, cuando ChatGPT agrupa las opciones, su sección, por ejemplo «GitHub — Clasificar PR, incidencias, CI y flujos de publicación (Complementos)».

Utilice las teclas de flecha o escriba una primera letra, pulse Intro para elegir, o pulse Tab hasta **Filtrar opciones** y escriba parte de un nombre. Escape cancela y cierra la ventana emergente de ChatGPT.

Después de elegir, el complemento regresa a ChatGPT, vuelve a abrir la ventana emergente y mueve el propio resaltado de ChatGPT hasta su opción fila por fila, comprobando cada paso, y luego la selecciona. Mantenga las manos alejadas del teclado por un momento mientras lo hace. A continuación escuchará qué se añadió a la petición, como «GitHub añadido», o NVDA leerá el cuadro de diálogo que abrió la opción, como **Seleccionar archivos**.

Si no se pueden leer las opciones pero la ventana emergente termina con **Escriba para buscar archivos o chats**, el complemento devuelve en su lugar a NVDA al modo exploración en esa línea. Pulse Flecha arriba para leer las opciones situadas encima y Intro para elegir una.

Si la ventana emergente no aparece, el complemento recurre al control independiente **Adjuntar archivos o conectar aplicaciones** que algunas vistas de Codex muestran debajo de la navegación **Mensajes del usuario**. Si ninguno está presente, la ventana cambia o usted navega fuera, el complemento deja el foco intacto. Solo elige la opción que usted seleccionó y nunca elige un archivo por usted.

#### Los menús de sugerencias «/» y «@»

Escribir «/» o «@» en el campo de mensaje abre un menú de sugerencias de comandos, o de archivos, herramientas y chats. ChatGPT mantiene el foco en el campo de mensaje y mueve un resaltado no anunciado con las teclas de flecha. El complemento indica cuántas sugerencias hay y cuál está resaltada, por ejemplo «Sugerencias: 28. Comentarios, Enviar comentarios sobre este chat, 1 de 28», y anuncia cada una a medida que pulsa Flecha arriba o Flecha abajo, como «Objetivo, Establecer un objetivo a seguir, 2 de 28». Escribir más filtra la lista; el complemento anuncia la nueva primera sugerencia cuando la lista cambia. Pulse Tab o Intro para elegir, o Escape para cerrar.

Desactive esto con **Anunciar los menús de sugerencias «/» y «@» en el campo de mensaje** en la página General de opciones. Si está instalado el complemento independiente Slash Menus, este complemento le cede estos menús para que ambos nunca hablen a la vez.

#### Diagnósticos del menú de archivos adjuntos

Si la ventana emergente sigue sin funcionar, active **Activar registro de diagnóstico depurado** en la categoría Avanzado de opciones y luego abra **Añadir archivos y más**. El complemento registra dónde aparece la ventana emergente: el foco de NVDA, los menús y elementos de menú de UI Automation y cualquier nueva ventana de ChatGPT. A continuación, guarde un informe de soporte desde la página Soporte de opciones; la captura está al final. **Capturar diagnósticos para el menú abierto Añadir archivos y más**, un comando no asignado de Gestos de entrada, captura bajo demanda mientras el menú está abierto. Solo se registran nombres de controles tipo menú, nunca el texto del chat.

Si la aplicación de escritorio no expone un control de archivos adjuntos funcional, abra la conversación en ChatGPT en la web en su navegador y utilice su menú de redacción.

## Acceso al navegador integrado

Cuando ChatGPT expone un contenedor de navegador o vista previa web a través de la accesibilidad de Chromium, el complemento reconoce los objetos situados debajo de ese contenedor nombrado explícitamente. También reconoce un documento web genuino anidado dentro del documento externo de ChatGPT, que es como se exponen algunas pestañas del navegador. El submenú nativo Navegador y sus comandos se excluyen deliberadamente. El complemento no hace clic, no envía formularios, no mueve el foco, no reemplaza roles nativos, no añade descripciones de control ni lee la página en nombre del usuario.

El resultado funciona como una página ordinaria de Chromium en NVDA. En modo foco, utilice Tab y Shift+Tab para moverse entre controles, Intro o Espacio para activar el control nativo actual, y las teclas de flecha donde el control las admita.

Pulse NVDA+Espacio para cambiar entre los modos foco y exploración. En modo exploración, utilice la navegación web normal de NVDA, incluidas H para encabezados, K para enlaces, F para campos de formulario, D para regiones, T para tablas y NVDA+F7 para la Lista de elementos.

Ninguna de estas teclas es interceptada ni simulada por el complemento.

El complemento conserva su búfer virtual original de conversación de Codex mientras el foco está dentro de la página integrada. Esto permite que la supervisión de la actividad de Codex continúe sin tratar la página como una nueva tarea ni desvincularse de la conversación.

La página Acceso al navegador de opciones tiene una opción, habilitada de forma predeterminada, para los mensajes automáticos **Cargando página** y **Carga completa**.

El complemento observa la creación nativa de documentos de Chromium, los cambios de estado de ocupación y el progreso de carga expuesto. Un breve temporizador de estabilización completa las páginas rápidas que no exponen un evento final. Se aplica un respaldo de seguridad más largo mientras Chromium informa que el documento está ocupado.

Los eventos repetidos no repiten el mismo mensaje. Cerrar o salir del navegador integrado cancela el estado de carga pendiente, de modo que una página antigua no pueda anunciar su finalización más tarde. Estos mensajes de estado no cambian el foco, el modo exploración, el cursor de revisión ni la posición de lectura braille.

El historial de anuncios contiene como máximo 20 entradas, permanece en memoria y se borra cuando cambia el documento de Codex supervisado o se cierra NVDA.

## Pruebas y compilación

Ejecute `build.ps1` para ejecutar las pruebas automatizadas, validar la plantilla de traducción y la sintaxis de Python, auditar la coherencia de versiones, dependencias, política de gestos, diseño de archivo, CRC e inventario de sonidos, y crear un paquete reproducible en `outputs`.

GitHub Actions ejecuta las mismas comprobaciones de lanzamiento en envíos (pushes) y solicitudes de extracción (pull requests). Si Python no está disponible como `python`, pase su ejecutable con `-PythonPath`. Archivos fuente idénticos producen una suma de verificación de paquete idéntica, incluso entre copias de Git con LF y CRLF.

Consulte `docs/TESTING.md` para ver la lista de verificación manual de NVDA utilizada antes de publicar una versión. Quienes contribuyan a las traducciones deben consultar `docs/TRANSLATING.md`. Quienes mantengan la Tienda de complementos deben consultar `docs/ADDON_STORE.md`.

## Versionado de lanzamientos

Las versiones del complemento siguen la versión estable actual de NVDA. Con NVDA 2026.2 estable, la línea base es 2026.2.0 y los parches del complemento son 2026.2.1, 2026.2.2, 2026.2.3, 2026.2.4, 2026.2.5, 2026.2.6, 2026.2.7, 2026.2.8, y así sucesivamente. Una versión estable más reciente de NVDA inicia una nueva línea coincidente. Las versiones preliminares (preview) de NVDA no cambian la línea de versión del complemento. Consulte `docs/VERSIONING.md` para obtener todos los detalles.

## Privacidad

El modo Completo puede verbalizar comandos, comentarios, rutas, nombres de archivo, URL y términos de búsqueda. El registro de depuración de NVDA registra la salida hablada, independientemente del registro interno depurado del complemento. Habilite la ocultación o el modo Mínimo antes de compartir un registro de NVDA y revise los registros en busca de datos personales antes de enviarlos a nadie.

La acción de ocultación de privacidad se puede asignar en Gestos de Entrada para cambios temporales de privacidad. La ocultación también se aplica a los comentarios completos conservados para braille, el historial y Copiar el último progreso completo de Codex. Los diagnósticos depurados informan sobre la configuración y el estado de supervisión sin incluir texto de comandos.

## Temporización braille

El progreso utiliza el mecanismo estándar de mensajes flash braille de NVDA. Su duración está controlada por la configuración global de tiempo de espera de mensajes braille de NVDA.

Los mensajes braille rutinarios del complemento se suprimen mientras el foco está en ChatGPT cuando **Mantener estable la lectura de la conversación** está habilitado. Mientras el usuario lee en modo exploración, las actualizaciones ordinarias de regiones activas transmitidas `Respuesta:`, `ChatGPT dijo:` y `Respuesta completa` también se retienen del controlador de salida nativo de NVDA. Esto evita que reemplacen la voz, el cursor de exploración o la ventana de visualización braille.

Los destellos (flashes) de finalización no urgentes del complemento se retienen del braille al mismo tiempo, mientras continúa su salida seleccionada de voz y sonido. La salida de respuestas en modo foco, las solicitudes de permisos, los cuadros de diálogo y las alertas urgentes nunca se suprimen.

La inspección completa del búfer de conversación se pausa mientras se edita la petición y durante tres segundos después de la navegación por teclado o braille en una conversación. Los eventos directos de estado y permisos siguen estando disponibles sin esperar un análisis. Cuando Chromium reemplaza su búfer, el complemento inspecciona solo una cola acotada en lugar de copiar todo el chat.

Después de una respuesta final, los pulsos de Trabajo y los sonidos continuos se pausan mientras el complemento espera cinco segundos por otra operación y requiere que el control Detener esté ausente. Luego confirma que la tarea está inactiva.

Cerrar u ocultar la ventana de ChatGPT durante dos segundos borra la actividad retenida incluso si permanecen procesos auxiliares de Electron. El simple hecho de cambiar a otra aplicación mantiene activa la supervisión.

Mientras se introduce braille contraído en la petición enfocada de ChatGPT, el complemento también protege la composición activa de una nueva palabra frente al evento de cursor retrasado que Chromium puede emitir para la palabra anterior. Esto no cambia las tablas de traducción, no consume gestos braille, no reemplaza el controlador de entrada de NVDA ni se ejecuta fuera de la petición de ChatGPT.

## Instalación y eliminación

Instale el paquete `.nvda-addon` a través del gestor de la Tienda de complementos de NVDA. Reinicie NVDA cuando se le solicite. Elimínelo o deshabilítelo desde el mismo gestor. Las actualizaciones conservan la configuración guardada; las nuevas funciones utilizan valores predeterminados seguros.

## Soporte y compatibilidad

El complemento es compatible con NVDA 2023.1 y versiones posteriores y se ha probado con NVDA 2026.2 estable. Si una actualización de la interfaz de Codex detiene los anuncios, habilite los diagnósticos depurados y proporcione un registro de NVDA después de eliminar claves remotas y otros datos personales.

Después de cada actualización de ChatGPT, el complemento comprueba una vez que aún puede encontrar el campo de mensaje, **Añadir archivos y más** y el interruptor de modo de ChatGPT y Codex. El resultado aparece en el registro de NVDA y en la línea **Comprobación de compatibilidad de ChatGPT** del informe de soporte. Si falta algo después de una actualización, NVDA indica una vez que es posible que algunas funciones del complemento no funcionen hasta que se actualice el complemento.

## Licencia

ChatGPT Desktop Access es software libre distribuido bajo la Licencia Pública General de GNU (GNU General Public License), versión 2 o, a su elección, cualquier versión posterior. Consulte `LICENSE.txt` para conocer los términos completos de la licencia.
