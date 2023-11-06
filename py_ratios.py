import Fallen as fa
import datetime as dt
import pandas as pd
import plotly.express as px
import flet as ft

def main(page: ft.Page):
    hoy = dt.date.today()
    fig = px.line()
    page.title = "Calculador de Ratios"
    page.horizontal_alignment = 'CENTER'
    page.vertical_alignment = "TOP"

    alerta = ft.AlertDialog(
        title=ft.Text("¡Error en los datos ingresados!\nTicker no válido")
    )

    def cerrar_alerta():
        alerta.open = False
        page.update()

    def abrir_alerta():
        page.dialog = alerta
        alerta.open = True
        page.update()

    def habilitar_controles():
        progreso.visible = False
        datos.disabled = False
        page.update()

    def calcula_ratio(e):
        progreso.visible = True
        datos.disabled = True
        page.update()

        try:
            historico_activo1 =  fa.rava.get_history(ticker1.value,
                                                    fecha_ini.value,
                                                    fecha_fin.value,)
        except:
            abrir_alerta()
            habilitar_controles()
            return

        try:
            historico_activo2 =  fa.rava.get_history(ticker2.value,
                                                    fecha_ini.value,
                                                    fecha_fin.value,)
        except:
            abrir_alerta()
            habilitar_controles()
            return

        ratio = historico_activo1.merge(historico_activo2, how='inner', on=['date'])
        ratio['ratio'] = ratio['close_x'] / ratio['close_y']
        titulo = f'Ratio {ticker1.value.upper()}/{ticker2.value.upper()}'
        fig = px.line(ratio, x='date', y='ratio', title=titulo)
        fig.add_hline(ratio['ratio'].mean(),)
        fig.show()
        habilitar_controles()

    espacio = ft.Container(width=70)
    ticker1 = ft.TextField(label='Ticker 1',
                           width=130,
                           value='AL30',)
    ticker2 = ft.TextField(label='Ticker 2',
                           width=130,
                           value='AL30D')
    fecha_ini = ft.TextField(label='Fecha Desde (aaaa-mm-dd)',
                             width=200,
                             value='2022-01-01')
    fecha_fin = ft.TextField(label='Fecha Hasta (aaaa-mm-dd)',
                             width=200,
                             value=hoy)
    boton = ft.OutlinedButton('Calcular Ratio',
                              width=200,
                              on_click=calcula_ratio)

    filas_datos = ft.Row(controls=[
        espacio,
        ticker1,
        ticker2,
        fecha_ini,
        fecha_fin,
        boton
    ])

    datos = ft.Container(filas_datos)
    progreso = ft.ProgressBar(width=1000,visible=False)

    col = ft.Column(controls=[
        ft.Text("Calculadora de Ratios\n",
                size=25,
                color=ft.colors.WHITE,
                text_align='CENTER',
                weight=1000,),
        datos,
        progreso,
        ft.Text("Los tickers de los distintos tipos de dolar son:\n \n  *DOLAR OFICIAL\n  *DOLAR MEP\n  *DOLAR CCL",
                size=15,
                color=ft.colors.WHITE,
                ),
    ])

    contenedor = ft.Container(col)

    page.add(
        contenedor,
    )
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
