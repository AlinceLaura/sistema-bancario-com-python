
from datetime import datetime 

Menu = """
########## MENU ##########
[1]Nova Conta
[2]Listar Contas
[3]Depositar
[4]Sacar
[5]Extrato
[0]Sair 
=> """

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope

class Historico:
     
     def __init__(self):
          self._transacoes = []
          
     def adicionar_transacao(self, transacao):
         self._transacoes.append(transacao)
          
     def gerar_relatorio(self, tipo_transacao=None):
          for transacao in self._transacoes:
               if tipo_transacao is None or transacao ["tipo"].lower()==tipo_transacao.lower():
                    yield transacao

class Conta:
     
     def __init__(self, titular, cpf, data_nascimento, endereco, saldo_inicial=0):
          
          self.titular = titular
          self.cpf = cpf
          self.data_nascimento = data_nascimento
          self.endereco = endereco
          self.saldo = saldo_inicial
          self.historico = Historico()

def selecionar_conta():
     cpf = input ("Informe o CPF do titular da conta: ")
     if cpf in contas:
          return contas [cpf], cpf
     else:
          print("Conta não encontrada.")
          return None, None 

def formatar_cpf(cpf):
          return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

class ContasIterador:
     def __init__(self, contas):
          self.contas = contas 
          self._index = 0
    
     def __iter__(self):
          return self
    
     def __next__(self):
          if self._index >= len(self.contas):
               raise StopIteration
          conta = self.contas[self._index]
          self._index += 1 
          return f"""\n
               CPF:\t{formatar_cpf(conta.cpf)}
               Nome:\t{conta.titular}
               DN:\t{conta.data_nascimento}
               Endereço:\t{conta.endereco}
               Saldo:\t\tR$ {conta.saldo:.2f}
             """
     


contas = {}
limite = 500
cheque_especial = 500
numero_saques = 0
limite_saques = 3 


@log_transacao
def nova_conta ():
        tentativas_cpf = 0

        while tentativas_cpf < 3:
            cpf = input("Informe o CPF do titular da nova conta: ")
            
            if len(cpf) == 11 and cpf.isdigit():
                break
            else:
                tentativas_cpf += 1
                print("Operação falhou! Número de caracteres insuficiente.")
        
        else:
            print("Número máximo de tentativas excedido. Retornando ao Menu.")
            return None
        
        tentativas_nome = 0
        while tentativas_nome < 3:
            nome = input("Informe o nome completo: ")
            
            if len(nome.strip()) > 5:
                break
            else: 
                tentativas_nome +=1
                print("Nome inválido. Informe o nome completo com pelo menos 6 caracteres.")

        else:
            print("Número máximo de tentativas excedido. Retornando ao Menu.")
            return None
                
        tentativas_data_de_nascimento = 0
        while tentativas_data_de_nascimento < 3:
            data_nascimento = input("Informe a data de nascimento (dia/mês/ano): ")
            
            try:
                data_valida = datetime.strptime(data_nascimento, "%d/%m/%Y")
                break
            except ValueError:
                tentativas_data_de_nascimento +=1
                print("Data de nascimento inválida. Informe a data de nascimento no formato (dia/mês/ano).")

        else:
            print("Número máximo de tentativas excedido. Retornando ao Menu.")
            return None
        
        tentativas_endereco = 0
        while tentativas_endereco < 3:
            endereco = input("Informe o endereço (logradouro, n°, bairro, cidade/UF), não insira caracteres especiais: ")
            
            if len(endereco.strip()) > 10:
                break
            else:
                tentativas_endereco +=1
                print("Endereço inválido. Informe o endereço no formato: logradouro, n°, bairro, cidade/UF), não insira caracteres especiais.")
        
        else:
            print("Número máximo de tentativas excedido. Retornando ao Menu.")
            return None

        print("=== Nova Conta criada com sucesso! ===")
        cpf_formatado=f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

        nova = Conta(titular=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
        nova.historico.adicionar_transacao({
             "tipo":f"Abertura de Conta para: {nome} | CPF: {cpf_formatado}",
             "valor": 0.00
             })
        
        contas[cpf] = nova

        return cpf


@log_transacao
def listar_contas():
     if not contas:
          print("Nenhuma conta cadastrada.")
          return
     
     print("\n=========== LISTA DE CONTAS ===========")
     iterador = ContasIterador(list(contas.values()))
     for conta_str in iterador:
          print(conta_str)

     print("=========================================")


@log_transacao
def depositar (conta):

        tipo_deposito = input("Escolha o tipo de depósito:\n[1] Dinheiro\n[2] Cheque\n=> ")

        if tipo_deposito not in ["1", "2"]:
            print("Tipo de depósito inválido.")
            return 
        
        try:
             valor = float(input("Informe o valor do depósito: "))
        except ValueError:
             print("Operação falhou! O valor informado é inválido.")
             return

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")

        else:
            conta.saldo += valor
            tipo = "Depósito em dinheiro" if tipo_deposito == "1" else "Depósito em cheque"
            conta.historico.adicionar_transacao({"tipo": tipo, "valor":valor})
            print(f"{tipo} de R$ {valor:.2f} realizado com sucesso!")
        

@log_transacao
def sacar (conta, limite, numero_saques, limite_saques, cheque_especial):
            
            try:
                 valor = float(input("Informe o valor do saque: "))
            except ValueError: 
                 print("Operação falhou! O valor informado é inválido.")
                 return numero_saques 
            
            if valor <= 0:
                 print("Operação falhou! O valor informado é inválido.")
                 return numero_saques
                 
            excedeu_limite = valor > limite 
            excedeu_saques = numero_saques >= limite_saques 
            saldo_disponivel = conta.saldo + cheque_especial
            
            if valor>saldo_disponivel:
                print("Operação falhou! Você não possui saldo suficiente e nem limite de cheque especial.")
                
            elif excedeu_limite:
                print("Operação falhou! O valor de saque excedeu o limite.")
           
            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")

            else:
                conta.saldo -= valor 
                conta.historico.adicionar_transacao({"tipo": "Saque", "valor": valor})
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            
            return numero_saques

            
@log_transacao
def extrato(conta):

     print("\n========== EXTRATO ==========")
     extrato = ""
     tem_transacao = False 

     transacoes = list(conta.historico.gerar_relatorio())
     if transacoes:
        for transacao in transacoes:
             extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao ['valor']:.2f}"

     else:
        extrato = "Não foram realizadas movimentações"
            
     print(extrato)
     print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")

     if conta.saldo < 0:
        print(f"Cheque especial utilizado: R$ {-conta.saldo:.2f} de R$ {cheque_especial:.2f}")

     print("==============================")


while True:
    
    opcao = input(Menu)

    if opcao == "1":
         cpf = nova_conta()
         if cpf:
              print(f"Conta criada com sucesso para o CPF: {cpf}")
         else: 
              print(f"Falha na criação da conta. Retornando ao Menu.")
    
    elif opcao == "2":
         listar_contas()

    elif opcao == "3":
         conta, _= selecionar_conta()
         if conta:
              depositar(conta)
    
    elif opcao == "4":
         conta, _= selecionar_conta()
         if conta:
              numero_saques = sacar(conta, limite, numero_saques, limite_saques, cheque_especial)

    elif opcao == "5":
         conta, _= selecionar_conta()
         if conta:
              extrato(conta)
       
    elif opcao == "0":
        print("Saindo do sistema. Até Logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")



