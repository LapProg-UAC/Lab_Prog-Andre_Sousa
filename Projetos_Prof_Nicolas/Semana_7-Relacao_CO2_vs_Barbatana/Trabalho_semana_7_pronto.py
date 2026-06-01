import os
import typing
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.io import export_png
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

def generate_plotly_visualization(input_csv: str, temp_output: str) -> None:
    """Gera o primeiro gráfico usando Plotly Express e exporta via Kaleido.

    Parameters
    ----------
    input_csv : str
        Caminho do ficheiro CSV contendo os dados dos pinguins.
    temp_output : str
        Caminho onde a imagem PNG temporária será guardada.
    """
    df_penguins: pd.DataFrame = pd.read_csv(input_csv)
    
    fig: px.scatter = px.scatter(
        df_penguins,
        x='massa',
        y='barbatana',
        color='especie',
        title='Pinguins: Massa vs Barbatana'
    )
    
    fig.write_image(temp_output, engine='kaleido')

def generate_bokeh_visualization(input_csv: str, temp_output: str) -> None:
    """Gera o segundo gráfico usando Bokeh e exporta usando Selenium Headless.

    Parameters
    ----------
    input_csv : str
        Caminho do ficheiro CSV contendo os dados de CO2.
    temp_output : str
        Caminho onde a imagem PNG temporária será guardada.
    """
    df_co2: pd.DataFrame = pd.read_csv(input_csv)
    
    p: figure = figure(
        title='CO2 Atmosférico ao Longo do Tempo',
        x_axis_label='Ano',
        y_axis_label='PPM'
    )
    
    p.line(df_co2['ano'], df_co2['ppm'], line_width=2, color='navy')
    p.circle(df_co2['ano'], df_co2['ppm'], size=8, color='navy', fill_color='white')

    chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    
    driver: webdriver.Chrome = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        export_png(p, filename=temp_output, webdriver=driver)
    finally:
        driver.quit()

def generate_correlation_visualization(input_csv: str, temp_output: str) -> None:
    """Calcula estimativas e correlação, gerando o terceiro gráfico em Matplotlib.

    Parameters
    ----------
    input_csv : str
        Caminho do ficheiro CSV contendo os dados de CO2.
    temp_output : str
        Caminho onde a imagem PNG temporária será guardada.
    """
    df_analysis: pd.DataFrame = pd.read_csv(input_csv)
    
    df_analysis['flipper_estimation'] = 180 + 14 * (df_analysis['ano'] - 2010)
    
    pearson_corr: float = df_analysis['ppm'].corr(df_analysis['flipper_estimation'])
    
    plt.figure(figsize=(6, 5))
    plt.scatter(df_analysis['ppm'], df_analysis['flipper_estimation'], color='purple')
    
    plt.title(f'Relação CO2 vs Barbatana (Corr: {pearson_corr:.4f})')
    plt.xlabel('Nível de CO2 (PPM)')
    plt.ylabel('Comprimento Estimado da Barbatana (mm)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(temp_output, bbox_inches='tight', dpi=100)
    plt.close()

def compose_final_image(temp_files: typing.List[str], output_filename: str) -> None:
    """Combina as três imagens temporárias num ficheiro JPEG final e limpa temporários.

    Parameters
    ----------
    temp_files : list of str
        Lista contendo os caminhos dos três ficheiros PNG temporários.
    output_filename : str
        Caminho do ficheiro JPEG final combinado.
    """
    images: typing.List[Image.Image] = [Image.open(x) for x in temp_files]
    
    widths: typing.List[int] = [img.width for img in images]
    heights: typing.List[int] = [img.height for img in images]

    total_width: int = sum(widths)
    max_height: int = max(heights)

    new_image: Image.Image = Image.new('RGB', (total_width, max_height), (255, 255, 255))

    x_offset: int = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width

    new_image.save(output_filename, format='JPEG', quality=95)

    for img in images:
        img.close()

    for file_path in temp_files:
        try:
            os.remove(file_path)
        except OSError:
            pass

def run_reporting_pipeline() -> None:
    """Orquestra a pipeline de geração e composição de gráficos."""
    penguins_data: str = 'pinguins_palmer.csv'
    co2_data: str = 'co2_maunaloa.csv'
    
    out_plotly: str = 'temp_plotly.png'
    out_bokeh: str = 'temp_bokeh.png'
    out_matplotlib: str = 'temp_matplotlib.png'
    final_jpeg: str = 'graficos_finais.jpg'
    
    temp_path_list: typing.List[str] = [out_plotly, out_bokeh, out_matplotlib]

    try:
        generate_plotly_visualization(penguins_data, out_plotly)
        generate_bokeh_visualization(co2_data, out_bokeh)
        generate_correlation_visualization(co2_data, out_matplotlib)
        
        compose_final_image(temp_path_list, final_jpeg)
        
    except FileNotFoundError as e:
        print(f'Erro de ficheiro: {e}')
    except Exception as e:
        print(f'Ocorreu um erro inesperado na pipeline: {e}')

if __name__ == '__main__':
    run_reporting_pipeline()