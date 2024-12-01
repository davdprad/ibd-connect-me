from database.database import Database
from database.scripts_sql.create_tables_connectme import query_create_tables
from data_generator.generate_data import DataGenerator

database = Database()

def delete_db():
    database.open_connection()
    database.execute_query("DROP DATABASE connect_me;")
    database.close_connection()

def create_db():
    database.open_connection()
    database.execute_query(query_create_tables)
    database.close_connection()

def generate_data():
    database.open_connection()
    generator = DataGenerator(database=database)

    usuarios = generator.populate_usuario(n=1000)
    grupos = generator.populate_grupo(n=200, usuarios=usuarios)
    temas = generator.populate_tema(n=200)

    database.close_connection()

# delete_db()
# create_db()
generate_data()