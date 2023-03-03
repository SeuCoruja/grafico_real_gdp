import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np

sns.set()

def main():
    real_gdp = pd.read_csv('GDPC1.csv', index_col='DATE')
    real_gdp.index = pd.DatetimeIndex(real_gdp.index)
    
    fig, ax = plt.subplots()
    real_gdp.index.name = 'Data'
    real_gdp.iloc[:, 0]['2002/01/01':].plot(logy=True, ax = ax)
    ax.yaxis.set_major_formatter('${x:1,.0f}')
    ax.yaxis.set_major_locator(mtick.LogLocator(base=10, subs=[15,20,25]))
    plota_linha_de_trend('2002/01/01', '2007/01/01', ax, real_gdp, '2004/01/01', '2023/03/03', ls = '--', color = 'red')
    ax.set_title('PIB per Capita Real dos EUA')
    plt.minorticks_off()
    plt.savefig('oh_nao.png')
    plt.close(fig)

    fig, ax = plt.subplots()
    real_gdp.index.name = 'Data'
    real_gdp.iloc[:, 0].plot(logy=True, ax = ax)
    ax.yaxis.set_major_formatter('${x:1,.0f}')
    ax.yaxis.set_major_locator(mtick.LogLocator(base=10, subs=[2,5,10,20]))
    plota_linha_de_trend('1950/01/01', '1953/01/01', ax, real_gdp, '1950/01/01', '1955/03/03', ls = '--', color = 'green')
    plota_linha_de_trend('1961/06/01', '1966/01/01', ax, real_gdp, '1963/06/01', '1970/01/01', ls = '--', color = 'green')
    plota_linha_de_trend('1971/03/01', '1973/03/01', ax, real_gdp, '1971/03/01', '1975/01/01', ls = '--', color = 'green')
    plota_linha_de_trend('1975/01/01', '1979/01/01', ax, real_gdp, '1975/01/01', '1984/01/01', ls = '--', color = 'green')
    plota_linha_de_trend('1984/01/01', '1990/01/01', ax, real_gdp, '1987/01/01', '1995/01/01', ls = '--', color = 'green')
    plota_linha_de_trend('1996/01/01', '1999/01/01', ax, real_gdp, '1997/01/01', '2004/03/01', ls = '--', color = 'green')
    plota_linha_de_trend('2002/01/01', '2007/01/01', ax, real_gdp, '2004/01/01', '2023/03/03', ls = '--', color = 'red')
    ax.set_title('PIB per Capita Real dos EUA')
    plt.savefig('mas_na_real.png')
    plt.close(fig)

    print()

def plota_linha_de_trend(
        dt_inicio_interpolacao, dt_fim_interpolacao, ax, y,
        dt_inicio_plot, dt_fim_plot, **kwargs
    ):
    y_intervalo = np.log(y[dt_inicio_interpolacao:dt_fim_interpolacao].copy())
    x_intervalo = pd.DataFrame(index = y_intervalo.index)
    x_intervalo['inclinacao'] = np.arange(len(x_intervalo))
    x_intervalo['const'] = 1
    a = np.matrix(x_intervalo)
    b = np.matrix(y_intervalo)
    fit = (a.T * a).I * a.T * b
    inclinacao, intercept = fit
    qtd_de_pontos_entre_as_dts_de_inicio = len(y[dt_inicio_interpolacao:dt_inicio_plot])
    index_para_plotar = pd.DatetimeIndex(pd.date_range(dt_inicio_plot, dt_fim_plot, freq='Q'))
    linha_fitada = np.exp(intercept + inclinacao * (qtd_de_pontos_entre_as_dts_de_inicio + np.arange(len(index_para_plotar))))
    serie_linha_fitada = pd.Series(data =  np.array(linha_fitada).flatten(), index = index_para_plotar)
    serie_linha_fitada.plot(ax = ax, **kwargs)

if __name__ == '__main__':
    main()