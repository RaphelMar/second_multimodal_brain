"""
Diagnóstico de qualidade dos chunks armazenados no ChromaDB.

Uso:
    python -m src.diagnostics.chunk_report

Métricas calculadas:
    1. Distribuição de tamanho (caracteres, palavras, tokens estimados)
    2. Detecção de outliers (chunks muito pequenos ou muito grandes)
    3. Distribuição por fonte (chunks por vídeo/documento)
    4. Coesão semântica (similaridade dos embeddings ao centroide da fonte)
    5. Similaridade intra-fonte vs inter-fonte
    6. Teste de retrieval com queries predefinidas
"""

from __future__ import annotations

import random
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np

from src.database.chroma_wrapper import VectorDB
from src.config.logger import logger


# ── Thresholds configuráveis ──────────────────────────────────────────

MIN_CHUNK_CHARS = 100       # Abaixo disso → chunk muito pequeno
MAX_CHUNK_CHARS = 3000      # Acima disso → chunk muito grande
OUTLIER_WARN_PCT = 5.0      # Alerta se outliers passarem desse %
COHESION_WARN = 0.5         # Alerta se coesão média cair abaixo disso
SAMPLE_SOURCES = 20         # Fontes amostradas pra métricas de embedding
SAMPLE_PAIRS = 200          # Pares amostrados pra similaridade intra/inter

# Queries de teste — CUSTOMIZE PARA SEU CASO DE USO
# Formato: ("query de busca", ["keyword1", "keyword2"])
# O teste verifica se pelo menos uma keyword aparece nos chunks retornados.
DEFAULT_TEST_QUERIES: list[tuple[str, list[str]]] = [
    # ── STF e política (Conrado Hübner e Thais Bilenky)
    (
        "críticas ao poder do STF na política brasileira",
        ["STF", "Supremo", "monocrática", "ativismo"],
    ),
    (
        "ativismo judicial e decisões monocráticas no STF",
        ["monocrática", "ativismo", "ministro", "Supremo"],
    ),
    (
        "papel da imprensa na cobertura do judiciário em Brasília",
        ["imprensa", "jornalismo", "Brasília", "judiciário"],
    ),
    (
        "polarização política e tensão entre os três poderes no Brasil",
        ["polarização", "Executivo", "Legislativo", "Judiciário"],
    ),
    # ── Lockdown e controle (Daniel Lopez)
    (
        "Daniel Lopez lockdown climático e restrições de mobilidade",
        ["lockdown", "climático", "mobilidade", "transporte"],
    ),
    # ── Geopolítica e crise
    (
        "crise do petróleo e impacto no abastecimento de comida",
        ["petróleo", "supermercado", "comida", "abastecimento"],
    ),
    (
        "greve dos caminhoneiros 2018 e crise de abastecimento",
        ["caminhoneiros", "greve", "abastecimento", "2018"],
    ),
    (
        "professor Universidade de Chicago conselheiro militar americano",
        ["Chicago", "conselheiro", "Dying to Win", "Bombing"],
    ),
    # ── Cenário macro
    (
        "piores cenários para o Brasil e o mundo no curto prazo",
        ["cenário", "crise", "risco", "colapso"],
    ),
]


