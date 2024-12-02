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
        print("\nPopulando grupo...")
        
        grupos_db = []
        grupos = []

        for i in range(n):
            nome = self.fake.word().capitalize() + " Group"
            biografia = self.fake.text(max_nb_chars=150)
            user_id_criou = random.choice(usuarios)
            data_criacao = self.fake.date_between(start_date='-2y', end_date='today')
            grupos.append((i + 1, nome, biografia, user_id_criou, data_criacao))
            grupos_db.append((nome, biografia, user_id_criou, data_criacao))

        self.db.execute_query("""
            INSERT INTO grupo (nome, biografia, user_id_criou, data_criacao)
            VALUES (%s, %s, %s, %s)
        """, grupos_db)

        return grupos

    def populate_usuario_grupo(self, usuarios, grupos):
        print("\nPopulando usuario_grupo...")

        usuario_grupo = []

        for grupo in grupos:
            usuarios_disponiveis = usuarios.copy()

            user_criador = grupo[3]
            grupo_id = grupo[0]
            data_ingresso_criador = grupo[4]
            usuario_grupo.append((user_criador, grupo_id, data_ingresso_criador))
            usuarios_disponiveis.remove(user_criador)

            for _ in range(random.randint(3, 10)):
                user_id = random.choice(usuarios_disponiveis)
                data_ingresso = self.fake.date_between(start_date=data_ingresso_criador, end_date='today')
                usuarios_disponiveis.remove(user_id)
                usuario_grupo.append((user_id, grupo_id, data_ingresso))

        self.db.execute_query("""
            INSERT INTO usuario_grupo (user_id, grupo_id, data_ingresso)
            VALUES (%s, %s, %s)
        """, usuario_grupo)

        return usuario_grupo

    def populate_conexao(self, usuarios):
        print("\nPopulando conexao...")

        conexoes = []
        conexoes_existentes = []

        for usuario in usuarios:
            usuarios_possiveis = usuarios.copy()
            usuarios_possiveis.remove(usuario)

            for _ in range(random.randint(3, 10)):
                user_id_1 = usuario
                user_id_2 = random.choice(usuarios_possiveis)
                data_amizade = self.fake.date_between(start_date='-1y', end_date='today')
                
                while (user_id_1, user_id_2) in conexoes_existentes or (user_id_2, user_id_1) in conexoes_existentes:
                    usuarios_possiveis.remove(user_id_2)
                    user_id_2 = random.choice(usuarios_possiveis)
                
                conexoes.append((user_id_1, user_id_2, data_amizade))
                conexoes_existentes.append((user_id_1, user_id_2))

        self.db.execute_query("""
            INSERT INTO conexao (user_id_1, user_id_2, data_amizade)
            VALUES (%s, %s, %s)
        """, conexoes)

        return conexoes

    def populate_post_u(self, usuarios):
        print("\nPopulando post_u...")

        posts = []
        posts_db = []
        i = 1

        for usuario in usuarios:
            for _ in range(random.randint(3, 10)):
                post_id = i
                tipo_midia = random.choice(["image", "video", "text"])
                conteudo = self.fake.text(max_nb_chars=300)
                user_id_postou = usuario
                data_post = self.fake.date_between(start_date='-1y', end_date='today')
                i = i + 1
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
        curtidas_existentes = []

        for _ in range(num_curtidas):
            conexao = random.choice(conexoes)
            user_id = conexao[0]
            
            posts_possiveis = [post for post in posts if post[3] == user_id]
            post = random.choice(posts_possiveis)
            post_id = post[0]

            data_curtida = self.fake.date_between(start_date=conexao[2], end_date='today')

            while (user_id, post_id) in curtidas_existentes:
                conexao = random.choice(conexoes)
                user_id = conexao[0]

                posts_possiveis = [post for post in posts if post[3] == user_id]
                post = random.choice(posts_possiveis)
                post_id = post[0]

            curtidas.append((user_id, post_id, data_curtida))
            curtidas_existentes.append((user_id, post_id))

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

    def populate_comentario_u(self, num_comentarios, conexoes, posts):
        print("\nPopulando comentario_u...")

        comen = []

        for _ in range(num_comentarios):
            conexao = random.choice(conexoes)
            user_id = conexao[0]
            
            posts_possiveis = [post for post in posts if post[3] == user_id]
            post = random.choice(posts_possiveis)
            post_id = post[0]

            data_curtida = self.fake.date_between(start_date=conexao[2], end_date='today')
            conteudo = self.fake.text(max_nb_chars=300)

            comen.append((user_id, post_id, conteudo, data_curtida))

        self.db.execute_query("""
            INSERT INTO comentario_u (user_id, post_id, conteudo, data_postagem)
            VALUES (%s, %s, %s, %s)
        """, comen)

    def populate_post_g(self, usuario_grupo, grupos):
        print("\nPopulando post_g...")

        posts = []
        posts_db = []
        i = 0

        for grupo in grupos:
            users_possiveis = [tuple for tuple in usuario_grupo if tuple[1] == grupo[0]]

            for _ in range(random.randint(3, 10)):
                tipo_midia = random.choice(["image", "video", "text"])
                conteudo = self.fake.text(max_nb_chars=300)
                user_postou = random.choice(users_possiveis)
                user_id_postou = user_postou[0]
                grupo_id = grupo[0]
                data_post = self.fake.date_between(start_date=user_postou[2], end_date='today')

                i = i + 1
                posts_db.append((tipo_midia, conteudo, user_id_postou, grupo_id, data_post))
                posts.append((i, tipo_midia, conteudo, user_id_postou, grupo_id, data_post))

        self.db.execute_query("""
            INSERT INTO post_g (tipo_midia, conteudo, user_id_postou, grupo_id, data_post)
            VALUES (%s, %s, %s, %s, %s)
        """, posts_db)

        return posts

    def populate_curtida_g(self, num_curtidas, usuario_grupo, posts):
        print("\nPopulando curtida_g...")

        curtidas = []
        curtidas_existentes = []

        for _ in range(num_curtidas):
            usuario_grupo_da_vez = random.choice(usuario_grupo)
            user_id = usuario_grupo_da_vez[0]
            grupo_id = usuario_grupo_da_vez[1]
            
            posts_possiveis = [post for post in posts if post[4] == grupo_id]
            post = random.choice(posts_possiveis)
            post_id = post[0]

            data_curtida = self.fake.date_between(start_date=usuario_grupo_da_vez[2], end_date='today')

            while (user_id, post_id) in curtidas_existentes:
                usuario_grupo_da_vez = random.choice(usuario_grupo)
                user_id = usuario_grupo_da_vez[0]
                grupo_id = usuario_grupo_da_vez[1]
                
                posts_possiveis = [post for post in posts if post[4] == grupo_id]
                post = random.choice(posts_possiveis)
                post_id = post[0]

            curtidas.append((user_id, post_id, data_curtida))
            curtidas_existentes.append((user_id, post_id))

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
        print("\nPopulando tema...")

        temas = []

        for _ in range(n):
            temas.append((self.fake.word().capitalize(),))

        self.db.execute_query("""INSERT INTO tema (nome) VALUES (%s)""", temas)

        return list(range(1, n + 1))

    def populate_interesse_tema(self, usuarios, temas):
        print("\nPopulando interesse_tema...")

        interesses = []

        for user_id in usuarios:
            temas_disponiveis = temas.copy()
            num_interesses = random.randint(1, 3)

            for _ in range(num_interesses):
                tema_id = random.choice(temas_disponiveis)
                interesses.append((user_id, tema_id))
                temas_disponiveis.remove(tema_id)

        self.db.execute_query("""
            INSERT INTO interesse_tema (user_id, tema_id)
            VALUES (%s, %s)
        """, interesses)
