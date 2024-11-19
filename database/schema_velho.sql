
CREATE TABLE Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    eh_admin BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE Eventos (
    even_id INTEGER PRIMARY KEY AUTOINCREMENT,
    even_nome TEXT NOT NULL,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Planilhas (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    objetivo REAL NOT NULL,
    data_submissao TEXT NOT NULL,
    plan_desc TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Itens (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_planilha INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    pagmt_dt DATE NOT NULL,
    FOREIGN KEY (id_planilha) REFERENCES Planilhas(id_planilha)
);