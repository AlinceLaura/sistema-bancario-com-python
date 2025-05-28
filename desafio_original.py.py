


Menu = """

[1]Depositar
[2]Sacar
[3]Extrato
[0]Sair 

=> """

saldo = 0
limite = 500
cheque_especial = 500
extrato = ""
numero_saques = 0
limite_saques = 3 

while True:
    
    opcao = input(Menu)

    if opcao == "1":
        tipo_deposito = input("Escolha o tipo de depósito:\n[1] Dinheiro\n[2] Cheque\n=> ")

        if tipo_deposito not in ["1", "2"]:
            print("Tipo de depósito inválido.")
            continue

        valor = float(input("Informe o valor do depósito: "))

        if valor <= 0:
            print("Operação falhou! O valor informdo é inválido.")

        else:
            saldo += valor
            if tipo_deposito == "1":
                extrato += f"Depósito em dinheiro: R$ {valor:.2f}\n"
            else:
                extrato += f"Depósito em cheque: R$ {valor:.2f}\n"

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        excedeu_limite = valor > limite 

        excedeu_saques = numero_saques >= limite_saques 

        saldo_disponivel = saldo+cheque_especial

        if valor>saldo_disponivel:
            print("Operação falhou! Você não possui saldo suficiente e nem limite de cheque especial.")

        elif excedeu_limite:
            print("Operação falhou! O valor de saque excedeu o limite")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor 
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else: 
            print("Operação falhou! O valor informado é inválido")

    
    elif opcao == "3":
        print("\n========== EXTRATO ==========")
        print("Não foram realizados movimentações."if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        if saldo < 0:
            print(f"Cheque especial utilizado: R$ {-saldo:.2f} de R$ {cheque_especial:.2f}")
        print("==============================")
    
    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
