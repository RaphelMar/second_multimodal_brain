# Diagnóstico de Chunks — ChromaDB

```text
════════════════════════════════════════════════════════════
  DIAGNÓSTICO DE CHUNKS — ChromaDB
  2026-03-31 10:54:17
════════════════════════════════════════════════════════════

⏳ Carregando documentos...
   1,192 documentos carregados.

📊 1. DISTRIBUIÇÃO DE TAMANHO
────────────────────────────────────────────────────────────
  Total de chunks: 1,192

  CARACTERES:
    Mínimo:         8
    Máximo:         1,000
    Média:          587.5
    Mediana:        612.0
    Desvio padrão:  307.3
    P5 / P95:       108.6 / 993.5

  PALAVRAS:
    Mínimo:         2
    Máximo:         204
    Média:          106.2
    Mediana:        111.0
    Desvio padrão:  55.4
    P5 / P95:       20.0 / 182.0

  TOKENS_EST:
    Mínimo:         2
    Máximo:         250
    Média:          146.5
    Mediana:        153.0
    Desvio padrão:  76.8
    P5 / P95:       27.0 / 248.0

⚠️ 2. OUTLIERS
────────────────────────────────────────────────────────────
  Chunks < 100 chars:  53 (4.45%)
  Chunks > 3000 chars: 0 (0.00%)

  Top 5 menores:
    [8 chars] ". Total." — CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPE
    [8 chars] "Vamos lá" — NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligênc
    [9 chars] "Boa sorte" — EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROB
    [10 chars] ". É mesmo?" — EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROB
    [11 chars] ". Obrigado." — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST

📁 3. DISTRIBUIÇÃO POR FONTE
────────────────────────────────────────────────────────────
  Total de fontes: 5

  Chunks por fonte:
    Mínimo:   195
    Máximo:   303
    Média:    238.4
    Mediana:  241.0

  Top 5 com MAIS chunks:
    [ 303] EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROBINSON FARI
    [ 254] VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU ESTÁ MORTO? E
    [ 241] NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligência Ltda. P
    [ 199] CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPEZ - Inteli
    [ 195] O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS BILENKY - I

  Top 5 com MENOS chunks:
    [ 195] O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS BILENKY - I
    [ 199] CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPEZ - Inteli
    [ 241] NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligência Ltda. P
    [ 254] VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU ESTÁ MORTO? E
    [ 303] EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROBINSON FARI

⏳ Carregando embeddings (amostragem)...

🧬 4. COESÃO SEMÂNTICA
────────────────────────────────────────────────────────────
  Fontes amostradas: 5

  Coesão média (sim. ao centroide): 0.5778
    Mínimo entre fontes:            0.5601
    Máximo entre fontes:            0.6116

  ✅ Coesão adequada (acima de 0.5).

🔀 5. SIMILARIDADE INTRA vs INTER-FONTE
────────────────────────────────────────────────────────────
  Fontes com embeddings válidos: 5

  Intra-fonte (mesma fonte):       0.3429
  Inter-fonte (fontes diferentes):  0.2835
  Ratio (intra/inter):              1.21x

  ✅ Chunks intra-fonte são 1.21x mais similares que inter-fonte.

🔍 6. TESTE DE RETRIEVAL
────────────────────────────────────────────────────────────

  ✅ "críticas ao poder do STF na política brasileira"
     Keywords encontradas: ['STF', 'Supremo']

  ✅ "ativismo judicial e decisões monocráticas no STF"
     Keywords encontradas: ['monocrática', 'ministro', 'Supremo']

  ✅ "papel da imprensa na cobertura do judiciário em Brasília"
     Keywords encontradas: ['imprensa', 'jornalismo', 'Brasília', 'judiciário']

  ✅ "polarização política e tensão entre os três poderes no Brasil"
     Keywords encontradas: ['Executivo', 'Legislativo', 'Judiciário']

  ✅ "Daniel Lopez lockdown climático e restrições de mobilidade"
     Keywords encontradas: ['lockdown', 'climático', 'transporte']

  ✅ "crise do petróleo e impacto no abastecimento de comida"
     Keywords encontradas: ['petróleo', 'supermercado', 'comida']

  ✅ "greve dos caminhoneiros 2018 e crise de abastecimento"
     Keywords encontradas: ['caminhoneiros', 'greve', 'abastecimento', '2018']

  ✅ "professor Universidade de Chicago conselheiro militar americano"
     Keywords encontradas: ['Chicago', 'conselheiro', 'Dying to Win', 'Bombing']

  ✅ "piores cenários para o Brasil e o mundo no curto prazo"
     Keywords encontradas: ['cenário', 'risco']

  Resultado: 9/9 queries com hit (100.0%)

════════════════════════════════════════════════════════════
  Diagnóstico concluído em 1.9s
════════════════════════════════════════════════════════════
```
