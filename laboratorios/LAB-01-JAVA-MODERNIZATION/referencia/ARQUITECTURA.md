# AssetDesk · Diagramas de referencia

Estos diagramas describen el código inicial. El destino conserva las funciones, con Java 21 como objetivo. El equipo contrasta cualquier diferencia con los cambios reales del wizard.

## Componentes

```mermaid
flowchart LR
    User[Usuario en terminal] --> Main[AssetDeskApplication]
    Main --> Service[ResourceService]
    Service --> Model[SharedResource]
    Service --> Store[(Catálogo en memoria)]
    Main --> Gson[Gson]
    Gson --> JSON[Salida JSON]
    Tests[ResourceServiceTest / JUnit 4] -. valida .-> Service
```

## Modelo

```mermaid
classDiagram
    class SharedResource {
        long id
        String name
        String category
        Date registeredAt
        String status
        String assignedTo
    }
    class ResourceService {
        findAll()
        findById(id)
        assign(id, team)
        release(id)
        summary()
    }
    class AssetDeskApplication {
        main(args)
    }
    AssetDeskApplication --> ResourceService
    ResourceService --> SharedResource
```

## Asignación

```mermaid
sequenceDiagram
    actor User as Usuario
    participant App as AssetDeskApplication
    participant S as ResourceService
    participant R as SharedResource
    User->>App: Ejecutar demo
    App->>S: assign(1, Equipo Demo)
    S->>S: Validar equipo e ID
    S->>R: Comprobar AVAILABLE
    S->>R: Cambiar a ASSIGNED
    S-->>App: Copia del recurso
    App->>S: release(1)
    S->>R: Cambiar a AVAILABLE y vaciar equipo
    S-->>App: Copia del recurso
    App-->>User: JSON con estados y contadores
```

## Estados

```mermaid
stateDiagram-v2
    [*] --> AVAILABLE
    AVAILABLE --> ASSIGNED: asignar a equipo
    ASSIGNED --> AVAILABLE: devolver
```

El diagrama de progreso que Bob pueda emitir describe las tareas de su workflow. Se conserva aparte de estos diagramas de arquitectura y dominio.
