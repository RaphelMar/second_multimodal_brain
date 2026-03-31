# Diagnóstico de Chunks — ChromaDB

```text
════════════════════════════════════════════════════════════
  DIAGNÓSTICO DE CHUNKS — ChromaDB
  2026-03-30 12:30:25
════════════════════════════════════════════════════════════

⏳ Carregando documentos...
   688 documentos carregados.

📊 1. DISTRIBUIÇÃO DE TAMANHO
────────────────────────────────────────────────────────────
  Total de chunks: 688

  CARACTERES:
    Mínimo:         88
    Máximo:         10,989
    Média:          948.0
    Mediana:        589.5
    Desvio padrão:  1,110.4
    P5 / P95:       120.3 / 2,970.1

  PALAVRAS:
    Mínimo:         14
    Máximo:         1,955
    Média:          170.9
    Mediana:        108.0
    Desvio padrão:  197.1
    P5 / P95:       22.4 / 544.6

  TOKENS_EST:
    Mínimo:         22
    Máximo:         2,747
    Média:          236.6
    Mediana:        147.0
    Desvio padrão:  277.6
    P5 / P95:       30.0 / 742.2

⚠️ 2. OUTLIERS
────────────────────────────────────────────────────────────
  Chunks < 100 chars:  14 (2.03%)
  Chunks > 3000 chars: 33 (4.80%)

  Top 5 menores:
    [88 chars] "Deu prazo de hoje. Só que ele mexeu no prazo hoje de manhã. " — CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPE
    [89 chars] "Enquanto isso, manda uma pergunta aí. Depois eu vou concluir" — NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligênc
    [89 chars] "Não porque eles mudaram de opinião ou porque o Alexandre se " — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST
    [91 chars] "É, balarina não vi ainda. E todo dia eu chego em casa e meu " — NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligênc
    [91 chars] "Jornal. Também comentam sobre o assunto. E no quadro Se For " — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST

  Top 5 maiores:
    [10,989 chars] "Sim, sim. Helena, você pode primeiramente se apresentar Cont..." — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST
    [7,002 chars] "Então vamos lá, Silvia. A Silvia que na verdade é a favor aí..." — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST
    [6,895 chars] "Posso começar Ele surge quando? Foi no primeiro governo Prim..." — O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS B
    [6,551 chars] "Começando por Israel, claro que tem uma experiência ali de d..." — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST
    [6,418 chars] "Não é dizer que essa interação sempre é regular e não sujeit..." — O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS B

📁 3. DISTRIBUIÇÃO POR FONTE
────────────────────────────────────────────────────────────
  Total de fontes: 5

  Chunks por fonte:
    Mínimo:   94
    Máximo:   179
    Média:    137.6
    Mediana:  136.0

  Top 5 com MAIS chunks:
    [ 179] EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROBINSON FARI
    [ 160] NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligência Ltda. P
    [ 136] CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPEZ - Inteli
    [ 119] VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU ESTÁ MORTO? E
    [  94] O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS BILENKY - I

  Top 5 com MENOS chunks:
    [  94] O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS BILENKY - I
    [ 119] VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU ESTÁ MORTO? E
    [ 136] CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPEZ - Inteli
    [ 160] NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligência Ltda. P
    [ 179] EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROBINSON FARI

⏳ Carregando embeddings (amostragem)...

🧬 4. COESÃO SEMÂNTICA
────────────────────────────────────────────────────────────
  Fontes amostradas: 5

  Coesão média (sim. ao centroide): 0.5894
    Mínimo entre fontes:            0.5740
    Máximo entre fontes:            0.6223

  ✅ Coesão adequada (acima de 0.5).

🔀 5. SIMILARIDADE INTRA vs INTER-FONTE
────────────────────────────────────────────────────────────
  Fontes com embeddings válidos: 5

  Intra-fonte (mesma fonte):       0.3369
  Inter-fonte (fontes diferentes):  0.3021
  Ratio (intra/inter):              1.12x

  ⛔ ALERTA: Ratio baixo (1.12x). Chunks de fontes diferentes
     são muito similares — o chunking pode não estar capturando
     informação específica de cada fonte.

🔍 6. TESTE DE RETRIEVAL
────────────────────────────────────────────────────────────

  ✅ "críticas ao poder do STF na política brasileira"
     Keywords encontradas: ['STF', 'Supremo']

  ✅ "ativismo judicial e decisões monocráticas no STF"
     Keywords encontradas: ['monocrática', 'ministro', 'Supremo']

  ✅ "papel da imprensa na cobertura do judiciário em Brasília"
     Keywords encontradas: ['imprensa', 'jornalismo', 'Brasília']

  ✅ "polarização política e tensão entre os três poderes no Brasil"
     Keywords encontradas: ['Executivo', 'Legislativo', 'Judiciário']

  ✅ "Daniel Lopez lockdown climático e restrições de mobilidade"
     Keywords encontradas: ['lockdown', 'climático', 'transporte']

  ✅ "crise do petróleo e impacto no abastecimento de comida"
     Keywords encontradas: ['petróleo', 'supermercado', 'comida', 'abastecimento']

  ✅ "greve dos caminhoneiros 2018 e crise de abastecimento"
     Keywords encontradas: ['caminhoneiros', 'greve', 'abastecimento', '2018']

  ✅ "professor Universidade de Chicago conselheiro militar americano"
     Keywords encontradas: ['Chicago', 'conselheiro', 'Dying to Win', 'Bombing']

  ✅ "piores cenários para o Brasil e o mundo no curto prazo"
     Keywords encontradas: ['cenário', 'crise']

  Resultado: 9/9 queries com hit (100.0%)

════════════════════════════════════════════════════════════
  Diagnóstico concluído em 0.8s
════════════════════════════════════════════════════════════
```
