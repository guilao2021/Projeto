create database consultorio character set = utf8;

USE consultorio;

CREATE TABLE clientes 
(ID INT AUTO_INCREMENT, 
NOME VARCHAR(50) NOT NULL,
CPF VARCHAR(11) NOT NULL,
TELEFONE VARCHAR(11) NOT NULL,
TELEFONE2 VARCHAR(11),
ENDERECO VARCHAR(100) NOT NULL,
BAIRRO VARCHAR(50),
ESTADO VARCHAR(50) DEFAULT 'São Paulo',
CIDADE VARCHAR(50) DEFAULT 'São Paulo',
CEP VARCHAR (8) NOT NULL,
PROFISSAO VARCHAR(50),
DATA_NASCIMENTO DATE,
NACIONALIDADE VARCHAR(50) DEFAULT 'Brasileiro(a)',
ESTADO_CIVIL VARCHAR(15),
INDICACAO VARCHAR(50),
PRIMARY KEY(ID);

CREATE TABLE dentistas
(CRO VARCHAR(50) NOT NULL,
NOME VARCHAR(100) NOT NULL,
ENDERECO VARCHAR(100),
TELEFONE VARCHAR(11),
DATA_ADMISSAO DATE,
COMISSAO FLOAT,
PRIMARY KEY(CRO);

CREATE TABLE NF
(NUMERO_NOTA INT NOT NULL,
TERMINO_TRATAMENTO DATE NOT NULL,
CRO VARCHAR(10) NOT NULL,
NOME_DENTISTA VARCHAR(100),
CPF_PACIENTE VARCHAR(11),
NOME_PACIENTE VARCHAR(100),
TRATAMENTO VARCHAR(100) NOT NULL,
VALOR_TRATAMENTO DECIMAL(7,2));

ALTER TABLE NF ADD CONSTRAINT PRIMARY KEY(NUMERO_NOTA);

ALTER TABLE NF ADD CONSTRAINT FK_CRO
FOREIGN KEY(CRO) 
REFERENCES DENTISTAS(CRO);

ALTER TABLE NF ADD CONSTRAINT FK_TRATAMENTO
FOREIGN KEY(TRATAMENTO) 
REFERENCES tabela_de_precos(DESCRICAO);

CREATE TABLE tabela_de_precos 
(DESCRICAO VARCHAR(150),
PRECO FLOAT,
primary key(DESCRICAO));

INSERT INTO tabela_de_precos (DESCRICAO, PRECO)
VALUES
('Pulpotomia (extração da polpa do dente)', 159.00),
('Apicectomia (remoção da ponta ou ápice da raiz)', 410.00),
('Apicetomia de molar', 485.00),
('Restauração com compósito (1 face)', 134.00),
('Restauração de Dente da Frente com resina', 134.00),
('Restauração de dente quebrado preço', 134.00),
('Obturação - Restauração de molar ou pré-molar com amálgama (1 face)'	, 106.00),
('Lente de contato dental', 1136.00),
('Obturação valor simples', 106.00),
('Extração de Dente', 162.00),
('Extrair dente do siso', 223.00),
('Extração de Dente de Leite', 90.00),
('Preço de canal dentário - dente incisivo (Tratamento endodôntico)', 431.00),
('Preço canal dentario - dente molar (Tratamento endodôntico)', 732.00),
('Tratamento periodontal (por sessão)', 140.00),
('Cirurgia de gengiva', 291.00),
('Manutenção de espaço', 420.00),
('Placa de mordida', 350.00),
('Aparelho ortodôntico fixo estético', 1187.00),
('Clareamento de dente desvitalizado', 377.00),
('Clareamento com moldeiras personalizadas (cada arcada)' , 539.00),
('Polimento coronário (2 arcadas)', 114.00),
('Limpeza dental preço (raspagem do tártaro)', 405.00);

CREATE TABLE tratamentos
(ID INT NOT NULL, 
INICIO_TRATAMENTO TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
TERMINO_TRATAMENTO TIMESTAMP,
INTERRUPCAO_TRATAMENTO DATE,
PA_MAX VARCHAR(5),
PA_MIN VARCHAR(5),
SENSIBILIDADE_ANESTESIA VARCHAR(5) NOT NULL,
SENSIBILIDADE_ANTIBIOTICOS VARCHAR(50),
DENTE VARCHAR(50) NOT NULL,
TRATAMENTO_REALIZADO VARCHAR(100));

ALTER TABLE tratamentos ADD CONSTRAINT FK_ID 
FOREIGN KEY (ID) REFERENCES clientes(ID);
