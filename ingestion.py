from src.ingestion.pipelines import youtube_pipeline



URL = "https://www.youtube.com/watch?v=KJaR4ReRYcE"
CATEGORIA = "teste"


n_chunks = youtube_pipeline.run(url= URL, category= CATEGORIA)

print(f"Ingestão concluída! {n_chunks} fragmentos armazenados na base de conhecimento.")