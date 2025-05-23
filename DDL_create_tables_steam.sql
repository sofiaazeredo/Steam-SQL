CREATE schema steam;

set search_path=steam;

CREATE TABLE Familia
(
  IDFamilia VARCHAR(8) NOT NULL,
  NomeDaFamilia VARCHAR(100) NOT NULL,
  PRIMARY KEY (IDFamilia)
);

CREATE TABLE Usuario
(
  IDUsuario VARCHAR(9) NOT NULL,
  DataDeCriacao DATE NOT NULL,
  NomeDePerfil VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL,
  NumeroDeTelefone INT,
  SaldoNaCarteira money NOT NULL,
  IDFamilia VARCHAR(8) NOT NULL,
  PRIMARY KEY (IDUsuario), 
  FOREIGN KEY (IDFamilia) REFERENCES Familia(IDFamilia)

);

CREATE TABLE Distribuidor
(
  IDNomeDIST VARCHAR(100) NOT NULL,
  DescricaoDIST VARCHAR(300),
  LinkParaSiteDistribuidor VARCHAR(300),
  PRIMARY KEY (IDNomeDIST)
);

CREATE TABLE Desenvolvedor
(
  IDNomeDEV VARCHAR(100) NOT NULL,
  DescricaoDEV VARCHAR(300),
  LinkParaSiteDesenvolvedor VARCHAR(300),
  PRIMARY KEY (IDNomeDEV)
);

CREATE TABLE Jogo
(
  IDJogo VARCHAR(7) NOT NULL,
  NomeJogo VARCHAR(100) NOT NULL,
  DataDeLancamento  DATE NOT NULL,
  Preco	money NOT NULL,
  DescricaoJogo VARCHAR(300) NOT NULL,
  PRIMARY KEY (IDJogo)
);

CREATE TABLE Genero
(
  IDJogo VARCHAR(7) NOT NULL,
  Genero VARCHAR(100) NOT NULL,
  FOREIGN KEY (IDJogo) REFERENCES Jogo(IDJogo)
);

CREATE TABLE Transacao
(
  IDTransacao VARCHAR(7) NOT NULL,
  IDJogo VARCHAR(7) NOT NULL,
  IDUsuario VARCHAR(9) NOT NULL,
  DataDaTransacao DATE NOT NULL,
  ValorMovimentado money NOT NULL,
  Desconto NUMERIC(5,2) CHECK (Desconto >= 0 AND Desconto <= 100),
  PRIMARY KEY (IDTransacao),
  FOREIGN KEY (IDJogo) REFERENCES Jogo(IDJogo),
  FOREIGN KEY (IDUsuario) REFERENCES Usuario(IDUsuario)
);

CREATE TABLE Avaliacao
(
  IDAvaliacao VARCHAR(8) NOT NULL,
  IDJogo VARCHAR(7) NOT NULL,
  IDUsuario VARCHAR(9) NOT NULL,
  Conteudo VARCHAR(300) NOT NULL,
  ClasseAvaliativa VARCHAR(50) NOT NULL,
  PRIMARY KEY (IDAvaliacao),
  FOREIGN KEY (IDJogo) REFERENCES Jogo(IDJogo),
  FOREIGN KEY (IDUsuario) REFERENCES Usuario(IDUsuario)
);