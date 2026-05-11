genealogy-app/
│
├── app/
│   ├── main.py
│
│   ├── ui/              # telas (Qt)
│   ├── controllers/     # conecta UI com lógica
│   ├── services/        # regras de negócio
│   ├── repositories/    # acesso a dados
│   ├── models/          # ORM (SQLAlchemy)
│   ├── database/
│
├── requirements.txt


Pessoa{
    id*,
    nome,
    sobrenome,
    genero,
    pai,
    mae,
}

Evento{
    id*,
    tipo,
    dia,
    mes,
    ano,
    exato,
    pessoa,
    local,
}

Local{
    id,
    cidade,
    estado,
    regiao,
    pais
}

Uniao{
    id,
    pai
    mae
    diaCasamento,
    mesCasamento,
    anoCasamento,
    local_casamento_fk
}