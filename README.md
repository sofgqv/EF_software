# EF_software

## Pregunta 3

- Se requiere realizar un cambio en el software para que soporte un valor máximo de 200 soles a transferir por día.
- Qué cambiaría en el código (Clases / Métodos) - No implementación
- Nuevos casos de prueba a adicionar.
- Cuánto riesgo hay de “romper” lo que ya funciona?


### ¿Qué cambiaría en el código?

Podríamos añadir en la clase `Cuenta` un atributo llamado `daily` que iría sumando los valores de las operaciones del día de cada usuario.

Al deployar la app en sitios como Heroku (con heroku scheduler) o AWS (EventBridge) se podría programar un comando que se active a las 11:59:59 de cada día y que reinicie el contador de `daily` a cero para todos los usuarios.

Además, antes de hacer cualquier operación se revisaría que la suma del valor de la transacción + daily sea menor a 200, sino no se permitirá hacer el pago.

### Nuevos casos de prueba

- Intentar hacer una transacción con el valor de `daily` en 50 y hacer una transacción de 100, que sería el caso de **exito** (200).
- Intentar hacer una transacción con el valor de `daily` en 170 y hacer una transacción de 35, que sería el caso de **error**.
- Intentar hacer una transacción con el valor de `daily` en 170 y hacer una transacción de 35 a las 11:59:00, que sería el caso de **error**, y volver a hacer la misma transacción a las 00:01:00 del día siguiente para revisar que funcione (sería un poco más complejo que el unit testing que se hace ahora pero considero que es posible y necesario para revisar el funcionamiento.)

### Riesgos

Creo que siempre hay un riesgo de "romper" algo que si funciona en casos de actualizar el código, por lo mismo se hace testing antes de hacer cualquier tipo de deploy o actualización. Sin embargo, los cambios son relativamentes mínimos, probablemente la mayor complejidad sea en relación a la programación del reinicio de `daily` y prevenir al usuario de hacer transacciones durante este periodo de transición (se podría colocar el servicio como no disponible por breves momentos, por ejemplo). Creo que si se hace un testing exhaustivo, el riesgo será mínimo!
