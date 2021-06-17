from cadastro_geral import *
from mysql.connector import Error
import mysql.connector

class NotasFiscais:
    def __init__(self, numero_nota, termino_tratamento, cro, cpf_paciente, tratamento_realizado):
        self.numero_nota = numero_nota
        self.termino_tratamento = termino_tratamento
        self.cro = cro
        self.cpf_paciente = cpf_paciente
        self.tratamento_realizado = tratamento_realizado

    def formata_data(self):
        return f'{self.termino_tratamento[6:]}-{self.termino_tratamento[3:5]}-{self.termino_tratamento[:2]}'

    def conectar_mysql(self):
        try:
            global conn
            conn = mysql.connector.connect(host='localhost', database='consultorio', user='###',
                                           password='###')
        except Error as erro:
            print("Erro de Conexão!")

    def gravar_mysql(self):
        try:
            self.conectar_mysql()
            sql_insert = f"""INSERT INTO NF (NUMERO_NOTA, TERMINO_TRATAMENTO, CRO, CPF_PACIENTE, TRATAMENTO) 
            VALUES ('{self.numero_nota}','{self.formata_data()}','{self.cro}', '{self.cpf_paciente}', 
            '{self.tratamento_realizado}') """
            cursor = conn.cursor()
            cursor.execute(sql_insert)
            conn.commit()
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

    def update_mysql(self):
        try:
            self.conectar_mysql()
            sql_update = f"""UPDATE NF A INNER JOIN DENTISTAS B ON A.CRO = B.CRO 
            INNER JOIN tabela_de_precos C ON A.TRATAMENTO = C.DESCRICAO 
            INNER JOIN clientes D on A.CPF_PACIENTE = D.CPF 
            SET 
            A.NOME_DENTISTA = B.NOME,
            A.VALOR_TRATAMENTO = C.PRECO,
            A.NOME_PACIENTE = D.NOME
            where numero_nota = '{self.numero_nota}';"""
            cursor = conn.cursor()
            cursor.execute(sql_update)
            conn.commit()
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

def cadastra_nf():
    print("** Digite as informações abaixo para cadastrar a nota fiscal **\n")

    numero_nota = input("Número da nota fiscal: ").strip()

    termino_tratamento = input("Data do término do tratamento: ")

    cro = input("CRO do dentista que realizou o tratamento: ").strip()

    cpf = input("CPF do paciente: ").strip()

    descricao_tratamento = input("Descrição do tratamento: ")

    nf = NotasFiscais(numero_nota, termino_tratamento, cro, cpf, descricao_tratamento)

    print("As informações estão corretas?")
    print(f"Numero da nota: {numero_nota}  Término do tratamento: {termino_tratamento}  CRO: {cro}\n"
          f"CPF do paciente: {cpf}  Descrição do tratamento: {descricao_tratamento}")

    confirma(nf)
    nf.update_mysql()

cadastra_nf()
