import os
from functions import *


def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- Menu ---")
        print("1 – Mostrar o total e a porcentagem de óbitos por bairro")
        print("2 – Mostrar a data em que foi notificado o primeiro caso de Covid-19")
        print("3 – Mostrar o bairro onde ocorreu a primeira notificação de Covid-19")
        print("4 – Mostrar o total de óbitos no município do Rio de Janeiro")
        print("5 – Mostrar o total e a porcentagem de óbitos por CEP ")
        print("6 – Sair ")

        try:
            opt = int(input("Selecione uma opção: "))
            if 1 <= opt <= 6:
                return opt
            else:
                print("Opção inválida. Por favor, selecione uma opção de 1 a 6.")
                input("\nPressione [enter] para continuar...")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
            input("\nPressione [enter] para continuar...")


def main():
    db_dados_covid = dict()
    carregar_dados(path_arq="Dados_CEP_MRJ_covid_19.csv", dict_db=db_dados_covid)

    opt = 1
    while opt != 6:
        opt = menu()

        if opt == 1:
            print("Listando percentual de óbitos por bairro...")
            if not listar_percentual_obito_por_bairro(dict_db=db_dados_covid):
                print("Nenhum caso registrado por bairro.")

        elif opt == 2:
            print("Buscando a data do primeiro caso...")
            data = buscar_data_primeiro_caso(dict_db=db_dados_covid)

            if data is not None:
                print("A data do primeiro caso é:", data)
            else:
                print("Nenhuma data registrada.")

        elif opt == 3:
            print("Buscando o bairro do primeiro caso...")
            bairro = buscar_bairro_primeiro_caso(dict_db=db_dados_covid)

            if bairro is not None:
                print("O bairro do primeiro caso é:", bairro)
            else:
                print("Nenhum bairro registrado ao primeiro caso.")

        elif opt == 4:
            print("Calculando o total de óbitos no municipio do Rio de Janeiro...")
            total_obitos = calcular_total_de_obitos(dict_db=db_dados_covid)
            print("O total de óbitos no município do Rio de Janeiro é:", total_obitos)

        elif opt == 5:
            print("Listando o percentual de óbitos por cep...")
            if not listar_percentual_obito_por_cep(dict_db=db_dados_covid):
                print("Nenhum caso registrado por CEP.")

        else:
            print("Encerrando programa...")


if __name__ == "__main__":
    main()
