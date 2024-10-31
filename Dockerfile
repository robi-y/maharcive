version: '3.8'

services:
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

  trino:
    image: trinodb/trino
    ports:
      - "8080:8080"
    volumes:
      - ./trino/catalog:/etc/trino/catalog
    depends_on:
      - minio

  jupyter:
    image: jupyter/pyspark-notebook
    ports:
      - "8888:8888"
    environment:
      JUPYTER_ENABLE_LAB: "yes"
    volumes:
      - jupyter_data:/home/jovyan/work
      - ./flows:/home/jovyan/flows

  prefect:
    image: prefecthq/prefect:2-python3.9
    ports:
      - "4200:4200"
    volumes:
      - ./flows:/opt/prefect/flows
      - prefect_data:/root/.prefect
    environment:
      - PREFECT_UI_API_URL=http://localhost:4200/api
      - PREFECT_API_URL=http://localhost:4200/api
      - PREFECT_SERVER_API_HOST=0.0.0.0
    command: prefect server start

  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: prefect
      POSTGRES_PASSWORD: prefect
      POSTGRES_DB: prefect
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  minio_data:
  jupyter_data:
  prefect_data:
  postgres_data: