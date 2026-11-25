# AssetDesk · Proyecto inicial del wizard Java

Aplicación de consola Java 8 para asignar y devolver recursos compartidos. Incluye cuatro recursos en memoria, salida JSON y cinco pruebas JUnit 4. Cada ejecución parte del mismo catálogo.

Commons Lang está en el ámbito `test` como ejercicio de remediación. Consulta [LAB.md](../LAB.md) para revisar el aviso y actualizar la versión con Bob.

```bash
mvn clean verify
java -jar target/assetdesk.jar list
java -jar target/assetdesk.jar demo
```

El wizard **Java Upgrade** se utilizará para pasar a Java 21. **Java Unit Testing** permitirá ampliar la cobertura del servicio. No se necesita servidor de aplicaciones ni base de datos externa.

Datos iniciales: cuatro recursos, tres disponibles y uno asignado. La demo asigna el recurso 1, muestra dos disponibles y lo devuelve, recuperando los tres disponibles.
