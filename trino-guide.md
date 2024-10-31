# Interacting with Trino from Terminal: CSV File Handling

## Prerequisites
1. Install Trino CLI
2. Configure MinIO as an object storage catalog
3. Prepare your CSV files

## Step-by-Step Guide

### 1. Download Trino CLI
```bash
# Download Trino CLI
curl -L https://repo1.maven.org/maven2/io/trino/trino-cli/429/trino-cli-429-executable.jar > trino
chmod +x trino
```

### 2. Create MinIO Catalog Configuration
Create a file `trino/catalog/minio.properties` with:
```properties
connector.name=hive-hadoop2
hive.metastore.uri=thrift://localhost:9083
hive.s3.endpoint=http://minio:9000
hive.s3.aws-access-key=minioadmin
hive.s3.aws-secret-key=minioadmin
hive.s3.path-style-access=true
```

### 3. Creating Schemas and Tables

#### Connect to Trino
```bash
./trino --server localhost:8080 --catalog minio
```

#### Create Schema
```sql
CREATE SCHEMA IF NOT EXISTS minio.mydata;
USE minio.mydata;
```

#### Create Table from CSV
```sql
CREATE TABLE customers (
    id INT,
    name VARCHAR,
    email VARCHAR,
    age INT
) WITH (
    format = 'CSV',
    external_location = 's3a://data/customers/'
);
```

### 4. Uploading CSV Files

#### Prepare MinIO Bucket
```bash
# Create bucket via MinIO CLI or web interface
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/data/customers
```

#### Upload CSV
```bash
# Upload CSV to MinIO
mc cp customers.csv local/data/customers/
```

### 5. Querying Data
```sql
-- Basic Select
SELECT * FROM customers LIMIT 10;

-- Aggregations
SELECT age, COUNT(*) 
FROM customers 
GROUP BY age 
ORDER BY COUNT(*) DESC;
```

### 6. Advanced CSV Handling

#### Specify CSV Options
```sql
CREATE TABLE products (
    product_id INT,
    name VARCHAR,
    price DECIMAL(10,2)
) WITH (
    format = 'CSV',
    external_location = 's3a://data/products/',
    skip.header.line.count = 1,  -- Skip header row
    delimiter = ';'  -- Non-standard delimiter
);
```

### Troubleshooting Tips
- Ensure MinIO and Trino are running
- Check network connectivity
- Verify file permissions
- Use `SHOW TABLES` to list tables
- Use `DESCRIBE table_name` to show table schema

### Common Errors
- `Connection refused`: Check Docker network
- `Access denied`: Verify MinIO credentials
- `Invalid schema`: Double-check table definition
```

### Example Workflow Script
<antArtifact identifier="trino-upload-script" type="application/vnd.ant.code" language="bash" title="Trino CSV Upload Automation Script">
#!/bin/bash

# Configuration
MINIO_ENDPOINT="http://localhost:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
BUCKET_NAME="data"
LOCAL_CSV_DIR="./csv_files"

# Setup MinIO alias
mc alias set local ${MINIO_ENDPOINT} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}

# Create bucket if not exists
mc mb -p local/${BUCKET_NAME}

# Upload all CSVs from local directory
for csv_file in ${LOCAL_CSV_DIR}/*.csv; do
    filename=$(basename "$csv_file")
    tablename="${filename%.*}"
    
    # Upload to MinIO
    mc cp "$csv_file" "local/${BUCKET_NAME}/${tablename}/"
    
    # Create Trino table (you'd customize this part)
    ./trino --execute "
    CREATE TABLE IF NOT EXISTS minio.mydata.${tablename} (
        -- Define your schema here based on CSV structure
    ) WITH (
        format = 'CSV',
        external_location = 's3a://${BUCKET_NAME}/${tablename}/'
    );
    "
done

echo "CSV files uploaded and tables created successfully!"