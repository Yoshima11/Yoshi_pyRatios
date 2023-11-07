import datetime as dt
import Fallen as fa
import plotly.express as px
import flet as ft
from flet.plotly_chart import PlotlyChart

def main(page: ft.Page):

    hoy = dt.date.today()
    titulo = ''
    page.title = 'Calculador de Ratios'
    page.horizontal_alignment = ft.alignment.center
    page.vertical_alignment = ft.alignment.top_center
    page.auto_scroll = True
    page.window_maximized = True
    alerta = ft.AlertDialog(title=ft.Text('¡Error en los datos ingresados!\n'\
                                          'Ticker no válido'))

    def abrir_alerta():
        page.dialog = alerta
        alerta.open = True
        page.update()

    def habilitar_controles():
        progreso.visible = False
        filas_datos.disabled = False
        boton_calcular.disabled = False
        page.update()

    def calcula_ratio(e):
        progreso.visible = True
        filas_datos.disabled = True
        boton_calcular.disabled = True
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
        fig = px.line(ratio, x='date', y='ratio', width=1800, height=700, )
        fig.add_hline(ratio['ratio'].mean(),)
        chart = PlotlyChart(fig, expand=True,)
        grafico.tabs.append(ft.Tab(text=titulo, content=chart))
        grafico.selected_index = boton_calcular.data
        boton_calcular.data +=1
        habilitar_controles()

    ticker1 = ft.TextField(label='Ticker 1',
                           value='AL30',)
    ticker2 = ft.TextField(label='Ticker 2',
                           value='AL30D')
    fecha_ini = ft.TextField(label='Fecha Desde (aaaa-mm-dd)',
                             value='2022-01-01')
    fecha_fin = ft.TextField(label='Fecha Hasta (aaaa-mm-dd)',
                             value=hoy)

    filas_datos = ft.Row(controls=[ticker1,
                                   ticker2,
                                   fecha_ini,
                                   fecha_fin,
                                   ], alignment=ft.MainAxisAlignment.CENTER, )

    boton_calcular = ft.TextButton(
                            content=ft.Container(
                                            content=ft.Text(
                                                'Calcular Ratio',
                                                size=20,
                                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                text_align=ft.TextAlign.CENTER,
                                                
                                            ),
                                            alignment=ft.alignment.center,
                            ),
                            on_click=calcula_ratio,
                            data=0,
                     )
    progreso = ft.ProgressBar(visible=False)

    fig = px.line()
    chart = PlotlyChart(fig, expand=True, isolated=True)
    grafico = ft.Tabs(expand=1, scrollable=False, indicator_tab_size=True)
    cont_grafico = ft.Container(content=grafico, )

    col = ft.Column(controls=[
        ft.Text("Calculadora de Ratios\n",
                size=25,
                color=ft.colors.WHITE,
                text_align='CENTER',),
        filas_datos,
        boton_calcular,
        progreso,
        cont_grafico,
    ], horizontal_alignment=ft.alignment.center, )

    contenedor = ft.Container(col)

    page.add(
        contenedor,
    )
ft.app(target=main)
