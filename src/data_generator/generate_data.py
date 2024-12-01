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

    def populate_post_u(self, n, usuarios):
        posts = []
        for _ in range(n):
            tipo_midia = random.choice(["image", "video", "text"])
            conteudo = self.fake.text(max_nb_chars=300)
            user_id_postou = random.choice(usuarios)
            data_post = self.fake.date_between(start_date='-1y', end_date='today')
            posts.append((tipo_midia, conteudo, user_id_postou, data_post))

        self.db.execute_query("""
            INSERT INTO post_u (tipo_midia, conteudo, user_id_postou, data_post)
            VALUES (%s, %s, %s, %s)
        """, posts)

    def populate_post_m(self, n, usuarios, grupos):
        posts = []
        for _ in range(n):
            tipo_midia = random.choice(["image", "video", "text"])
            conteudo = self.fake.text(max_nb_chars=300)
            user_id_postou = random.choice(usuarios)
            grupo_id = random.choice(grupos)
            data_post = self.fake.date_between(start_date='-1y', end_date='today')
            posts.append((tipo_midia, conteudo, user_id_postou, grupo_id, data_post))

        self.db.execute_query("""
            INSERT INTO post_m (tipo_midia, conteudo, user_id_postou, grupo_id, data_post)
            VALUES (%s, %s, %s, %s, %s)
        """, posts)

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
