import pandas as pd

def parse_tradebook(file) -> pd.DataFrame:
    """
    Parses a Zerodha tradebook CSV file and returns a summary DataFrame.

    Columns in tradebook typically include:
    ['Trade Date', 'Exchange', 'Segment', 'Instrument Type', 'Symbol', 'Trade Type',
     'Quantity', 'Price', 'Order No', ...]
    """

    df = pd.read_csv(file)

    # Filter only Equity trades (optional: Segment == 'EQ')
    df = df[df['Segment'].str.upper() == 'EQ']

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename for simplicity
    df = df.rename(columns={
        'symbol': 'Stock Name',
        'trade type': 'Buy/Sell Type',
        'quantity': 'Quantity',
        'price': 'Price'
    })

    # Group by Stock and Buy/Sell Type
    summary = (
        df.groupby(['Stock Name', 'Buy/Sell Type'])
        .agg(
            Quantity=('Quantity', 'sum'),
            Avg_Price=('Price', 'mean'),
            Total_Value=('Price', lambda x: (x * df.loc[x.index, 'Quantity']).sum())
        )
        .reset_index()
    )

    # Round values for display
    summary['Avg_Price'] = summary['Avg_Price'].round(2)
    summary['Total_Value'] = summary['Total_Value'].round(2)

    return summary
