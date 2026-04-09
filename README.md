# 🐾 Centro de Adopción "Nancy"

Sistema de gestión para un **Centro de Adopción de Mascotas** desarrollado con Python y Flask. Este proyecto permite visualizar perros disponibles y registrar adopciones de forma segura.

## Capturas del Proyecto
![Catálogo](catalogo.png)
![Formulario](formulario.png)
![Registro](regristro.png)
![Historial](historial.png)

## Funcionalidades
* **Catálogo:** Visualización de perritos desde MySQL.
* **Adopciones:** Formulario para registrar nuevos dueños.
* **Registro de Adopción:** Uso de SQL para asegurar que los datos se guarden correctamente.
* **Historial:** Registro de todas las adopciones realizadas.

## Tecnologías
* **Lenguaje:** Python 3
* **Framework:** Flask
* **Base de Datos:** MySQL
* **Sistema Operativo:** Linux
## Pilares del Proyecto
1. Integridad de Datos (Transacciones SQL)
Lo más importante del sistema es su fiabilidad. Al procesar una adopción, el código realiza una Transacción Atómica:

**Registra al adoptante en la base de datos.

**Actualiza el estado del perro a "Adoptado" automáticamente.

**Seguridad: Si alguno de estos pasos falla, el sistema cancela todo (ROLLBACK) para evitar que un perro quede en un "limbo" informativo.

2. Seguridad y Control
**Prevención de Inyecciones SQL: Se utilizan consultas parametrizadas para evitar que usuarios malintencionados manipulen la base de datos a través de los formularios.

**Filtrado Dinámico: El catálogo solo consulta y muestra registros donde el campo adopted es igual a 0, asegurando que el usuario final solo vea opciones reales.

3. Desarrollo en Entorno Linux
El proyecto está optimizado para entornos Linux, utilizando herramientas de terminal para la gestión de dependencias y el control de versiones con Git, lo que facilita su despliegue en servidores reales.

## Componentes Principales
**Backend: Lógica de rutas y conexión a base de datos en Python.

**Frontend: Plantillas dinámicas en HTML que responden a los datos del servidor.

**Base de Datos: Estructura relacional en MySQL para el almacenamiento persistente.
