from sqlalchemy import create_engine

def save_dataframe(df, table_name):
    engine = create_engine("sqlite:///db/app.db")
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )