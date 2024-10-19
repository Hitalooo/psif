
CREATE TABLE Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    eh_admin BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE Eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_evento TEXT NOT NULL,
    data_pgmt INTEGER NOT NULL,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Planilhas (
    id_planilha INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    total REAL NOT NULL,
    data_submissao TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);


CREATE TABLE Itens (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_planilha INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (id_planilha) REFERENCES Planilhas(id_planilha)
);