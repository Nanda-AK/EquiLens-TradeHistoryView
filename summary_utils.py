import pandas as pd

REQUIRED_COLUMNS = ['symbol', 'trade_type', 'quantity', 'price', 'trade_date']

def get_trade_date_range(df):
    df_copy = df.copy()
    df_copy['trade_date'] = pd.to_datetime(df_copy['trade_date'], dayfirst=True)
    oldest_date = df_copy['trade_date'].min().strftime("%d-%b-%Y")
    latest_date = df_copy['trade_date'].max().strftime("%d-%b-%Y")
    return oldest_date, latest_date


def parse_tradebook(file) -> pd.DataFrame:

    file.seek(0)  # ✅ Reset pointer before parsing
    df = pd.read_csv(file)
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Validate required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing)}")

    # Optional: filter for segment == EQ
    if 'segment' in df.columns:
        df = df[df['segment'].str.upper() == 'EQ']

    # Clean and rename
    df = df.rename(columns={
        'symbol': 'Stock Name',
        'trade_type': 'Buy/Sell Type',
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
