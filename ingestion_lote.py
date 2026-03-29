import polars as pl
from src.ingestion.pipelines import youtube_pipeline

df = (
    pl.read_excel("data/temp/links.xlsx")
    .slice(0, 10)
)

for row in df.iter_rows(named= True):
    URL = row["Link"]
    CATEGORIA = row["Categoria"]

    print("\n")
    print("=" * 50)
    n_chunks = youtube_pipeline.run(url= URL, category= CATEGORIA)
    print(f"Ingestão concluída! {n_chunks} fragmentos armazenados na base de conhecimento.")
    print("=" * 50)
    print("\n")

