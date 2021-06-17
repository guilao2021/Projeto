from cadastro_geral import *
import mysql.connector
from mysql.connector import Error

class TabelaPreco:
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor

    def conectar_mysql(self):
        try:
            global conn
            conn = mysql.connector.connect(host='localhost', database='consultorio', user='###', password='###')
        except Error as erro:
            print("Erro de Conexão")

    def gravar_mysql(self):
        try:
            self.conectar_mysql()
            sql_insert = f"""INSERT INTO tabela_de_precos (DESCRICAO, PRECO)
            VALUES ('{self.descricao}','{self.valor}') """
            cursor = conn.cursor()
            cursor.execute(sql_insert)
            conn.commit()
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

def boas_vindas():
    print("** Para realizar o cadastro de tratamentos, digite as informações pedidas abaixo **\n")

def pede_descricao():
    tratamento = input("Descrição do tratamento: ").capitalize()
    return tratamento

def pede_valor():
    valor = float(input("Valor do tratamento: "))
    return valor

def cadastra():
    boas_vindas()

    descricao = pede_descricao()

    valor = pede_valor()

    tratamento = TabelaPreco(descricao, valor)
    print('\n As informações estão corretas?')
    print(f"Descrição: {descricao}  Valor: {valor}")

    confirma(tratamento)

cadastra()
