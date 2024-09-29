import pandas as pd
import matplotlib.pyplot as plt
import httpx

def filtro():

    df = pd.read_csv('data.csv', on_bad_lines='skip', delimiter=';', low_memory=False)

    return df

def filtro_Municipio(df,mun):
    filtro = df[df['municipio'] == mun]
    return filtro

def filtro_Product(df, product):
    filtro = df[df['especie'].isin(product)]
    return filtro

def graficar(df, mun):

    df_municipality = filtro_Municipio(df,mun)

    print(df_municipality)

    df_2023  = df_municipality[df_municipality['anho'] == "2023"]

    print(df_2023)

    product_count = df_2023['especie'].value_counts()

    print(product_count)

    top_5_product = product_count.head(5).index

    print(top_5_product)


    df_top_5_product = filtro_Product(df_municipality,top_5_product)

    print(df_top_5_product)

    top_5_counts = df_top_5_product['especie'].value_counts()

    print(top_5_counts)

    plt.figure(figsize=(10, 6))
    plt.pie(top_5_counts, labels=top_5_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    image_path = 'static/img/grafica.png'
    plt.savefig(image_path)
    plt.close()

    product_info = {}
    for product in top_5_product:
        product_data = df_top_5_product[df_top_5_product['especie'] == product].iloc[0]
        product_info[product] = {
            'EstadoFisicoProduccio': product_data['EstadoFisicoProduccio'],
            'rendimiento': product_data['rendimiento'],
            'nombre_cientifico': product_data['nombre_cientifico']
        }

    return product_info

