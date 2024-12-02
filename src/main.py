from database.database import Database
from database.scripts_sql.create_tables_connectme import query_create_tables
from data_generator.generate_data import DataGenerator

database = Database()

def create_db():
    database.open_connection()
    database.execute_query(query_create_tables)
    database.close_connection()

def generate_data():
    database.open_connection()
    generator = DataGenerator(database=database)

    usuarios = generator.populate_usuario(n=1000)
    grupos = generator.populate_grupo(n=200, usuarios=usuarios)
    temas = generator.populate_tema(n=500)

    generator.populate_interesse_tema(usuarios=usuarios, temas=temas)
    usuario_grupo = generator.populate_usuario_grupo(usuarios=usuarios, grupos=grupos)
    conexoes = generator.populate_conexao(usuarios=usuarios)

    post_u = generator.populate_post_u(usuarios=usuarios)
    generator.populate_curtida_u(num_curtidas=2000, conexoes=conexoes, posts=post_u)
    generator.populate_mensagem_u(num_mensagens=3000, conexoes=conexoes)
    generator.populate_comentario_u(num_comentarios=2000, conexoes=conexoes, posts=post_u)

    post_g = generator.populate_post_g(usuario_grupo=usuario_grupo, grupos=grupos)
    generator.populate_curtida_g(num_curtidas=2000, usuario_grupo=usuario_grupo, posts=post_g)

    database.close_connection()

create_db()
generate_data()