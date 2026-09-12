import psycopg


def get_connection():
    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="intelligence_graph",
        user="postgres",
        password="tripitashashi"
    )

    return connection