class ChunkDiagnostics:
    """
    Diagnóstico completo de qualidade dos chunks no ChromaDB.

    Lê direto do banco via VectorDB, calcula 6 métricas e gera relatório
    no terminal + markdown.
    """

    def __init__(self):
        self._db = VectorDB()
        # Acesso direto à collection do Chroma pra queries de diagnóstico.
        # Necessário porque o wrapper do LangChain não expõe metadados em bulk.
        self._collection = self._db._db._collection
        self._lines: list[str] = []

    # ── Helpers ────────────────────────────────────────────────────────

    def _log(self, text: str = "") -> None:
        """Imprime no terminal e armazena pra exportação markdown."""
        print(text)
        self._lines.append(text)

    def _header(self, emoji: str, title: str) -> None:
        self._log()
        self._log(f"{emoji} {title}")
        self._log("─" * 60)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """~4 caracteres por token em português."""
        return len(text) // 4

    @staticmethod
    def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
        """Similaridade cosseno entre dois vetores."""
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    # ── Carga de dados ─────────────────────────────────────────────────

    def _load_all_docs(self) -> dict:
        """Carrega todos os documentos e metadados (sem embeddings — rápido)."""
        return self._collection.get(include=["documents", "metadatas"])

    def _load_source_embeddings(self, source_id: str) -> dict:
        """Carrega embeddings de uma fonte específica."""
        return self._collection.get(
            where={"source_id": source_id},
            include=["documents", "embeddings"],
        )

    # ── Métrica 1: Distribuição de tamanho ─────────────────────────────

    def _metric_size_distribution(self, documents: list[str]) -> dict:
        """Distribuição de caracteres, palavras e tokens por chunk."""
        chars = np.array([len(d) for d in documents])
        words = np.array([len(d.split()) for d in documents])
        tokens = np.array([self._estimate_tokens(d) for d in documents])

        stats = {}
        for name, arr in [("caracteres", chars), ("palavras", words), ("tokens_est", tokens)]:
            stats[name] = {
                "min": int(np.min(arr)),
                "max": int(np.max(arr)),
                "media": round(float(np.mean(arr)), 1),
                "mediana": round(float(np.median(arr)), 1),
                "desvio_padrao": round(float(np.std(arr)), 1),
                "p5": round(float(np.percentile(arr, 5)), 1),
                "p95": round(float(np.percentile(arr, 95)), 1),
            }

        self._header("📊", "1. DISTRIBUIÇÃO DE TAMANHO")
        self._log(f"  Total de chunks: {len(documents):,}")

        for name, s in stats.items():
            self._log(f"\n  {name.upper()}:")
            self._log(f"    Mínimo:         {s['min']:,}")
            self._log(f"    Máximo:         {s['max']:,}")
            self._log(f"    Média:          {s['media']:,.1f}")
            self._log(f"    Mediana:        {s['mediana']:,.1f}")
            self._log(f"    Desvio padrão:  {s['desvio_padrao']:,.1f}")
            self._log(f"    P5 / P95:       {s['p5']:,.1f} / {s['p95']:,.1f}")

        return stats

    # ── Métrica 2: Outliers ────────────────────────────────────────────

    def _metric_outliers(self, documents: list[str], metadatas: list[dict]) -> dict:
        """Detecta chunks anormalmente pequenos ou grandes."""
        total = len(documents)
        small = [(i, len(documents[i])) for i in range(total) if len(documents[i]) < MIN_CHUNK_CHARS]
        large = [(i, len(documents[i])) for i in range(total) if len(documents[i]) > MAX_CHUNK_CHARS]

        small_pct = (len(small) / total) * 100 if total else 0
        large_pct = (len(large) / total) * 100 if total else 0

        self._header("⚠️", "2. OUTLIERS")
        self._log(f"  Chunks < {MIN_CHUNK_CHARS} chars:  {len(small):,} ({small_pct:.2f}%)")
        self._log(f"  Chunks > {MAX_CHUNK_CHARS} chars: {len(large):,} ({large_pct:.2f}%)")

        if small_pct > OUTLIER_WARN_PCT:
            self._log(
                f"\n  ⛔ ALERTA: {small_pct:.1f}% dos chunks são muito pequenos. "
                f"O SemanticChunker pode estar fragmentando demais."
            )
        if large_pct > OUTLIER_WARN_PCT:
            self._log(
                f"\n  ⛔ ALERTA: {large_pct:.1f}% dos chunks são muito grandes. "
                f"Considere reduzir o breakpoint_threshold_amount."
            )

        # Top 5 menores
        small_sorted = sorted(small, key=lambda x: x[1])[:5]
        if small_sorted:
            self._log(f"\n  Top 5 menores:")
            for idx, size in small_sorted:
                title = metadatas[idx].get("title", "?")[:50]
                preview = documents[idx][:60].replace("\n", " ")
                self._log(f"    [{size:,} chars] \"{preview}\" — {title}")

        # Top 5 maiores
        large_sorted = sorted(large, key=lambda x: x[1], reverse=True)[:5]
        if large_sorted:
            self._log(f"\n  Top 5 maiores:")
            for idx, size in large_sorted:
                title = metadatas[idx].get("title", "?")[:50]
                preview = documents[idx][:60].replace("\n", " ")
                self._log(f"    [{size:,} chars] \"{preview}...\" — {title}")

        return {
            "small_count": len(small),
            "small_pct": round(small_pct, 2),
            "large_count": len(large),
            "large_pct": round(large_pct, 2),
        }

    # ── Métrica 3: Distribuição por fonte ──────────────────────────────

    def _metric_source_distribution(self, metadatas: list[dict]) -> dict:
        """Quantos chunks cada fonte (vídeo/documento) gerou."""
        sources: dict[str, str] = {}       # source_id → title
        counts: Counter[str] = Counter()

        for m in metadatas:
            sid = m.get("source_id", "desconhecido")
            counts[sid] += 1
            if sid not in sources:
                sources[sid] = m.get("title", sid[:16])

        per_source = np.array(list(counts.values()))

        self._header("📁", "3. DISTRIBUIÇÃO POR FONTE")
        self._log(f"  Total de fontes: {len(counts):,}")
        self._log(f"\n  Chunks por fonte:")
        self._log(f"    Mínimo:   {int(np.min(per_source)):,}")
        self._log(f"    Máximo:   {int(np.max(per_source)):,}")
        self._log(f"    Média:    {np.mean(per_source):.1f}")
        self._log(f"    Mediana:  {np.median(per_source):.1f}")

        # Top 5 mais chunks
        self._log(f"\n  Top 5 com MAIS chunks:")
        for sid, count in counts.most_common(5):
            self._log(f"    [{count:>4}] {sources[sid][:60]}")

        # Top 5 menos chunks
        self._log(f"\n  Top 5 com MENOS chunks:")
        for sid, count in counts.most_common()[:-6:-1]:
            self._log(f"    [{count:>4}] {sources[sid][:60]}")

        return {
            "total_sources": len(counts),
            "min": int(np.min(per_source)),
            "max": int(np.max(per_source)),
            "mean": round(float(np.mean(per_source)), 1),
            "source_ids": list(counts.keys()),
        }

    # ── Métrica 4: Coesão semântica ───────────────────────────────────

    def _metric_semantic_cohesion(self, source_ids: list[str]) -> dict:
        """
        Mede o quão coesos são os chunks dentro de cada fonte.

        Para cada fonte amostrada, calcula o centroide (embedding médio) e
        mede a similaridade cosseno de cada chunk ao centroide. Quanto mais
        alto, mais os chunks de uma mesma fonte "falam sobre a mesma coisa".
        """
        sampled = random.sample(source_ids, min(SAMPLE_SOURCES, len(source_ids)))
        cohesion_scores: list[float] = []

        self._header("🧬", "4. COESÃO SEMÂNTICA")
        self._log(f"  Fontes amostradas: {len(sampled)}")

        for sid in sampled:
            data = self._load_source_embeddings(sid)
            embeddings = data.get("embeddings")

            if embeddings is None or len(embeddings) < 2:
                continue

            emb_array = np.array(embeddings, dtype=np.float32)
            centroid = emb_array.mean(axis=0)

            sims = [self._cosine_sim(emb, centroid) for emb in emb_array]
            cohesion_scores.append(float(np.mean(sims)))

        if not cohesion_scores:
            self._log("  ⚠️ Não foi possível calcular (embeddings indisponíveis).")
            return {"mean_cohesion": 0.0, "scores": []}

        overall = float(np.mean(cohesion_scores))
        self._log(f"\n  Coesão média (sim. ao centroide): {overall:.4f}")
        self._log(f"    Mínimo entre fontes:            {min(cohesion_scores):.4f}")
        self._log(f"    Máximo entre fontes:            {max(cohesion_scores):.4f}")

        if overall < COHESION_WARN:
            self._log(
                f"\n  ⛔ ALERTA: Coesão abaixo de {COHESION_WARN}. "
                f"Chunks podem estar fragmentados demais."
            )
        else:
            self._log(f"\n  ✅ Coesão adequada (acima de {COHESION_WARN}).")

        return {"mean_cohesion": overall, "scores": cohesion_scores}

    # ── Métrica 5: Intra vs Inter-fonte ───────────────────────────────

    def _metric_intra_vs_inter(self, source_ids: list[str]) -> dict:
        """
        Compara similaridade entre chunks da MESMA fonte vs fontes DIFERENTES.

        Ratio alto (>1.2) = chunks capturam informação específica de cada fonte.
        Ratio baixo (~1.0) = chunks de fontes diferentes são indistinguíveis.
        """
        sampled = random.sample(source_ids, min(SAMPLE_SOURCES, len(source_ids)))

        # Carrega embeddings das fontes amostradas
        source_embs: dict[str, np.ndarray] = {}
        for sid in sampled:
            data = self._load_source_embeddings(sid)
            embs = data.get("embeddings")
            if embs is not None and len(embs) >= 2:
                source_embs[sid] = np.array(embs, dtype=np.float32)

        self._header("🔀", "5. SIMILARIDADE INTRA vs INTER-FONTE")

        if len(source_embs) < 2:
            self._log("  ⚠️ Fontes insuficientes para comparação (mínimo: 2).")
            return {"intra": 0.0, "inter": 0.0, "ratio": 0.0}

        self._log(f"  Fontes com embeddings válidos: {len(source_embs)}")

        # Intra-fonte: pares de chunks da MESMA fonte
        intra_sims: list[float] = []
        for embs in source_embs.values():
            n = len(embs)
            n_pairs = min(SAMPLE_PAIRS // len(source_embs), n * (n - 1) // 2)
            indices = list(range(n))
            for _ in range(max(n_pairs, 1)):
                i, j = random.sample(indices, 2)
                intra_sims.append(self._cosine_sim(embs[i], embs[j]))

        # Inter-fonte: pares de chunks de fontes DIFERENTES
        inter_sims: list[float] = []
        sids = list(source_embs.keys())
        for _ in range(SAMPLE_PAIRS):
            s1, s2 = random.sample(sids, 2)
            i = random.randint(0, len(source_embs[s1]) - 1)
            j = random.randint(0, len(source_embs[s2]) - 1)
            inter_sims.append(self._cosine_sim(source_embs[s1][i], source_embs[s2][j]))

        intra_mean = float(np.mean(intra_sims))
        inter_mean = float(np.mean(inter_sims))
        ratio = intra_mean / inter_mean if inter_mean > 0 else 0.0

        self._log(f"\n  Intra-fonte (mesma fonte):       {intra_mean:.4f}")
        self._log(f"  Inter-fonte (fontes diferentes):  {inter_mean:.4f}")
        self._log(f"  Ratio (intra/inter):              {ratio:.2f}x")

        if ratio < 1.2:
            self._log(
                f"\n  ⛔ ALERTA: Ratio baixo ({ratio:.2f}x). Chunks de fontes diferentes"
                f"\n     são muito similares — o chunking pode não estar capturando"
                f"\n     informação específica de cada fonte."
            )
        else:
            self._log(f"\n  ✅ Chunks intra-fonte são {ratio:.2f}x mais similares que inter-fonte.")

        return {"intra": intra_mean, "inter": inter_mean, "ratio": round(ratio, 2)}

    # ── Métrica 6: Teste de retrieval ─────────────────────────────────

    def _metric_retrieval_test(self, test_queries: list[tuple[str, list[str]]]) -> dict:
        """
        Executa queries de teste e verifica se as keywords esperadas
        aparecem nos chunks retornados.
        """
        self._header("🔍", "6. TESTE DE RETRIEVAL")

        if not test_queries:
            self._log("  ⚠️ Nenhuma query de teste definida.")
            self._log("")
            self._log("  Para usar esta métrica, defina suas queries no topo do módulo")
            self._log("  (DEFAULT_TEST_QUERIES) ou passe via parâmetro em run_all().")
            self._log('  Formato: [("query", ["keyword1", "keyword2"]), ...]')
            return {"total": 0, "hits": 0, "hit_rate": 0.0}

        retriever = self._db.retriever(k=5)
        hits = 0

        for query, expected_keywords in test_queries:
            try:
                docs = retriever.invoke(query)
                combined = " ".join(d.page_content.lower() for d in docs)
                found = [kw for kw in expected_keywords if kw.lower() in combined]
                is_hit = len(found) > 0

                status = "✅" if is_hit else "❌"
                self._log(f"\n  {status} \"{query}\"")
                self._log(f"     Keywords encontradas: {found if found else 'nenhuma'}")

                if is_hit:
                    hits += 1

            except Exception as e:
                self._log(f"\n  ⚠️ Erro na query \"{query}\": {e}")

        hit_rate = (hits / len(test_queries)) * 100
        self._log(f"\n  Resultado: {hits}/{len(test_queries)} queries com hit ({hit_rate:.1f}%)")

        return {"total": len(test_queries), "hits": hits, "hit_rate": round(hit_rate, 1)}

    # ── Execução principal ─────────────────────────────────────────────

    def run_all(self, test_queries: list[tuple[str, list[str]]] | None = None) -> None:
        """Executa todas as métricas e imprime relatório no terminal."""
        start = time.time()
        self._lines = []

        self._log("═" * 60)
        self._log("  DIAGNÓSTICO DE CHUNKS — ChromaDB")
        self._log(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log("═" * 60)

        # ── Carrega dados base (sem embeddings — rápido)
        self._log("\n⏳ Carregando documentos...")
        data = self._load_all_docs()
        documents = data["documents"]
        metadatas = data["metadatas"]
        self._log(f"   {len(documents):,} documentos carregados.")

        if not documents:
            self._log("\n⛔ Banco vazio. Nenhuma métrica calculada.")
            return

        # ── Métricas 1-3 (rápidas, sem embeddings)
        self._metric_size_distribution(documents)
        self._metric_outliers(documents, metadatas)
        source_stats = self._metric_source_distribution(metadatas)

        # ── Métricas 4-5 (amostragem com embeddings)
        source_ids = source_stats.get("source_ids", [])
        if len(source_ids) >= 2:
            self._log("\n⏳ Carregando embeddings (amostragem)...")
            self._metric_semantic_cohesion(source_ids)
            self._metric_intra_vs_inter(source_ids)
        else:
            self._log("\n⚠️ Menos de 2 fontes — métricas de embedding ignoradas.")

        # ── Métrica 6 (retrieval)
        queries = test_queries or DEFAULT_TEST_QUERIES
        self._metric_retrieval_test(queries)

        # ── Resumo
        elapsed = time.time() - start
        self._log()
        self._log("═" * 60)
        self._log(f"  Diagnóstico concluído em {elapsed:.1f}s")
        self._log("═" * 60)

    def save_markdown(self, path: str = "reports/chunk_diagnostics.md") -> None:
        """Salva o relatório gerado por run_all() como markdown."""
        if not self._lines:
            logger.warning("Nenhum relatório gerado. Execute run_all() antes.")
            return

        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            f.write("# Diagnóstico de Chunks — ChromaDB\n\n")
            f.write("```text\n")
            for line in self._lines:
                f.write(line + "\n")
            f.write("```\n")

        print(f"\n📄 Relatório salvo em: {output}")


# ── Entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    diag = ChunkDiagnostics()
    diag.run_all()
    diag.save_markdown()