CREATE TABLE planilhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    objetivo REAL NOT NULL,
    data_ini DATE NOT NULL,
    data_fim DATE NOT NULL
);

CREATE TABLE lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_planilha INTEGER NOT NULL,
    id_participante TEXT NOT NULL /*trocar por um id de verdade*/,
    data DATE NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,

    FOREIGN KEY (id_planilha) REFERENCES planilhas
);

