import os
from datetime import datetime


def converter_data(data_str):
    try:
        return datetime.strptime(data_str, '%d/%m/%Y') if data_str else None
    except ValueError:
        return None


def carregar_dados(path_arq, dict_db):
    if os.path.exists(path_arq):
        with open(path_arq, 'r', encoding='utf-8') as arq:
            for i, linha in enumerate(arq):
                dados = linha.strip().split(";")

                if len(dados) != 8:
                    continue

                dict_db[i] = {
                    "dt_notific": converter_data(dados[0]),
                    "dt_inicio_sintomas": converter_data(dados[1]),
                    "bairro_resid__estadia": dados[2],
                    "ap_residencia_estadia": dados[3],
                    "evolução": dados[4],
                    "dt_óbito": converter_data(dados[5]),
                    "cep": dados[6],
                    "data_atualização": converter_data(dados[7]),
                }


def obitos_por_bairro(dict_db):
    casos_por_bairro = dict()

    for bairro, dados in dict_db.items():
        if dados["bairro_resid__estadia"] not in casos_por_bairro:
            casos_por_bairro[dados["bairro_resid__estadia"]] = [0, 0]

        if dados["evolução"] == "óbito":
            casos_por_bairro[dados["bairro_resid__estadia"]][0] += 1

        casos_por_bairro[dados["bairro_resid__estadia"]][1] += 1

    return casos_por_bairro


def obitos_por_cep(dict_db):
    casos_por_cep = dict()

    for bairro, dados in dict_db.items():
        if dados["cep"] not in casos_por_cep:
            casos_por_cep[dados["cep"]] = [0, 0]

        if dados["evolução"] == "óbito":
            casos_por_cep[dados["cep"]][0] += 1

        casos_por_cep[dados["cep"]][1] += 1

    return casos_por_cep


def calcular_percentual_obito(obitos, total_de_casos):
    return (obitos / total_de_casos) * 100


def listar_percentual_obito_por_bairro(dict_db):
    casos_por_bairro = obitos_por_bairro(dict_db)

    if len(casos_por_bairro) != 0:

        for bairro, dados in casos_por_bairro.items():
            percentual_obito = calcular_percentual_obito(obitos=dados[0], total_de_casos=dados[1])

            print(f"Bairro: {bairro}\n"
                  f"Percentual de óbito: {percentual_obito:.2f}\n"
                  f"Total de casos: {dados[1]}\n")
        return True
    return False


def listar_percentual_obito_por_cep(dict_db):
    casos_por_cep = obitos_por_cep(dict_db)

    if len(casos_por_cep) != 0:

        for cep, dados in casos_por_cep.items():
            percentual_obito = calcular_percentual_obito(obitos=dados[0], total_de_casos=dados[1])

            print(f"CEP: {cep}\n"
                  f"Percentual de óbito: {percentual_obito:.2f}\n"
                  f"Total de casos: {dados[1]}\n")
        return True
    return False


def buscar_data_primeiro_caso(dict_db):
    data_primeiro_caso = datetime.max

    for _, dados in dict_db.items():
        if dados["dt_notific"] and dados["dt_notific"] < data_primeiro_caso:
            data_primeiro_caso = dados["dt_notific"]

    return data_primeiro_caso.strftime('%d/%m/%Y') if data_primeiro_caso != datetime.max else None


def buscar_bairro_primeiro_caso(dict_db):
    data = datetime.strptime(buscar_data_primeiro_caso(dict_db), "%d/%m/%Y")

    if data is not None:
        for _, dados in dict_db.items():
            if dados["dt_notific"] == data:
                return dados["bairro_resid__estadia"]
    return None


def calcular_total_de_obitos(dict_db):
    casos_por_bairro = obitos_por_bairro(dict_db)

    total_de_obitos = 0
    for bairro, dados in casos_por_bairro.items():
        total_de_obitos += dados[1]

    return total_de_obitos
