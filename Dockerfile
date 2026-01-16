FROM apache/airflow:2.8.1

USER root

# Install Java 
RUN apt-get update \
    && apt-get install -y openjdk-17-jdk \
    && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Download PostgreSQL JDBC driver inside Airflow container
RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.6.0.jar \
    -o /opt/airflow/postgresql-42.6.0.jar
