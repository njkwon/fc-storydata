#bin/bash

wget https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.14.4/snowflake-jdbc-3.14.4.jar
wget https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.12/2.15.0-spark_3.4/spark-snowflake_2.12-2.15.0-spark_3.4.jar

sudo mv *.jar /usr/lib/spark/jars/
