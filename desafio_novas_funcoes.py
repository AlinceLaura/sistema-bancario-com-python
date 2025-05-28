import textwrap

def menu():
    menu = """\n
    ========== MENU ==========
    [1]Depositar
    [2]Sacar
    [3]Extrato
    [4]Criar Usuário
    [5]Criar Conta
    [6]Listar Contas
    [0]Sair
    """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato +=f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, cheque_especial):
    
    excedeu_limite = valor > limite 
    excedeu_saques = numero_saques >= limite_saques 
    saldo_disponivel = saldo+cheque_especial
    
    if valor>saldo_disponivel:
        print("\n@@@ Operação falhou! Você não possui saldo suficiente e nem limite de cheque especial. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor de saque excedeu o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
         saldo -= valor 
         extrato += f"Saque:\t\tR$ {valor:.2f}\n"
         numero_saques += 1
         print("\n=== Saque realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques
    
def exibir_extrato(saldo,/,*,extrato, cheque_especial):
    print("\n========== EXTRATO ==========")
    print("Não foram realizados movimentações."if not extrato else extrato)
    print(f"\nSaldo:\t\t R$ {saldo:.2f}")
    
    if saldo < 0:
        print(f"Cheque especial utilizado: R$ {-saldo:.2f} de R$ {cheque_especial:.2f}")
        print("==============================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário cadastrado com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Iforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome":nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco":endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario (cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario ["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n === Conta criada com sucesso!===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario":usuario}
        
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

def listar_contas (contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
        print("=" *100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "1234"
    
    saldo = 0
    limite = 500
    cheque_especial = 500
    extrato = ""
    numero_saques = 0 
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            tipo_deposito = input("Escolha o tipo de depósito:\n[1] Dinheiro\n[2] Cheque\n=> ")
            
            if tipo_deposito not in ["1", "2"]:
                print("Tipo de depósito inválido.")
                continue
            
            valor = float(input("Informe o valor do depósito: "))
            
            if valor <= 0:
                print("Operação falhou! O valor informado é inválido.")
                continue

            saldo, extrato = depositar(saldo, valor, extrato)
                
            if tipo_deposito == "1":
                extrato += f"Dinheiro\n"
            else:
                extrato += f"Cheque\n"
                
        elif opcao == "2":
             valor = float(input("Informe o valor do saque: "))

             saldo, extrato, numero_saques = sacar(
                 saldo=saldo,
                 valor=valor,
                 extrato=extrato,
                 limite=limite,
                 numero_saques=numero_saques,
                 limite_saques=LIMITE_SAQUES,
                 cheque_especial=cheque_especial
             )
        
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato, cheque_especial=cheque_especial)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao =="5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)
            
        elif opcao == "0":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
            main()

