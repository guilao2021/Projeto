from validate_docbr import CPF
import requests, re

class Cadastro:
    def __init__(self, nome, telefone, cep, numero_complemento, data):
        self.nome = nome
        self.telefone = telefone
        self.cep = cep
        self.numero_complemento = numero_complemento
        self.data = data

    def valida_telefone(self):
        telefone = Telefone(self.telefone)
        return telefone

    def formata_data(self):
        return f'{self.data[6:]}-{self.data[3:5]}-{self.data[:2]}'

    def valida_cep(self):
        cep = Cep(self.cep)
        return cep

    def get_endereco(self):
        return f"{self.valida_cep().logradouro()}, {self.numero_complemento}"

    def get_bairro(self):
        return self.valida_cep().bairro()

    def get_cidade(self):
        return self.valida_cep().cidade()

    def get_estado(self):
        return self.valida_cep().estado()

def pede_cep():
    pede_cep = input("CEP: ")
    while len(pede_cep) != 8:
        print("CEP deve conter 8 digitos!!")
        pede_cep = input("CEP: ")
    cep = ''.join(filter(lambda i: i if i.isdigit() else None, pede_cep))
    return cep

def formata_numero_complemento(numero, complemento):
    if len(complemento) > 0:
        numero_complemento = f"{numero} - {complemento} "
        return numero_complemento
    else:
        numero_complemento = numero
        return numero_complemento

def pede_telefone(telefone):
    while len(telefone) == 8 or len(telefone) == 9:
        print("\nÈ preciso digitar o DDD!!!\n")
        telefone = input("Telefone: ").strip()
    telefone_record = ''.join(filter(lambda i: i if i.isdigit() else None, telefone))
    return telefone_record

def confirma(usuario):
    confirma = input("\n Para salvar registro, digite: S / N ").upper().strip()
    while confirma not in ("S", "N"):
        print("\nOpção inválida!!")
        confirma = input("\n Para salvar registro, digite: S / N ").upper().strip()
    if confirma == "S":
        usuario.gravar_mysql()
        print("\nRegistro inserido com sucesso!")
    else:
        print("\n** Reinicie o cadastro **\n")

class Cep:

    def __init__(self, cep):
        if len(cep) == 8:
            self.cep = cep
        else:
            raise ValueError("CEP deve conter 8 dígitos!")

    def cep_valido(self):
        url = 'https://viacep.com.br/ws/{}/json/'.format(self.cep)
        check_cep = requests.get(url)
        try:
            dados = check_cep.json()
            return   [dados['localidade'],
                      dados['uf'],
                      dados['logradouro'],
                      dados['bairro']]
        except KeyError:
            raise ValueError("CEP inválido!!!!")

    def cidade(self):
        info = self.cep_valido()
        return info[0]

    def estado(self):
        info = self.cep_valido()
        return info[1]

    def logradouro(self):
        info = self.cep_valido()
        return info[2]

    def bairro(self):
        info = self.cep_valido()
        return info[3]

    def mascara_cep(self):
        return f"{self.cep[:5]}-{self.cep[5:]}"

    def __str__(self):
        return self.mascara_cep()

class Documento:

    @staticmethod
    def analisa_doc(doc):
        if len(doc) == 11:
            return Cpf(doc)
        else:
            raise ValueError("Número de digitos incorreto!!")

class Cpf:

    def __init__(self, doc):
        if self.analisa_cpf(doc):
            self.cpf = doc
        else:
            raise ValueError('CPF inserido não é valido!')

    def analisa_cpf(self, doc):
        analisa_cpf = CPF()
        return analisa_cpf.validate(doc)

    def formata_cpf(self):
        cpf_mask = CPF()
        return cpf_mask.mask(self.cpf)

    def __str__(self):
        return self.formata_cpf()

class Telefone:
    def __init__(self, telefone):
        if len(telefone) == 10 or len(telefone) == 11:
            if self.valida_telefone(telefone):
                self.numero = telefone
            else:
                raise ValueError("Número incorreto!")
        else:
            raise ValueError("Quantidade de digitos incorreto!!")

    def valida_telefone(self, telefone):
        padrao = '([0-9]{2})([0-9]{4,5})([0-9]{4})'
        resposta = re.findall(padrao, telefone)
        if resposta:
            return True
        else:
            return False

    def formata_telefone(self):
        padrao = '([0-9]{2})([0-9]{4,5})([0-9]{4})'
        resposta = re.search(padrao, self.numero)
        telefone_formatado = "({}){}-{}".format(resposta.group(1), resposta.group(2), resposta.group(3))

        return telefone_formatado

    def __str__(self):
        return self.formata_telefone()
