import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import click
from src.analyzer import Analyzer
from src.llm_processor import LLMProcessor

@click.command()
@click.option('--data-path', default='data/freelancer_earnings_bd.csv', help='Path to CSV data')
@click.option('--show-chart', is_flag=True, help='Show chart for region earnings distribution')
@click.option('--show-crypto-chart', is_flag=True, help='Show chart for cryptocurrency usage percentage')
@click.argument('query', required=False)
def main(data_path, query, show_chart, show_crypto_chart):
    analyzer = Analyzer(data_path)
    llm = LLMProcessor()
    
    if show_chart:
        chart = analyzer.get_region_earnings_chart()
        click.echo(click.style("=== Визуализация: Средний доход по регионам ===", fg="cyan"))
        click.echo(f"Тип графика: {chart['type']}")
        click.echo(click.style("Данные:", fg="yellow"))
        for label, value in zip(chart['data']['labels'], chart['data']['datasets'][0]['data']):
            click.echo(f"- {label}: {value:.2f} USD")
        click.echo("В UI это отобразится как интерактивный барный график.")
        return
    
    if show_crypto_chart:
        chart = analyzer.get_crypto_usage_chart()
        click.echo(click.style("=== Визуализация: Процент использования криптовалюты ===", fg="cyan"))
        click.echo(f"Тип графика: {chart['type']}")
        click.echo(click.style("Данные:", fg="yellow"))
        for label, value in zip(chart['data']['labels'], chart['data']['datasets'][0]['data']):
            click.echo(f"- {label}: {value:.2f}%")
        click.echo("В UI это отобразится как интерактивный круговой график.")
        return
    
    if not query:
        click.echo(click.style("=== Ошибка ===", fg="red"))
        click.echo("Введите запрос (например, 'Насколько выше доход у фрилансеров с криптовалютой?')")
        return
    
    query_type = llm.process_query(query)
    result = analyzer.custom_query(query_type)
    click.echo(click.style("=== Результат ===", fg="cyan"))
    click.echo(click.style(f"Запрос: {query}", fg="yellow"))
    click.echo(result)

if __name__ == "__main__":
    main()