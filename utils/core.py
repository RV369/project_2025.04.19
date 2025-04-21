import pandas as pd


async def read_file_excel(excel) -> dict:
    """Читает файл, выводит содержимое в словарь"""
    df = pd.read_excel(excel, index_col=0)
    zuzublik = {
        'title': df.iat[0, 0],
        'url': df.iat[0, 1],
        'xpath': df.iat[0, 2],
    }
    return zuzublik
