import Fallen as fall
import datetime as dt
import pandas as pd
import plotly.express as px
import flet as ft
from flet import *
from flet.plotly_chart import PlotlyChart

def main(page: ft.Page):
    hoy = dt.date.today()
    fig = px.line()
    page.title = "Calculador de Ratios"
    page.horizontal_alignment = 'center'
    page.vertical_alignment = "top"

    def calcula_ratio(e):
        '''
        if ticker1.value == "dolar" :
            historico_activo1 = fall.ambito.dolar_oficial(str(fecha_ini.value), str(fecha_fin.value))
        elif ticker1.value == "blue" :
            historico_activo1 = fall.ambito.dolar_blue(str(fecha_ini.value), str(fecha_fin.value))
        else:
            historico_activo1 = fall.rava.get_history(ticker1.value, fecha_ini.value, fecha_fin.value)
        if ticker2.value == "dolar" :
            historico_activo2 = fall.ambito.dolar_oficial(str(fecha_ini.value), str(fecha_fin.value))
        elif ticker2.value == "blue" :
            historico_activo2 = fall.ambito.dolar_blue(str(fecha_ini.value), str(fecha_fin.value))
        else:
            historico_activo2 = fall.rava.get_history(ticker2.value, fecha_ini.value, fecha_fin.value)
        '''
        historico_activo1 = fall.rava.get_history(ticker1.value, fecha_ini.value, fecha_fin.value)
        historico_activo2 = fall.rava.get_history(ticker2.value, fecha_ini.value, fecha_fin.value)
        ratio = historico_activo1.merge(historico_activo2, how='inner', on=['date'])
        ratio['ratio'] = ratio['close_x'] / ratio['close_y']
        fig = px.line(ratio, x='date', y='ratio')
        fig.add_hline(ratio['ratio'].mean())
        fig.show()

    ticker1 = ft.TextField(label='Ticker 1', width=130, value='AL30')
    ticker2 = ft.TextField(label='Ticker 2', width=130, value='AL30D')
    fecha_ini = ft.TextField(label='Fecha Desde (aaaa-mm-dd)', width=200, value='2022-01-01')
    fecha_fin = ft.TextField(label='Fecha Hasta (aaaa-mm-dd)', width=200, value=hoy)
    boton = ft.TextButton('Calcular Ratio', width=200, on_click=calcula_ratio)

    filas_datos = ft.Row(controls=[
        ticker1,
        ticker2,
        fecha_ini,
        fecha_fin,
        boton
    ])

    datos = ft.Container(filas_datos)

    col = ft.Column(controls=[
        datos,
    ])

    contenedor = ft.Container(col)

    page.add(
        contenedor,
    )
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
