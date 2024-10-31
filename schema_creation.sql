create database mahanlake;

CREATE EXTERNAL TABLE IF NOT EXISTS radar_measurements (
    time DOUBLE,
    azimuth DOUBLE,
    elevation DOUBLE,
    range DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION './radar/'
TBLPROPERTIES (
    'skip.header.line.count'='1',
    'serialization.encoding'='UTF-8'
)CREATE EXTERNAL TABLE IF NOT EXISTS flights (
    time DOUBLE,
    x DOUBLE,
    y DOUBLE,
    z DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION './flights/'
TBLPROPERTIES (
    'skip.header.line.count'='1',
    'serialization.encoding'='UTF-8'
);





