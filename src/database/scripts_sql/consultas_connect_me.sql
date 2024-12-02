USE connect_me;

-- 1) Informações de um determinado usuário
SELECT *
FROM usuario
WHERE user_id = 'USUARIO_ID';

-- 2) Lista de conexões de um determinado usuário
SELECT
	u.nome,
    u.foto,
    u.localizacao,
    u.biografia,
    u.data_nasc
FROM usuario u
JOIN conexao c
	ON (u.user_id = c.user_id_1 OR u.user_id = c.user_id_2)
WHERE
	(c.user_id_1 = 'USUARIO_ID' OR c.user_id_2 = 'USUARIO_ID') AND
    u.user_id <> 'USUARIO_ID';
    
-- 3) Postagens de um determinado usuário
SELECT 
    post_id,
    tipo_midia,
    conteudo,
    data_post,
    'usuario' AS origem
FROM post_u
WHERE user_id_postou = 'USUARIO_ID'
UNION ALL
SELECT 
    post_id,
    tipo_midia,
    conteudo,
    data_post,
    'grupo' AS origem
FROM post_g
WHERE user_id_postou = 'USUARIO_ID'
ORDER BY data_post DESC;

-- 4) Listar 20 postagens mais recentes feitas em um grupo especifico
SELECT *
FROM post_g
WHERE grupo_id = 'GRUPO_ID'
ORDER BY data_post DESC
LIMIT 20;

-- 5) Listar as 10 mensagens mais recentes trocadas por dois usuários
SELECT 
    mensagem_id,
    conteudo,
    user_id_envia,
    user_id_recebe,
    data_envio,
    data_recebimento
FROM mensagem_u
WHERE
    (user_id_envia = 'USUARIO_ID_1' AND user_id_recebe = 'USUARIO_ID_2') OR 
    (user_id_envia = 'USUARIO_ID_2' AND user_id_recebe = 'USUARIO_ID_1')
ORDER BY data_envio DESC
LIMIT 10;

-- 6) Usuários cujos nomes contenham a string fornecida
SELECT *
FROM usuario
WHERE nome LIKE '%STRING%';

-- 7) Listar 5 posts com maior interação
SELECT 
    post_id,
    COUNT(*) AS total_interacoes
FROM (
    SELECT post_id 
    FROM curtida_u
    WHERE data_curtida >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT post_id
    FROM curtida_g
    WHERE data_curtida >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT post_id
    FROM comentario_u
    WHERE data_postagem >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT post_id
    FROM comentario_g
    WHERE data_postagem >= NOW() - INTERVAL 7 DAY
) AS interacoes
GROUP BY post_id
ORDER BY total_interacoes DESC
LIMIT 5;

-- 8) Listar quantos usuarios interagiram com um determinado post
SELECT 
    COUNT(DISTINCT user_id) AS total_usuarios_interagiram
FROM (
    SELECT user_id
    FROM curtida_u
    WHERE 
        post_id = 'POST_ID'
        AND data_curtida >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT user_id
    FROM curtida_g
    WHERE 
        post_id = 'POST_ID'
        AND data_curtida >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT user_id
    FROM comentario_u
    WHERE 
        post_id = 'POST_ID'
        AND data_postagem >= NOW() - INTERVAL 7 DAY
    UNION ALL
    SELECT user_id
    FROM comentario_g
    WHERE
		post_id = 'POST_ID'
        AND data_postagem >= NOW() - INTERVAL 7 DAY
) AS interacoes;
