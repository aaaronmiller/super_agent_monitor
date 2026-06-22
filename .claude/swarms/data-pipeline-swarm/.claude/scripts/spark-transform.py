#!/usr/bin/env python3
from pyspark.sql import SparkSession

def run_transform(input_path, output_path):
    spark = SparkSession.builder.appName("DataPipeline").getOrCreate()
    df = spark.read.parquet(input_path)
    # Transformations here
    df.write.mode("overwrite").parquet(output_path)
    spark.stop()
