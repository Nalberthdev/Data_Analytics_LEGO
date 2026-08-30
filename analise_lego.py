import pandas as pd
import matplotlib


conjuntos = pd.read_csv("base_de_dados/lego_sets.csv") #carrega a nossa base de dados



# mostra o tamanho da tabela linhas/colunas
print(conjuntos.shape) 

#mostra o nome das colunas 
print(conjuntos.columns.tolist())


# retorno do print nalberth@nalberth-Vostro-3480:~/Data_Analytics_LEGO$ python analise_lego.py 
# 8457, 14)
# set_id', 'name', 'year', 'theme', 'subtheme', 'themeGroup', 'category', 'pieces', 'minifigs', 'agerange_min', 'US_retailPrice', 'bricksetURL', 'thumbnailURL', 'imageURL']



# criação da tabela de frêquencia ( fi ) 

coluna = "themeGroup" 


# frequencia (fi): quantas vezes cada grupo aparece
frequencia_absoluta = conjuntos[coluna].value_counts(dropna=False)  


# frequencia relativa (fr): fi dividido pelo total (valor entre 0 e 1)
frequencia_relativa = conjuntos[coluna].value_counts(dropna=False, normalize=True)

# frequencia percentual (%): fr multiplicada por 100
frequencia_percentual = (frequencia_relativa * 100).round(2)

# junta as 3 colunas numa unica tabela
tabela_frequencia = pd.DataFrame({
    "fi": frequencia_absoluta,
    "fr": frequencia_relativa.round(4),
    "%": frequencia_percentual,
})

# frequencia absoluta acumulada (soma que vai empilhando de cima para baixo)
tabela_frequencia["fi_acumulada"] = tabela_frequencia["fi"].cumsum()

print(tabela_frequencia)
print("Soma de fi:", tabela_frequencia["fi"].sum())