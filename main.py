import pandas as pd
import streamlit as st
import time

import plotly.express as px


def main():
    st.title("Análise James Delivery")
    st.header("Faça upload do arquivo .csv")

    arquivo = st.file_uploader("Upload CSV", type=['csv'])
    if arquivo is not None:
        detalhes_arquivo = {
            "filename": arquivo.name,
            "filetype": arquivo.type,
            "filesize": arquivo.size
        }
        # st.write(detalhes_arquivo)
        df = pd.read_csv(arquivo)
        st.dataframe(df)

        st.sidebar.title('Menu')
        analise_desejada = st.sidebar.selectbox(
            'Seleciona a análise desejada',
            ('Top 10 refeições mais vendidas',
             'Top 10 refeições com maior faturamento',
             'Top 10 lojas com mais pedidos',
             'Top 10 lojas com maior faturamento',
             'Outras análises')
        )

        latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'Carregando {i + 1}')
            bar.progress(i + 1)
            time.sleep(0.03)

        if analise_desejada == 'Top 10 refeições mais vendidas':
            st.title('Top 10 refeições mais vendidas')

            top_refeicao = dados_plot(df, 'refeicao_id', 'qtd_pedido')

            indice = lista_indice(top_refeicao, 'refeicao_id')

            fig = grafico_barra(indice, top_refeicao, 'qtd_pedido', 'Refeição ID')

            st.plotly_chart(fig)

        elif analise_desejada == 'Top 10 refeições com maior faturamento':
            st.title('Top 10 refeições com maior faturamento')

            top_receita = dados_plot(df, 'refeicao_id', 'valor_final')

            indice = lista_indice(top_receita, 'refeicao_id')

            fig = grafico_barra(indice, top_receita, 'valor_final', 'Refeição ID')

            st.plotly_chart(fig)

        elif analise_desejada == 'Top 10 lojas com mais pedidos':
            st.title('Top 10 lojas com mais pedidos')

            top_lojas = dados_plot(df, 'loja_id', 'qtd_pedido')

            indice = lista_indice(top_lojas, 'loja_id')

            fig = grafico_barra(indice, top_lojas, 'qtd_pedido', 'Loja ID')

            st.plotly_chart(fig)

        elif analise_desejada == 'Top 10 lojas com maior faturamento':
            st.title('Top 10 lojas com maior faturamento')

            top_lojas = dados_plot(df, 'loja_id', 'valor_final')

            indice = lista_indice(top_lojas, 'loja_id')

            fig = grafico_barra(indice, top_lojas, 'valor_final', 'Loja ID')

            st.plotly_chart(fig)

        elif analise_desejada == 'Outras análises':
            st.title('Mais informações sobre os pedidos')
            opcao = st.selectbox(
                'Escolha uma opção',
                ('Pedidos por Categoria',
                 'Pedidos por Cozinha',
                 'Pedidos por Tipo de Loja')
            )

            if opcao == 'Pedidos por Categoria':

                fig = px.bar(df,
                             x = df.categoria.value_counts().sort_values(ascending=True).index,
                             y = df.categoria.value_counts().sort_values(ascending=True).values,
                             labels= {
                                 'x': 'Categoria',
                                 'y': 'N° de pedidos'
                             })

                st.plotly_chart(fig)

            elif opcao == 'Pedidos por Cozinha':

                fig = px.bar(df,
                             x = df.cozinha.value_counts().sort_values(ascending=True).index,
                             y = df.cozinha.value_counts().sort_values(ascending=True).values,
                             labels= {
                                 'x': 'Cozinha',
                                 'y': 'N° de pedidos'
                             })

                st.plotly_chart(fig)


            elif opcao == 'Pedidos por Tipo de Loja':

                fig = px.bar(df,
                             x = df.loja_tipo.value_counts().sort_values(ascending=True).index,
                             y = df.loja_tipo.value_counts().sort_values(ascending=True).values,
                             labels= {
                                 'x': 'Tipo de loja',
                                 'y': 'N° de pedidos'
                             })

                st.plotly_chart(fig)


def grafico_barra(indice, df, y, label_x):
    fig = px.bar(df,
                 x = indice,
                 y = y,
                 labels = {
                     'x': label_x,
                 }
                 )
    return fig


def lista_indice(df, coluna):
    indice = []
    for i in list(df[coluna].values):
        indice.append(str(i))
    return indice


def dados_plot(df, x, y):
    df_plot = df[[x, y]].groupby(x).sum().sort_values(by=y, ascending=True).tail(10).reset_index()

    return df_plot


if __name__ == '__main__':
    main()
