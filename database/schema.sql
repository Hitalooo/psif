
CREATE TABLE Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    eh_admin BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE Eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_evento TEXT NOT NULL,
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


CREATE TABLE PlanilhaItens (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_planilha INTEGER NOT NULL,
    nome_item TEXT NOT NULL,
    valor_item REAL NOT NULL,
    FOREIGN KEY (id_planilha) REFERENCES Planilhas(id_planilha)
);


CREATE TABLE Juros (
    id_juros INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    objetivo REAL NOT NULL,
    taxa_juros REAL NOT NULL,
    periodo_meses INTEGER NOT NULL,
    valor_total REAL NOT NULL,
    mensalidade REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);
