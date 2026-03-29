# Diagnóstico de Chunks — ChromaDB

```text
════════════════════════════════════════════════════════════
  DIAGNÓSTICO DE CHUNKS — ChromaDB
  2026-03-29 15:13:55
════════════════════════════════════════════════════════════

⏳ Carregando documentos...
   1,213 documentos carregados.

📊 1. DISTRIBUIÇÃO DE TAMANHO
────────────────────────────────────────────────────────────
  Total de chunks: 1,213

  CARACTERES:
    Mínimo:         4
    Máximo:         10,989
    Média:          1,181.0
    Mediana:        724.0
    Desvio padrão:  1,389.4
    P5 / P95:       28.0 / 3,968.8

  PALAVRAS:
    Mínimo:         1
    Máximo:         2,061
    Média:          213.7
    Mediana:        133.0
    Desvio padrão:  249.8
    P5 / P95:       5.0 / 731.0

  TOKENS_EST:
    Mínimo:         1
    Máximo:         2,747
    Média:          294.9
    Mediana:        181.0
    Desvio padrão:  347.4
    P5 / P95:       7.0 / 991.8

⚠️ 2. OUTLIERS
────────────────────────────────────────────────────────────
  Chunks < 100 chars:  145 (11.95%)
  Chunks > 3000 chars: 111 (9.15%)

  ⛔ ALERTA: 12.0% dos chunks são muito pequenos. O SemanticChunker pode estar fragmentando demais.

  ⛔ ALERTA: 9.2% dos chunks são muito grandes. Considere reduzir o breakpoint_threshold_amount.

  Top 5 menores:
    [4 chars] "Irã." — GUERRA NO IRÃ E O GRANDE RESET: DANIEL LOPEZ - Int
    [4 chars] "Sim!" — ALEXANDRE e VORCARO + TRUMP CONTRA PCC e CV +  MAH
    [6 chars] "Mas..." — O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS B
    [6 chars] "Total." — NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligênc
    [6 chars] "É ali." — SEGREDOS REVELADOS DO SATANISMO: DANI PIRES E MÃE 

  Top 5 maiores:
    [10,989 chars] "Sim, sim. Helena, você pode primeiramente se apresentar Cont..." — VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU EST
    [10,741 chars] "Vai dar outra face? Eu vou dar. Você vai dar outro... Não, v..." — SEGREDOS REVELADOS DO SATANISMO: DANI PIRES E MÃE 
    [9,524 chars] "Tá, eu quero agora. Não sei, a gente vai descobrir ainda hoj..." — ALEXANDRE e VORCARO + TRUMP CONTRA PCC e CV +  MAH
    [9,386 chars] "Exatamente. O Irã tem 57 distritos, o exército está espalhad..." — EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROB
    [8,490 chars] "Você me perguntou, Vilela, antes sobre o fim da guerra. Veja..." — ALEXANDRE e VORCARO + TRUMP CONTRA PCC e CV +  MAH

📁 3. DISTRIBUIÇÃO POR FONTE
────────────────────────────────────────────────────────────
  Total de fontes: 10

  Chunks por fonte:
    Mínimo:   79
    Máximo:   166
    Média:    121.3
    Mediana:  115.5

  Top 5 com MAIS chunks:
    [ 166] BANCO MASTER: KIM KATAGUIRI, ACÁCIO MIRANDA E LUIZ FELIPE FR
    [ 164] GUERRA NO IRÃ E O GRANDE RESET: DANIEL LOPEZ - Inteligência 
    [ 151] DEBATE: IDOLATRIA - ARIEL LAZARI X ELIZEU RODRIGUES - Inteli
    [ 141] EUA X IRÃ: HAVERÁ UM VENCEDOR? - JOSÉ KOBORI E ROBINSON FARI
    [ 124] NOVO LOCKDOWN CHEGANDO?: DANIEL LOPEZ - Inteligência Ltda. P

  Top 5 com MENOS chunks:
    [  79] O BRASIL NAS MÃOS DO STF: CONRADO HÜBNER E THAIS BILENKY - I
    [  84] SEGREDOS REVELADOS DO SATANISMO: DANI PIRES E MÃE ANALU - In
    [  98] VORCARO VAI DELATAR! + CUBA CAIRÁ? + NETANYAHU ESTÁ MORTO? E
    [  99] ALEXANDRE e VORCARO + TRUMP CONTRA PCC e CV +  MAHSIMA X PEI
    [ 107] CONTAGEM REGRESSIVA PARA O APOCALIPSE: DANIEL LOPEZ - Inteli

⏳ Carregando embeddings (amostragem)...

🧬 4. COESÃO SEMÂNTICA
────────────────────────────────────────────────────────────
  Fontes amostradas: 10

  Coesão média (sim. ao centroide): 0.5941
    Mínimo entre fontes:            0.5718
    Máximo entre fontes:            0.6272

  ✅ Coesão adequada (acima de 0.5).

🔀 5. SIMILARIDADE INTRA vs INTER-FONTE
────────────────────────────────────────────────────────────
  Fontes com embeddings válidos: 10

  Intra-fonte (mesma fonte):       0.3722
  Inter-fonte (fontes diferentes):  0.2923
  Ratio (intra/inter):              1.27x

  ✅ Chunks intra-fonte são 1.27x mais similares que inter-fonte.

🔍 6. TESTE DE RETRIEVAL
────────────────────────────────────────────────────────────

  ✅ "críticas ao poder do STF na política brasileira"
     Keywords encontradas: ['STF', 'Supremo']

  ✅ "ativismo judicial e decisões monocráticas no STF"
     Keywords encontradas: ['monocrática', 'ministro', 'Supremo']

  ✅ "papel da imprensa na cobertura do judiciário em Brasília"
     Keywords encontradas: ['imprensa', 'jornalismo']

  ✅ "polarização política e tensão entre os três poderes no Brasil"
     Keywords encontradas: ['polarização', 'Executivo', 'Legislativo', 'Judiciário']

  ✅ "Daniel Lopez lockdown climático e restrições de mobilidade"
     Keywords encontradas: ['lockdown', 'climático', 'transporte']

  ✅ "agenda climática como instrumento de controle estatal"
     Keywords encontradas: ['controle', 'governo']

  ✅ "crise do petróleo e impacto no abastecimento de comida"
     Keywords encontradas: ['petróleo', 'comida']

  ✅ "greve dos caminhoneiros 2018 e crise de abastecimento"
     Keywords encontradas: ['caminhoneiros', 'greve', 'abastecimento', '2018']

  ✅ "professor Universidade de Chicago conselheiro militar americano"
     Keywords encontradas: ['Chicago', 'conselheiro', 'Dying to Win', 'Bombing']

  ✅ "piores cenários para o Brasil e o mundo no curto prazo"
     Keywords encontradas: ['cenário']

  Resultado: 10/10 queries com hit (100.0%)

════════════════════════════════════════════════════════════
  Diagnóstico concluído em 2.6s
════════════════════════════════════════════════════════════
```
