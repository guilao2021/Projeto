from cadastro_geral import *
from mysql.connector import Error
import mysql.connector

class tratamentos:
    def __init__(self, id, termino_tratamento, pa_max, pa_min, sens_anestesia,
                 sens_antibioticos, dente_tratado, tratamento_realizado):
        self.id = id
        self.termino_tratamento = termino_tratamento
        self.pa_max = pa_max
        self.pa_min = pa_min
        self.sens_anestesia = sens_anestesia
        self.sens_antibioticos = sens_antibioticos
        self.dente_tratado = dente_tratado
        self.tratamento_realizado = tratamento_realizado

    def formata_data(self):
        return f'{self.termino_tratamento[6:10]}-{self.termino_tratamento[3:5]}-{self.termino_tratamento[:2]} ' \
               f'{self.termino_tratamento[10:]}'

    def gravar_mysql(self):
        conn = mysql.connector.connect(host='localhost', database='consultorio', user='###', password='###')
        sql_insert = f"""INSERT INTO tratamentos (id, termino_tratamento, pa_max, pa_min, sensibilidade_anestesia, 
        sensibilidade_antibioticos, dente, tratamento_realizado) 
        VALUES ('{self.id}','{self.formata_data()}','{self.pa_max}', '{self.pa_min}', '{self.sens_anestesia}', 
        '{self.sens_antibioticos}','{self.dente_tratado}', '{self.tratamento_realizado}') """
        cursor = conn.cursor()
        cursor.execute(sql_insert)
        conn.commit()
        conn.close()

def pede_termino_tratamento():
    print("\nData e hora do término do tratamento\n"
          "OBS: O formato deve ser: 01-01-01 00:00:00")
    termino_tratamento = input("Digite: ")
    return termino_tratamento

def pergunta_hipertenso():
    print("Paciente é hipertenso? ")
    pergunta = input("S / N: ").upper()
    while pergunta not in ("S", "N"):
        print("\nOpção inválida!!\n")
        pergunta = input("S / N: ").upper()
    if pergunta == "S":
        return True
    else:
        return False

def pede_pa_max():
    pa_max = float(input("PA MÀX: "))
    if pa_max >= 17:
        raise ValueError("Paciente não deve realizar o procedimento porque a pressão arterial está elevada!!")
    else:
        pa_str = str(pa_max)
        return pa_str

def pede_pa_min():
    pa_min = float(input("PA MIN: "))
    if pa_min >= 11:
        raise ValueError("Paciente não deve realizar o procedimento porque a pressão arterial está elevada!!")
    else:
        pa_str = str(pa_min)
    return pa_str

def sensibilidade_anestesia():
    print("Possui sensibilidade a anestesias?")
    sens_anestesia = input("S / N: ").upper()
    while sens_anestesia not in ("S", "N"):
        print("Opção inválida!!")
        sens_anestesia = input("S / N: ").upper()
    if sens_anestesia == "S" or sens_anestesia == "N":
        return sens_anestesia

def sensibilidade_antibioticos():
    print("Possui sensibilidade a antibióticos?")
    sens_antibioticos = input("S / N: ").upper()
    while sens_antibioticos not in ("S", "N"):
        print("Opção inválida!!")
        sens_antibioticos = input("S / N: ").upper()
    if sens_antibioticos == "S":
        antibioticos = input("Quais antibióticos? ").capitalize()
        return antibioticos
    else:
        return "N"

def cadastra_tratamento():
    print("** Tela dedicada para o cadastro de tratamentos realizados **\n")

    id = int(input("Digite o ID do paciente: "))

    termino_tratamento = pede_termino_tratamento()

    pergunta_pressao = pergunta_hipertenso()
    if pergunta_pressao == True:
        pa_max = pede_pa_max()
        pa_min = pede_pa_min()
    else:
        pa_max = ""
        pa_min = ""

    anestesia = sensibilidade_anestesia()

    antibioticos = sensibilidade_antibioticos()

    dentes = input("Digite os dentes que serão tratados: ").capitalize()

    tratamento = input("Descrição do tratamento: ").capitalize()

    registro = tratamentos(id, termino_tratamento, pa_max, pa_min, anestesia, antibioticos, dentes, tratamento)

    print("As informações estão corretas?")
    print(f"ID: {id}  Término do tratamento: {termino_tratamento}  PA MÁX: {pa_max}  PA MIN: {pa_min}\n"
    f"Sensibilidade a anestesia: {anestesia}  Sensibilidade a antibióticos: {antibioticos}\n"
    f"Dentes tratados: {dentes}  Tratamento: {tratamento}")

    confirma(registro)

cadastra_tratamento()
