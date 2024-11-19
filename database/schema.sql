/*CREATE TABLE Planilhas (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    objetivo REAL NOT NULL,
    data_submissao TEXT NOT NULL,
    plan_desc TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);
*/

CREATE TABLE Lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_participante TEXT /*trocar por um id de verdade*/,
    data DATE,
    descricao TEXT,
    valor REAL
);