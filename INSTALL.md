## INSTALL

**Requisitos Previos**
Antes de proceder con la instalación y uso de la aplicación, asegúrese de tener instalado Docker y Docker Compose en su sistema. Estos serán necesarios para construir y ejecutar los contenedores de la aplicación.

**Instalación y Configuración**
1. **Clonar el Repositorio:**
   Clone el repositorio de la aplicación a su máquina local utilizando Git.

2. **Configuración del Entorno:**
   Configure las variables de entorno necesarias, incluyendo la clave secreta para JWT, mediante un archivo `.env`. Esto incluye configuraciones para la base de datos y el servidor Redis.

3. **Construcción de Contenedores:**
   Navegue al directorio donde se encuentran los archivos de Docker Compose y ejecute el siguiente comando para construir los contenedores:
   ```bash
   docker-compose up --build
   ```

**Uso de la Aplicación**
Una vez que los contenedores estén en funcionamiento, puede iniciar la aplicación del cliente utilizando el siguiente comando:
```bash
python3 client.py --email [su_email] --password [su_contraseña]
```
Donde `[su_email]` y `[su_contraseña]` deben ser reemplazados por sus credenciales reales. Este comando iniciará la interfaz de cliente, desde donde podrá realizar las operaciones mencionadas anteriormente.

**Notas Adicionales**
- Asegúrese de que los puertos utilizados por la aplicación (por ejemplo, el puerto 5500 para el servidor) estén libres y no bloqueados por otras aplicaciones.
