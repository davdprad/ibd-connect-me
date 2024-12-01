from faker import Faker
from database.database import Database
import random

class DataGenerator:
    def __init__(self, database: Database):
        """
        Initialize the Faker instance and the Database connection.
        """
        fake = Faker()
        fake.unique.clear()
        self.fake = fake

        self.db = database

    def generate_unique_username(self, existing_usernames):
        """
        Gera um username único garantindo que não esteja na lista de usernames existentes.
        """
        faker = Faker()
        while True:
            username = faker.user_name()
            if username not in existing_usernames:
                return username

    def populate_usuario(self, n):
        print("\nPopulando usuario...")
        
        usuarios = []
        existing_usernames = []
        
        for _ in range(n):
            user_id = self.generate_unique_username(existing_usernames)
            nome = self.fake.name()
            foto = self.fake.image_url()
            localizacao = self.fake.city()
            biografia = self.fake.text(max_nb_chars=200)
            data_nasc = self.fake.date_of_birth(minimum_age=18, maximum_age=70)
            usuarios.append((user_id, nome, foto, localizacao, biografia, data_nasc))
            existing_usernames.append(user_id)

        self.db.execute_query("""
            INSERT INTO usuario (user_id, nome, foto, localizacao, biografia, data_nasc)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, usuarios)

        return [user[0] for user in usuarios]

    def populate_grupo(self, n, usuarios):
        grupos = []
        for _ in range(n):
            nome = self.fake.word().capitalize() + " Group"
            biografia = self.fake.text(max_nb_chars=150)
            user_id_criou = random.choice(usuarios)
            grupos.append((nome, biografia, user_id_criou))

        self.db.execute_query("""
            INSERT INTO grupo (nome, biografia, user_id_criou)
            VALUES (%s, %s, %s)
        """, grupos)

        results = self.db.execute_query("SELECT grupo_id FROM grupo")
        return [row[0] for row in results]

    def populate_usuario_grupo(self, usuarios, grupos):
        usuario_grupo = []
        for _ in range(len(usuarios) * 2):
            user_id = random.choice(usuarios)
            grupo_id = random.choice(grupos)
            data_ingresso = self.fake.date_between(start_date='-1y', end_date='today')
            usuario_grupo.append((user_id, grupo_id, data_ingresso))

        self.db.execute_query("""
            INSERT INTO usuario_grupo (user_id, grupo_id, data_ingresso)
            VALUES (%s, %s, %s)
        """, usuario_grupo)

        return usuario_grupo

    def populate_conexao(self, num_por_usuario, usuarios):
        print("\nPopulando conexao...")

        conexoes = set()

        for usuario in usuarios:
            for _ in range(num_por_usuario):
                user_id_1 = usuario
                user_id_2 = usuario
                while user_id_1 == user_id_2:
                    user_id_2 = random.choice(usuarios)
                
                data_amizade = self.fake.date_between(start_date='-1y', end_date='today')
                
                while ((user_id_1, user_id_2, data_amizade) in conexoes) or ((user_id_2, user_id_1, data_amizade) in conexoes):
                    user_id_2 = random.choice(usuarios)
                    while user_id_1 == user_id_2:
                        user_id_2 = random.choice(usuarios)

                conexoes.add((user_id_1, user_id_2, data_amizade))

        self.db.execute_query("""
            INSERT INTO conexao (user_id_1, user_id_2, data_amizade)
            VALUES (%s, %s, %s)
        """, list(conexoes))

        return list(conexoes)

    def populate_post_u(self, num_posts_user, usuarios):
        print("\nPopulando post_u...")

        posts = []
        posts_db = []

        for usuario in usuarios:
            for i in range(num_posts_user):
                post_id = i
                tipo_midia = random.choice(["image", "video", "text"])
                conteudo = self.fake.text(max_nb_chars=300)
                user_id_postou = usuario
                data_post = self.fake.date_between(start_date='-1y', end_date='today')

                posts.append((post_id, tipo_midia, conteudo, user_id_postou, data_post))
                posts_db.append((tipo_midia, conteudo, user_id_postou, data_post))

        self.db.execute_query("""
            INSERT INTO post_u (tipo_midia, conteudo, user_id_postou, data_post)
            VALUES (%s, %s, %s, %s)
        """, posts_db)

        return posts
    
    def populate_curtida_u(self, num_curtidas, conexoes, posts):
        print("\nPopulando curtida_u...")

        curtidas = []

        for _ in range(num_curtidas):
            conexao = random.choice(conexoes)
            user_id = conexao[0]
            
            posts_possiveis = [post for post in posts if post[3] == user_id]
            post = random.choice(posts_possiveis)
            post_id = post[0]

            data_curtida = self.fake.date_between(start_date='-1y', end_date='today')
            curtidas.append((user_id, post_id, data_curtida))

        self.db.execute_query("""
            INSERT INTO curtida_u (user_id, post_id, data_curtida)
            VALUES (%s, %s, %s)
        """, curtidas)

    def populate_mensagem_u(self, num_mensagens, conexoes):
        print("\nPopulando mensagem_u...")

        mensagens_u = []

        for _ in range(num_mensagens):
            conexao = random.choice(conexoes)
            user_id_envia, user_id_recebe = random.sample(conexao[:2], 2)
            conteudo = self.fake.text(max_nb_chars=150)
            data_envio = self.fake.date_between(start_date=conexao[2], end_date='today')
            data_recebimento = self.fake.date_between(start_date=data_envio, end_date="+5d") if random.random() > 0.5 else None
            
            mensagens_u.append((conteudo, user_id_envia, user_id_recebe, data_envio, data_recebimento))

        self.db.execute_query("""
            INSERT INTO mensagem_u (conteudo, user_id_envia, user_id_recebe, data_envio, data_recebimento)
            VALUES (%s, %s, %s, %s, %s)
        """, mensagens_u)

    def populate_post_g(self, n, usuarios):
        posts = []
        for _ in range(n):
            tipo_midia = random.choice(["image", "video", "text"])
            conteudo = self.fake.text(max_nb_chars=300)
            user_id_postou = random.choice(usuarios)
            
            grupo_user = self.db.execute_query(f"""SELECT grupo_id FROM usuario_grupo WHERE user_id = {user_id_postou} ORDER BY RAND() LIMIT 1""")
            grupo_id = grupo_user[0]

            data_ingresso = self.db.execute_query(f"""SELECT data_ingresso FROM usuario_grupo WHERE user_id = '{user_id_postou}'""")
            data_post = self.fake.date_between(start_date=data_ingresso, end_date='today')

            posts.append((tipo_midia, conteudo, user_id_postou, grupo_id, data_post))

        self.db.execute_query("""
            INSERT INTO post_g (tipo_midia, conteudo, user_id_postou, grupo_id, data_post)
            VALUES (%s, %s, %s, %s, %s)
        """, posts)

        results = self.db.execute_query("SELECT post_id FROM post_g")
        return [row[0] for row in results]

    def populate_curtida_g(self, usuarios, posts):
        curtidas = []
        for user_id in usuarios:
            post_id = random.choice(posts)
            data_curtida = self.fake.date_this_year()
            curtidas.append((user_id, post_id, data_curtida))

        self.db.execute_query("""
            INSERT INTO curtida_g (user_id, post_id, data_curtida)
            VALUES (%s, %s, %s)
        """, curtidas)

    def populate_mensagem_g(self, usuarios, num_mensagens):
        mensagens = []
        for _ in range(num_mensagens):
            user_id_envia = random.choice(usuarios)
            user_id_recebe = random.choice(usuarios)

            while user_id_envia == user_id_recebe:
                user_id_recebe = random.choice(usuarios)
            
            conteudo = self.fake.text(max_nb_chars=150)
            data_envio = self.fake.date_this_year()
            data_recebimento = self.fake.date_between(start_date=data_envio, end_date="+5d") if random.random() > 0.5 else None
            
            mensagens.append((conteudo, user_id_envia, user_id_recebe, data_envio, data_recebimento))

        self.db.execute_query("""
            INSERT INTO mensagem_g (conteudo, user_id_envia, user_id_recebe, data_envio, data_recebimento)
            VALUES (%s, %s, %s, %s, %s)
        """, mensagens)

    def populate_tema(self, n):
        temas = [(self.fake.word().capitalize(),) for _ in range(n)]
        self.db.execute_query("INSERT INTO tema (nome) VALUES (%s)", temas)

        results = self.db.execute_query("SELECT tema_id FROM connect_me.tema")
        return [row[0] for row in results]

    def populate_interesse_tema(self, usuarios, temas):
        interesses = []
        for user_id in usuarios:
            tema_id = random.choice(temas)
            interesses.append((user_id, tema_id))

        self.db.execute_query("""
            INSERT INTO interesse_tema (user_id, tema_id)
            VALUES (%s, %s)
        """, interesses)
