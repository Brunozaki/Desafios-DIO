import textwrap
import os
from time import sleep
from datetime import datetime


def clean():
    os.system('cls')

def menu(nivel = 0):
    if nivel == 0:
        menu = """
        Menu do Usuário:
        [1] Acessar usuário existente
        [2] Criar novo usuário
        [q] Sair
        """
        return input(textwrap.dedent(menu))
    elif nivel == 11:
        menu = """
        [1] Acessar conta
        [2] Listar contas do usuário
        [3] Criar conta nova        
        [q] Sair
        """
    elif nivel == 111:
        menu = """
        O que você deseja fazer?
        [1] Saque
        [2] Depósito
        [3] Extrato
        [q] Sair
        """

    return input(textwrap.dedent(menu))

def criar_usuario(cpf, nome, data_nascimento, endereco,/):
    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "contas": []
    }
    return usuario

def acessar_usuario(usuarios, cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta(cpf):
    num_contas = len(contas)
    conta = {
        "agencia": '0001',
        "numero_conta": num_contas + 1,
        "cpf": cpf,
        "saldo": 0,
        "limite": 500,
        "numero_saques": 0,
        "limite_saques": 3,
        "extrato": [{"Data":datetime.now(), "Movimento": "Inicialização da conta", "Saldo": 0}]
    }

    contas.append(conta)
    return {"agencia": conta["agencia"], "numero_conta": conta["numero_conta"]}

def acessar_conta(contas, *, agencia, numero_conta):
    for conta in contas:
        if conta["agencia"] == agencia and conta["numero_conta"] == numero_conta:
            return conta
    return None

def saque (conta, valor):
    conta["saldo"] -= valor
    conta["numero_saques"] += 1
    conta["limite"] -= valor
    conta["extrato"].append({"Data":datetime.now(), "Movimento": f"Saque de R$ -{valor:.2f}", "Saldo": conta["saldo"]})

def deposito (conta, valor):
    conta["saldo"] += valor
    conta["extrato"].append({"Data":datetime.now(), "Movimento": f"Depósito de R$ {valor:.2f}", "Saldo": conta["saldo"]})

usuarios = []
contas = []

while True:

    clean()
    opcao = menu()

    if opcao == "1":
        clean()
        cpf = input("Informe o CPF (somente números): ")
        usuario = acessar_usuario(usuarios, cpf)
        if usuario:
            opcao = menu(11)
        else:
            print('CPF não encontrado')
            continue

        if opcao == "1":
            clean()
            agencia = str(input("Informe o número da agência: "))
            numero_conta = int(input("Informe o número da conta: "))
            conta = acessar_conta(contas, agencia=agencia, numero_conta=numero_conta)

            if conta:
                while True: 
                    clean()
                    print("Acesso à conta realizado com sucesso!")
                    print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")
                    print(f"Saldo: R$ {conta['saldo']:.2f}")
                    print(f"Limite: R$ {conta['limite']:.2f}")
                    print(f"Número de saques realizados: {conta['numero_saques']}")
                    print(f"Limite de saques: {conta['limite_saques']}")
                    opcao_conta = menu(111)                

                    if opcao_conta == "1":
                        clean()
                        valor = float(input("Informe o valor do saque: "))
                        if valor > 0 and valor <= conta["saldo"] and conta["numero_saques"] < conta["limite_saques"]:
                            saque(conta, valor)
                            print("Saque realizado com sucesso!")
                            sleep(1)
                        else:
                            print("Operação falhou! Verifique o valor ou o limite de saques e tente novamente.")
                            sleep(3)
                            continue
                    elif opcao_conta == "2":
                        clean()
                        valor = float(input("Informe o valor do depósito: "))
                        if valor > 0:
                            deposito(conta, valor)
                            print("Depósito realizado com sucesso!")
                            sleep(1)
                        else:
                            print("Operação falhou! O valor informado é inválido.")
                            sleep(3)
                            continue
                    elif opcao_conta == "3":
                        clean()
                        print("Extrato da conta:")
                        for movimento in conta["extrato"]:
                            data_str = movimento["Data"].strftime("%d-%m-%Y %H:%M:%S")
                            print(f"{data_str} - {movimento['Movimento']} - Saldo: R$ {movimento['Saldo']:.2f}")
                        input("Aperte qualquer tecla para sair...")
                    elif opcao_conta == "q":
                        print("Saindo da conta...")
                        sleep(1)
                        break
                    else:
                        print("Operação inválida, por favor selecione novamente a operação desejada.")
                        sleep(1)
                        continue
            else:
                print("Conta não encontrada.")
                sleep(1)
                continue

        elif opcao == "2":
            clean()
            print("Contas do usuário:")
            if len(usuario["contas"]) == 0:
                print("Nenhuma conta encontrada para este usuário.")
                sleep(2)
                continue

            for conta in contas:
                if conta["cpf"] == cpf:
                    print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")
            input("Aperte qualquer tecla para sair...")

        elif opcao == "3":
            clean()
            conta = criar_conta(cpf)
            usuario["contas"].append(conta)
            print("Conta criada com sucesso!")
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")
            sleep(2)
        
        elif opcao == "q":
            break

    elif opcao == "2":
        clean()
        cpf = input("Informe o CPF (somente números): ")
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")
        usuarios.append(criar_usuario(cpf, nome, data_nascimento, endereco))
        print("Usuário criado com sucesso!")
        sleep(2)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        sleep(1)
        continue
    