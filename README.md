
<div align="center">
  <table>
    <tr>
      <td><img src="https://housebarber.cl/wp-content/uploads/2022/11/HOUSE-BARBER22.1_Mesa-de-trabajo-1-e1678206242931.png" alt="Descripción de la imagen" width="200" height="auto"></td>
      <td><img src="https://t3.ftcdn.net/jpg/05/41/66/02/360_F_541660295_yGWCQXja2mLAR0V8osB9eKWgFS9v2Gkq.jpg" alt="Descripción de la imagen 2" width="350" height="auto"></td>
    </tr>
  </table>
</div>



# Proyecto-Arqui-Software Barber House
Bienvenido al proyecto Barber House. A continuación, te proporcionamos una guía paso a paso para ejecutar y poner en marcha el proyecto.

## Pre-requisitos
 Asegúrate de tener instalado Docker y Python en tu máquina.

## 1. Ejecutar Docker compose
Para iniciar todos los servicios utilizando Docker Compose, primero navega al directorio del proyecto donde se encuentra el archivo ``docker-compose.yml``. Luego, abre una terminal en ese directorio y ejecuta el siguiente comando:

* Si estas en windows, ejecuta el siguiente comando en la terminal 
  ```bash 
      docker-compose up -d
  ```
* Si estas en linux, ejecuta el siguiente comando en la terminal 
  ```bash
    docker compose up -d
  ```
   *Asegúrate de que todos los servicios se inicien correctamente sin errores.*

## 2. **Instalar dependencias**

  En la misma terminal, antes de ejecutar cualquier parte del proyecto, es esencial instalar todas las dependencias requeridas. Para esto ejecuta:
    
      pip install -r requirements.txt
    

## 3. **Ejecutar los servicios de lógica**
  Con las dependencias ya instaladas, puedes iniciar los servicios de lógica del proyecto. Ejecuta:
    
    python ejectServices.py
    

## 4. **Ejecutar la interfaz gráfica**
  Con los servicios de lógica en funcionamiento, lanza la interfaz gráfica para interactuar con el proyecto. Ejecuta:
    
    python interface.py
    

## Uso

  Una vez que todo esté en marcha, sigue las indicaciones en la interfaz gráfica para utilizar las funcionalidades del proyecto Barber House.
