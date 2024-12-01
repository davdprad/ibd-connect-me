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
    # grupos = generator.populate_grupo(n=200, usuarios=usuarios)
    temas = generator.populate_tema(n=500)
    
    generator.populate_interesse_tema(usuarios=usuarios, temas=temas)

    # usuario_grupo = generator.populate_usuario_grupo(usuarios=usuarios, grupos=grupos)

    conexoes = generator.populate_conexao(num_por_usuario=3, usuarios=usuarios)
    post_u = generator.populate_post_u(num_posts_user=3, usuarios=usuarios)
    generator.populate_curtida_u(num_curtidas=2000, conexoes=conexoes, posts=post_u)
    generator.populate_mensagem_u(num_mensagens=2000, conexoes=conexoes)
    generator.populate_comentario_u(num_comentarios=2000, conexoes=conexoes, posts=post_u)

    database.close_connection()

# delete_db()
create_db()
generate_data()