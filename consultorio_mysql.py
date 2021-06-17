import mysql.connector
from mysql.connector import Error

class BancoMySql:
    def __init__(self, tabela, parametro, identificador):
        self.tabela = tabela
        self.parametro = parametro
        self.identificador = identificador

    def conectar_mysql(self):
        try:
            global conn
            conn = mysql.connector.connect(host='localhost', database='consultorio', user='###', password='###')
        except Error as erro:
            print("Erro de Conexão")

    def func_consulta_especifica(self):
        try:
            self.conectar_mysql()
            consulta_sql = f"SELECT * FROM {self.tabela} WHERE {self.parametro} like '%{self.identificador}%'"
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            linhas = cursor.fetchall()
            for linha in linhas:
                print(linha)
        except Error as erro:
            print("Falha ao consultar tabela: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

    def func_consulta_geral(self):
        try:
            self.conectar_mysql()
            consulta_sql = f"SELECT * FROM {self.tabela}"
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            linhas = cursor.fetchall()
            for linha in linhas:
                print(linha)
            conn.close()
        except Error as erro:
            print("Falha ao consultar tabela: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

    def func_atualizar(self, update):
        try:
            self.conectar_mysql()
            alterar = update
            cursor = conn.cursor()
            cursor.execute(alterar)
            conn.commit()
            print("Parâmetro alterado com sucesso!")
            cursor.close()
        except Error as erro:
            print("Falha ao inserir dados no MySQL: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

    def func_deletar(self, deletar):
        try:
            self.conectar_mysql()
            excluir = deletar
            cursor = conn.cursor()
            cursor.execute(excluir)
            conn.commit()
            print("Registro excluido!!")
        except Error as erro:
            print("Falha ao consultar tabela: {}".format(erro))
        finally:
            if (conn.is_connected()):
                conn.close()

#Menu
def options():
    print("** Tela dedicada para a realização de SELECTS, UPDATES E DELETES no banco de dados"
          " CONSULTORIO **\n")
    print("Selecione uma das opções abaixo:")
    print("1 - Consulta | 2 - Atualizar dados | 3 - Deletar dados: ")
    opcao = int(input(""))
    opcoes_validas = [1, 2, 3]
    while opcao not in opcoes_validas:
        print("Opção inválida!!")
        opcao = input("Digite novamente: ").lower().strip()
    if opcao == 1:
        return consulta()
    if opcao == 2:
        return atualiza()
    if opcao == 3:
        return deleta()

def seleciona_tabela():
    print("Digite o nome de uma das tabelas abaixo: ")
    print("Clientes | Dentistas | Tabela de preços | Tratamentos | Notas Fiscais")
    tab_escolhida = input("").lower()
    tabelas_validas = ["clientes", "dentistas", "tabela_de_precos", "tabela de preços", "tratamentos", "notas fiscais"]
    while tab_escolhida not in tabelas_validas:
        print("Tabela não existe!!!")
        tab_escolhida = input("Digite o nome da tabela que deseja selecionar: ").lower()
    if tab_escolhida == 'tabela de preços':
        return 'tabela_de_precos'
    if tab_escolhida == 'notas fiscais':
        return 'nf'
    return tab_escolhida

#Select
def consulta():
    tabela = seleciona_tabela()
    print("\n** Tela dedicada para consultar dados da tabela selecionada **\n")
    tipo_consulta = int(input("1 - Consulta Geral | 2 - Consulta Especifica: "))
    if tipo_consulta == 1:
        consulta = BancoMySql(tabela,"", "").func_consulta_geral()
        return consulta
    elif tipo_consulta ==2:
        parametro = input("Digite o nome da coluna que servirá como parametro: ").strip().upper()
        identificador = input("Digite uma palavra chave: ").strip()
        consulta = BancoMySql(tabela, parametro, identificador).func_consulta_especifica()
        return consulta
    else:
        print("Opção inválida!!!")

#Update
def atualiza():
    tabela = seleciona_tabela()
    print("\n** Tela dedicada para atualizar dados na tabela selecionada **\n")
    parametro = input("Digite o nome da coluna que servirá como parametro: ").strip().upper()
    identificador = input("Digite uma palavra chave: ").title()
    BancoMySql(tabela, parametro, identificador).func_consulta_especifica()
    print("\nEntre com a alteração")
    coluna_a_alterar = input("Digite o nome da coluna que deseja alterar: ").upper()
    dado_a_alterar = input("Digite o novo dado da tabela para alterar : ").title().strip()
    update = f"""UPDATE {tabela} SET {coluna_a_alterar} = '{dado_a_alterar}' 
    WHERE {parametro} = '{identificador}' """
    BancoMySql(tabela, parametro, identificador).func_atualizar(update)
    verifica = input("\nDeseja consultar a atualização? S / N: ").upper()
    while verifica not in ("S","N"):
        print("Opção inválida!!!")
        verifica = input('S / N: ').upper()
    if (verifica == 'S'):
        BancoMySql(tabela, parametro, identificador).func_consulta_especifica()
    else:
        print("\nAté mais!")

#Delete
def deleta():
    tabela = seleciona_tabela()
    print('\n** Tela dedicada para deletar dados da tabela selecionada **\n')
    parametro = input("Digite o nome da coluna que servirá como parametro: ").strip().upper()
    identificador = input("Digite uma palavra chave: ").title()
    BancoMySql(tabela, parametro, identificador).func_consulta_especifica()
    print("Deseja excluir esse registro?")
    confirma = input('S / N: ').upper()
    while confirma not in('S', 'N'):
        print("Opção inválida!!")
        confirma =  input('S / N: ').upper()
    if confirma == 'S':
        deletar = f"DELETE FROM {tabela} WHERE {parametro} = {identificador}"
        BancoMySql(tabela, parametro, identificador).func_deletar(deletar)
    else:
        print("\nAté mais!")

options()
