import pandas as pd

REQUIRED_COLUMNS = ['symbol', 'trade type', 'quantity', 'price']

def parse_tradebook(file) -> pd.DataFrame:
    """
    Parses a Zerodha tradebook CSV and summarizes buy/sell activity.
    """

    df = pd.read_csv(file)

    # Normalize column names: lowercase and strip spaces
    df.columns = df.columns.str.strip().str.lower()

    # Ensure required columns exist
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing)}")

    # Optional filtering: only EQ segment if present
    if 'segment' in df.columns:
        df = df[df['segment'].str.upper() == 'EQ']

    # Rename for summary
    df = df.rename(columns={
        'symbol': 'Stock Name',
        'trade type': 'Buy/Sell Type',
        'quantity': 'Quantity',
        'price': 'Price'
    })

    # Ensure numeric
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df.dropna(subset=['Quantity', 'Price'], inplace=True)

    # Compute summary
    summary = (
        df.groupby(['Stock Name', 'Buy/Sell Type'])
        .agg(
            Quantity=('Quantity', 'sum'),
            Avg_Price=('Price', 'mean'),
            Total_Value=('Price', lambda x: (x * df.loc[x.index, 'Quantity']).sum())
        )
        .reset_index()
    )

    summary['Avg_Price'] = summary['Avg_Price'].round(2)
    summary['Total_Value'] = summary['Total_Value'].round(2)

    return summary
