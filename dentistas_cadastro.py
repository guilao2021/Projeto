from cadastro_geral import *
from mysql.connector import Error
import mysql.connector

class Dentistas(Cadastro):
    def __init__(self, cro, nome, cep, numero_complemento, telefone, data, comissao):
        super().__init__(nome, telefone, cep, numero_complemento, data)
        self.cro = cro
        self.comissao = comissao

    def cro_format(self):
        cro_formatado = f"{self.cro[0:2]}.{self.cro[2:]}"
        return cro_formatado

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
            sql_insert = f"""INSERT INTO dentistas (cro, nome, endereco, telefone, data_admissao, comissao)           
            VALUES ('{self.cro}','{self.nome}','{self.get_endereco()}','{self.telefone}','{self.formata_data()}',
            '{self.comissao}')"""
            cursor = conn.cursor()
            cursor.execute(sql_insert)
            conn.commit()
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

def pede_cro():
    cro = input("CRO: ")
    cro_record = ''.join(filter(lambda i: i if i.isdigit() else None, cro))
    return cro_record

def pede_comissao():
    comissao = input("Taxa de comissão: ")
    comissao_format = f'{comissao[0]}.{comissao[2:]}'
    comissao_record = float(comissao_format)
    return comissao_record

def cadastra_prestador():
    print("** Para realizar o cadastro do(a) prestador(a), digite as informações pedidas abaixo **\n")

    cro = pede_cro()

    nome_prestador = input("Nome: ").title().strip()

    cep = pede_cep()

    numero = input("Número: ").strip()
    complemento = input("Complemento: ").strip().capitalize()
    numero_complemento = formata_numero_complemento(numero, complemento)

    pergunta_telefone = input("Telefone: ").strip()
    telefone = pede_telefone(pergunta_telefone)

    data_adm = input("Data de admissão: ").strip()
    data_formatada = f'{data_adm[:2]}/{data_adm[3:5]}/{data_adm[6:]}'

    comissao = pede_comissao()

    prestador = Dentistas(cro, nome_prestador, cep, numero_complemento, telefone, data_adm, comissao)

    print('\n As informações estão corretas?')
    print(f"CRO: {prestador.cro_format()}  Nome: {nome_prestador}  Endereço: {prestador.get_endereco()}  "
          f"Telefone: {prestador.valida_telefone()}\nData de admissão: {data_formatada}  Comissão: {comissao}")

    confirma(prestador)

teste = cadastra_prestador()
