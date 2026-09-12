from src.database.postgres import get_connection


connection = get_connection()

print("Connected to PostgreSQL successfully!")

connection.close()