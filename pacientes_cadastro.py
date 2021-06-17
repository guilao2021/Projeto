from cadastro_geral import *
from CPF import Documento
from Telefones import Telefone
from mysql.connector import Error
import mysql.connector

class Clientes(Cadastro):
    def __init__(self, nome, cpf, telefone, telefone2, data, cep, numero_complemento, profissao,
                 nacionalidade, estado_civil, indicacao):
        super().__init__(nome, telefone, cep, numero_complemento, data)
        self._cpf = cpf
        self.telefone2 = telefone2
        self.profissao = profissao
        self.nacionalidade = nacionalidade
        self.estado_civil = estado_civil
        self.indicacao = indicacao

    def valida_cpf(self):
        if self._cpf == " ":
            return self._cpf
        cpf = Documento.analisa_doc(self._cpf)
        return cpf

    def valida_telefone2(self):
        if self.telefone2 == " ":
            return self.telefone2
        telefone2 = Telefone(self.telefone2)
        return telefone2

    def gravar_mysql(self):
        conn = mysql.connector.connect(host='localhost', database='consultorio', user='###', password='###')
        sql_insert = f"""INSERT INTO clientes (NOME, CPF, TELEFONE, TELEFONE2, DATA_NASCIMENTO, CEP, ENDERECO, BAIRRO, 
         CIDADE, ESTADO, PROFISSAO, NACIONALIDADE, ESTADO_CIVIL, INDICACAO) 
         VALUES ('{self.nome}','{self._cpf}','{self.telefone}','{self.telefone2}','{self.formata_data()}',
         '{self.cep}', '{self.get_endereco()}','{self.get_bairro()}','{self.get_cidade()}','{self.get_estado()}',
          '{self.profissao}', '{self.nacionalidade}', '{self.estado_civil}', '{self.indicacao}') """
        cursor = conn.cursor()
        cursor.execute(sql_insert)
        conn.commit()
        conn.close()

def pede_cpf():
    pergunta_cpf = input("Possui CPF?\n Digite S / N ").upper().strip()
    while pergunta_cpf not in ("S", "N"):
        print("\nOpção inválida!!\n")
        pergunta_cpf = input("Possui CPF?\n Digite S / N ").upper().strip()
    if pergunta_cpf == "S":
        cpf = input("CPF: ")
        cpf_record = ''.join(filter(lambda i: i if i.isdigit() else None, cpf))
        return cpf_record
    else:
        cpf_record = " "
        return cpf_record

def pede_telefone2():
    pergunta_telefone2 = input("Possui outro telefone?\n Digite: S / N ").upper().strip()
    while pergunta_telefone2 not in ("S", "N"):
        print("\nOpção inválida!!\n")
        pergunta_telefone2 = input("Possui outro telefone?\n Digite: S / N ").upper().strip()
    if pergunta_telefone2 == "S":
        telefone2 = input("Telefone: ").strip()
        while len(telefone2) == 8 or len(telefone2) == 9:
            print("\nÈ preciso digitar o DDD!!!\n")
            telefone2 = input("Telefone: ").strip()
        telefone_record2 = ''.join(filter(lambda i: i if i.isdigit() else None, telefone2))
        return telefone_record2
    else:
        telefone_record2 = " "
        return telefone_record2

def pede_indicacao():
    indicacao = input("Foi indicado por alguém?\n Digite S / N  ").upper().strip()
    while indicacao not in ("S", "N"):
        print("\nOpção inválida!!\n")
        indicacao = input("Foi indicado por alguém?\n Digite S / N  ").upper().strip()
    if indicacao == "S":
        confirma_indicacao = input("Quem indicou: ").title().strip()
        return confirma_indicacao
    else:
        confirma_indicacao = " "
        return confirma_indicacao

def cadastra_paciente():
    print("** Para realizar o cadastro do(a) paciente, digite as informações pedidas abaixo **\n")

    nome_paciente = input("Nome: ").title().strip()

    cpf = pede_cpf()

    pergunta_telefone = input("Telefone: ").strip()
    telefone = pede_telefone(pergunta_telefone)

    telefone2 = pede_telefone2()

    data_nascimento = input("Data de nascimento: ").strip()
    data_formatada = f'{data_nascimento[:2]}/{data_nascimento[3:5]}/{data_nascimento[6:]}'

    cep = pede_cep()

    numero = input("Número: ").strip()
    complemento = input("Complemento: ").strip().capitalize()
    numero_complemento = formata_numero_complemento(numero, complemento)

    profissao = input("Profissão: ").capitalize().strip()

    nacionalidade = input('Nacionalidade: ').capitalize().strip()

    estado_civil = input("Estado civil: ").capitalize().strip()

    indicacao = pede_indicacao()

    cliente = Clientes(nome_paciente, cpf, telefone, telefone2, data_nascimento, cep, numero_complemento, profissao,
                       nacionalidade, estado_civil, indicacao)

    print('\n As informações estão corretas?')
    print(f"Nome: {nome_paciente}  CPF: {cliente.valida_cpf()}  Telefone: {cliente.valida_telefone()}\n"
          f"Telefone2: {cliente.valida_telefone2()}  Data de Nascimento: {data_formatada}  CEP: {cliente.valida_cep()}\n"
          f"Logradouro: {cliente.get_endereco()}  Bairro: {cliente.get_bairro()}  Estado: {cliente.get_estado()}\n"
          f"Cidade: {cliente.get_cidade()}  Profissão: {profissao}  Nacionalidade: {nacionalidade}\n"
          f"Estado Civil: {estado_civil}  Indicação: {indicacao}")

    confirma(cliente)

paciente = cadastra_paciente()