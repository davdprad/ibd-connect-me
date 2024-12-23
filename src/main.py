from database.database import Database
from database.scripts_sql.create_tables_connectme import query_create_tables
from data_generator.generate_data import DataGenerator

class Main:
    database = Database()

    def __init__(self):
        # Criar as tabelas do banco connect_me caso ainda não existam
        # self.create_db()

        # Gerar os dados ficticios para o banco de dados.
        self.generate_data()

    def create_db(self):
        """
        Cria as tabelas necessárias.
        """
        self.database.open_connection()
        print("\nCriando as tabelas do banco...")

        self.database.execute_query(query_create_tables)
        print("Tabelas criadas com sucesso!\n")

        self.database.close_connection()

    def generate_data(self):
        """
        Gera os dados necessários para o banco connect_me.
        """
        # Abre a conexão com o banco de dados.
        self.database.open_connection()
        
        # Instancia a classe geradora de dados
        generator = DataGenerator(database=self.database)

        # Gera os dados ficticios para o banco de dados.
        usuarios = generator.populate_usuario(n=1000)
        grupos = generator.populate_grupo(n=200, usuarios=usuarios)
        temas = generator.populate_tema(n=500)

        usuario_grupo = generator.populate_usuario_grupo(usuarios=usuarios, grupos=grupos)
        conexoes = generator.populate_conexao(usuarios=usuarios)
        generator.populate_interesse_tema(usuarios=usuarios, temas=temas)
        generator.populate_grupo_tema(grupos=grupos, temas=temas)

        post_u = generator.populate_post_u(usuarios=usuarios)
        generator.populate_curtida_u(num_curtidas=2000, conexoes=conexoes, posts=post_u)
        generator.populate_mensagem_u(num_mensagens=3000, conexoes=conexoes)
        generator.populate_comentario_u(num_comentarios=2000, conexoes=conexoes, posts=post_u)

        post_g = generator.populate_post_g(usuario_grupo=usuario_grupo, grupos=grupos)
        generator.populate_curtida_g(num_curtidas=2000, usuario_grupo=usuario_grupo, posts=post_g)
        generator.populate_mensagem_g(usuario_grupo=usuario_grupo, num_mensagens=3000)
        generator.populate_comentario_g(num_comentarios=2000, usuario_grupo=usuario_grupo, posts=post_g)
        
        # Fecha a conexão com o banco de dados.
        self.database.close_connection()

main = Main()
