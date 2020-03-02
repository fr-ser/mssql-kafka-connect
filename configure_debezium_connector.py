import json

import requests

from config import (
    KAFKA_SERVER,
    KAFKA_CONNECT_URL,
    DB_DEBEZIUM_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def add_connector(connector_name, table_whitelist, database=None, server_name=None):
    database = database if database else DB_NAME
    server_name = server_name if server_name else "main"

    resp = requests.post(
        f"{KAFKA_CONNECT_URL}/connectors",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "name": connector_name,
            "config": {
                "connector.class": "io.debezium.connector.sqlserver.SqlServerConnector",
                "tasks.max": "1",
                "database.server.name": server_name,
                "database.hostname": DB_DEBEZIUM_HOST,
                "database.port": DB_PORT,
                "database.user": DB_USER,
                "database.password": DB_PASSWORD,
                "database.dbname": database,
                "database.history.kafka.bootstrap.servers": KAFKA_SERVER,
                "database.history.kafka.topic": "__debezium.dbhistory",
                "table.whitelist": table_whitelist,
            }
        }),
        timeout=10,
    )

    resp.raise_for_status()
    print(f"Kafka Connect {connector_name} created successfully")


def delete_connector(connector_name):
    resp = requests.delete(
        f"{KAFKA_CONNECT_URL}/connectors/{connector_name}",
        timeout=10,
    )

    resp.raise_for_status()
    print(f"Kafka Connect {connector_name} deleted successfully")


if __name__ == "__main__":
    connector_name = "DEBEZIUM_CONNECTOR"
    table_whitelist = r"dbo[.]one,dbo[.]two"

    add_connector(connector_name, table_whitelist)
