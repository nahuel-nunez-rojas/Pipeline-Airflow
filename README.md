# Pipeline en Airflow

Este proyecto es una práctica con [Franca Tortarolo](https://github.com/FrancaTortaroloo) para aprender a usar Airflow y automatizar flujos de trabajo con datos. La idea fue utilizar la API de OpenWeatherMap, transformar los datos obtenidos y cargarlos en un bucket S3 de AWS.

### Contexto

El primer obstáculo fue no tener al menos 2 núcleos en una instancia EC2 de AWS ya que era un requisito para correr Airflow, así que decidí usar Docker y desplegar un contenedor con Ubuntu para simular un entorno EC2 de manera local.

## 💻 Pasos

### 1. Desplegar el contenedor en Docker

- Crear un contenedor con Ubuntu y abrir el puerto 8080 para que lo use Airflow:
  ```bash
  docker run -d -p 8080:8080 --name airflow_container ubuntu
  ```

![Imagen de Docker](https://github.com/nahuel-nunez-rojas/Pipeline-Airflow/blob/main/images/conteiner.png)

### 2. Actualizar el sistema e instalar dependencias

- Dentro del contenedor, ejecutar:
  ```bash
  apt update
  apt install python3-pip -y
  apt install python3.12-venv -y
  apt install awscli -y
  ```

### 3. Configurar el entorno e instalar librerías

- Crear y activar un entorno virtual:
  ```bash
  python3 -m venv airflow-env
  source airflow-env/bin/activate
  ```
- Instalar librerías:
  ```bash
  pip install pandas s3fs apache-airflow
  ```

### 4. Iniciar Airflow

- Ejecutar el servicio:
  ```bash
  airflow standalone
  ```
- Acceder desde el navegador en: http://localhost:8080

![Imagen de Airflow](https://github.com/nahuel-nunez-rojas/Pipeline-Airflow/blob/main/images/airflow.png)

### 5. Conectar desde VS Code al contenedor y escribir el código en Python

### 6. Crear el bucket en S3 y configurar credenciales de AWS

- Configurar AWS CLI:
  ```bash
  aws configure
  ```
- Obtener token de sesión:
  ```bash
  aws sts get-session-token
  ```

![Imagen de S3](https://github.com/nahuel-nunez-rojas/Pipeline-Airflow/blob/main/images/bucket.png)

### 7. Probar el pipeline y verificar la carga en S3

- Ejecutar el pipeline y comprobar que el archivo se haya subido correctamente al bucket y Airflow debe mostrar que la tarea se completó sin errores.



## English Version:
# Airflow Pipeline

This project is a practice to learn how to use Airflow and automate data workflows. The main idea was to use the OpenWeatherMap API, transform the obtained data, and load it into an S3 bucket on AWS.

### Context

The first challenge was not having at least 2 cores on an EC2 instance in AWS, so I decided to use Docker and deploy a container with Ubuntu to simulate an EC2 environment locally.

## 💻 Steps

### 1. Deploy the container in Docker

- Create a container with Ubuntu and open port 8080 for Airflow:
  ```bash
  docker run -d -p 8080:8080 --name airflow_container ubuntu
  ```

### 2. Update the system and install dependencies

- Inside the container, run:
  ```bash
  apt update
  apt install python3-pip -y
  apt install python3.12-venv -y
  apt install awscli -y
  ```

### 3. Set up the environment and install libraries

- Create and activate a virtual environment:
  ```bash
  python3 -m venv airflow-env
  source airflow-env/bin/activate
  ```
- Install libraries:
  ```bash
  pip install pandas s3fs apache-airflow
  ```

### 4. Start Airflow

- Run the service:
  ```bash
  airflow standalone
  ```
- Access from the browser at: http://localhost:8080

### 5. Connect from VS Code to the container and write the Python code

### 6. Create the S3 bucket and configure credentials

- Configure AWS CLI:
  ```bash
  aws configure
  ```
- Get session token:
  ```bash
  aws sts get-session-token
  ```

### 7. Test the pipeline and verify the upload to S3

- Run the pipeline and check if the file has been uploaded to the bucket.

