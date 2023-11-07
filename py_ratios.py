import datetime as dt
import Fallen as fa
import plotly.express as px
import flet as ft
from flet.plotly_chart import PlotlyChart

def main(page: ft.Page):

    hoy = dt.date.today()
    titulo = ''
    page.title = 'Calculadora de Ratios'
    page.horizontal_alignment = ft.alignment.center
    page.vertical_alignment = ft.alignment.top_center
    page.auto_scroll = True
    page.window_maximized = True
    alerta = ft.AlertDialog(title=ft.Text('¡Error en los datos ingresados!\n'\
                                          'Ticker no Encontrado.'))

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
        fig = px.line(ratio, x='date', y='ratio', width=1900, height=750, title=titulo, )
        fig.add_hline(ratio['ratio'].mean(),)
        chart = PlotlyChart(fig, expand=True, )
        if(ver_grafico.value==True):
            fig.show()

        col.controls.pop(5)
        grafico = ft.Container(content=chart, alignment=ft.alignment.center)
        col.controls.append(grafico)
        habilitar_controles()

    def mostrar_grafico(e):
        fig.show()

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
    
    boton_calcular = ft.ElevatedButton('Calcular Ratio', on_click=calcula_ratio, scale=1.5, color=ft.colors.WHITE, )
    contenedor_boton_calcular = ft.Container(content=boton_calcular, alignment=ft.alignment.center, margin=10)
    
    ver_grafico = ft.Switch(label='Ver grafico completo', value=False)

    progreso = ft.ProgressBar(visible=False)

    fig = px.line(width=1900, height=750, )
    chart = PlotlyChart(fig, expand=True, )
    grafico = ft.Container(content=chart, alignment=ft.alignment.center)

    col = ft.Column(controls=[
        ft.Text("Calculadora de Ratios\n",
                size=25,
                color=ft.colors.WHITE,
                text_align='CENTER',),
        filas_datos,
        contenedor_boton_calcular,
        progreso,
        ver_grafico,
        grafico,
    ], horizontal_alignment=ft.alignment.center, )

    contenedor = ft.Container(col)

    page.add(
        contenedor,
    )

ft.app(target=main)
