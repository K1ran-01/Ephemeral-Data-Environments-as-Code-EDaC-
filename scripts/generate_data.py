import os
from pyspark.sql import SparkSession
import dbldatagen as dg

# Grab the catalog name from an environment variable
# In a CI/CD pipeline, this would be set from the Terraform output
catalog_name = os.getenv("CATALOG_NAME", "sandbox_pr_local")
schema_name = "default" # Or any other schema you create

# Initialize Spark Session
spark = (
    SparkSession.builder
    .appName("EdaDataGen")
    .getOrCreate()
)

# Define the data generation spec for the customers table
customer_data_spec = (
    dg.DataGenerator(spark, name="customer_data", rows=1000, partitions=4)
    .withColumn("customer_id", "long", minValue=1, uniqueValues=1000)
    .withColumn("first_name", "string", template=r"\w")
    .withColumn("last_name", "string", template=r"\w")
    .withColumn("email", "string", template=r"\\w.\\w@\\w.com")
    .withColumn("reg_date", "timestamp", begin="2022-01-01 00:00:00", end="2023-12-31 23:59:59", interval="1 minute")
)

# Generate the customers DataFrame
df_customers = customer_data_spec.build()

# Define the data generation spec for the orders table
# This demonstrates referential integrity by using the customer_id from the customers table
order_data_spec = (
    dg.DataGenerator(spark, name="order_data", rows=10000, partitions=8)
    .withColumn("order_id", "long", minValue=10000, uniqueValues=10000)
    .withColumn("customer_id", "long", data_source=df_customers, data_source_column="customer_id")
    .withColumn("order_date", "timestamp", begin="2023-01-01 00:00:00", end="2023-12-31 23:59:59", interval="1 minute")
    .withColumn("amount", "double", minValue=1.0, maxValue=1000.0, step=0.01)
)

# Generate the orders DataFrame
df_orders = order_data_spec.build()

# In a real run, you would write these to the ephemeral catalog
# For demonstration, we'll just show the schema and a few rows
print("Generated Customers Schema:")
df_customers.printSchema()
df_customers.show(5)

print("Generated Orders Schema:")
df_orders.printSchema()
df_orders.show(5)

# Example of writing to the catalog
df_customers.write.format("delta").mode("overwrite").saveAsTable(f"{catalog_name}.{schema_name}.customers")
df_orders.write.format("delta").mode("overwrite").saveAsTable(f"{catalog_name}.{schema_name}.orders")

print(f"Data generation script finished. In a real run, data would be written to catalog: '{catalog_name}'")
