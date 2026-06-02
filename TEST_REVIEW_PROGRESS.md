# Test Review Progress (Agent-Friendly)

## Rules
- Fixed record file: `TEST_REVIEW_PROGRESS.md`
- Record format: list entries (one per phase) with structured fields
- Status enum: `PASS` | `FAIL` | `PENDING`

## Phase Status List
- phase: C1
  date: 2026-05-25
  status: PASS
  summary: Core data type contracts verified
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_core_types.py"
  result: "8 passed"
  files:
    - "src/core/types.py"
    - "src/core/__init__.py"
    - "tests/unit/test_core_types.py"
  failures: []

- phase: C2
  date: 2026-05-25
  status: PASS
  summary: SHA256 + SQLite integrity checks passed (including extra boundary tests)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_file_integrity.py tests/unit/test_file_integrity_contract_extra.py"
  result: "14 passed"
  files:
    - "src/libs/loader/file_integrity.py"
    - "src/libs/loader/__init__.py"
    - "tests/unit/test_file_integrity.py"
    - "tests/unit/test_file_integrity_contract_extra.py"
  failures: []

- phase: C3
  date: 2026-05-25
  status: FAIL
  summary: Loader abstraction + PDF Loader had 2 confirmed issues
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_loader_pdf_contract.py tests/unit/test_loader_pdf_contract_extra.py"
  result: "2 failed, 8 passed"
  files:
    - "src/libs/loader/base_loader.py"
    - "src/libs/loader/pdf_loader.py"
    - "tests/unit/test_loader_pdf_contract.py"
    - "tests/unit/test_loader_pdf_contract_extra.py"
  failures:
    - test: "test_pdf_loader_rejects_non_string_text_extractor_output"
      error: "Failed: DID NOT RAISE <class 'TypeError'>"
      cause: "non-string text_extractor output was silently stringified instead of fail-fast"
      locations:
        - "src/libs/loader/pdf_loader.py:54"
    - test: "test_pdf_loader_ignores_invalid_image_items_without_crashing"
      error: "ValueError: metadata.images[1].id must be a non-empty string"
      cause: "invalid image records were not filtered before Document contract validation"
      locations:
        - "src/libs/loader/pdf_loader.py:72"
        - "src/core/types.py:67"

- phase: C3-retest-1
  date: 2026-05-25
  status: PASS
  summary: C3 fixes verified with broader boundary and error-path coverage
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_loader_pdf_contract.py tests/unit/test_loader_pdf_contract_extra.py"
  result: "14 passed"
  files:
    - "src/libs/loader/base_loader.py"
    - "src/libs/loader/pdf_loader.py"
    - "tests/unit/test_loader_pdf_contract.py"
    - "tests/unit/test_loader_pdf_contract_extra.py"
  failures: []

- phase: C4-recheck-1
  date: 2026-05-25
  status: FAIL
  summary: C4 was placeholder-only at that time, with missing tests
  commands:
    - "Get-Content src/ingestion/chunking/document_chunker.py"
    - "rg --files tests | rg \"chunker|chunking|document_chunker\""
  result: "document_chunker.py was placeholder; no C4 tests found"
  files:
    - "src/ingestion/chunking/document_chunker.py"
    - "src/ingestion/chunking/__init__.py"
  failures:
    - test: "N/A"
      error: "C4 implementation missing"
      cause: "Document chunking integration logic absent"
      locations:
        - "src/ingestion/chunking/document_chunker.py:1"

- phase: C5-recheck-1
  date: 2026-05-25
  status: PASS
  summary: C5 ChunkRefiner logic and unit tests passed; integration skipped without OPENAI_API_KEY
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_chunk_refiner.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_chunk_refiner_llm.py"
  result: "unit: 15 passed; integration: 2 skipped"
  files:
    - "src/ingestion/transform/base_transform.py"
    - "src/ingestion/transform/chunk_refiner.py"
    - "tests/unit/test_chunk_refiner.py"
    - "tests/integration/test_chunk_refiner_llm.py"
    - "tests/fixtures/noisy_chunks.json"
  failures: []

- phase: C4-C5-unified-test-1
  date: 2026-05-25
  status: PASS
  summary: Unified C4/C5 regression passed; C5 online LLM integration skipped as expected
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_document_chunker.py tests/unit/test_document_chunker_contract_extra.py tests/unit/test_chunk_refiner.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_chunk_refiner_llm.py"
  result: "unit: 26 passed; integration: 2 skipped"
  files:
    - "src/ingestion/chunking/document_chunker.py"
    - "src/ingestion/transform/base_transform.py"
    - "src/ingestion/transform/chunk_refiner.py"
    - "tests/unit/test_document_chunker.py"
    - "tests/unit/test_document_chunker_contract_extra.py"
    - "tests/unit/test_chunk_refiner.py"
    - "tests/integration/test_chunk_refiner_llm.py"
  failures: []

- phase: C6-review-1
  date: 2026-05-25
  status: FAIL
  summary: MetadataEnricher works functionally, but trace fallback_count has a reproducible counting bug
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_metadata_enricher_contract.py"
    - "python repro for fallback_count with forced _rule_based_metadata error"
  result: "unit: 9 passed; logic repro: fallback_count expected 1 but got 2"
  files:
    - "src/ingestion/transform/metadata_enricher.py"
    - "tests/unit/test_metadata_enricher_contract.py"
    - "config/settings.yaml"
  failures:
    - test: "fallback_count_repro_single_chunk"
      error: "trace payload fallback_count == 2"
      cause: "fallback_count incremented in except, then incremented again when metadata_fallback_reason exists"
      locations:
        - "src/ingestion/transform/metadata_enricher.py:64"
        - "src/ingestion/transform/metadata_enricher.py:80"

- phase: C6-retest-1
  date: 2026-05-25
  status: PASS
  summary: C6 fallback_count 统计重复累加问题已修复，单测与复现实验通过
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_metadata_enricher_contract.py"
    - "python repro for fallback_count with forced _rule_based_metadata error"
  result: "unit: 10 passed; logic repro: fallback_count == 1"
  files:
    - "src/ingestion/transform/metadata_enricher.py"
    - "tests/unit/test_metadata_enricher_contract.py"
    - "config/settings.yaml"
    - "src/ingestion/transform/__init__.py"
  failures: []

- phase: C7-review-1
  date: 2026-05-25
  status: PASS
  summary: ImageCaptioner implementation and fallback behavior verified
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_image_captioner_fallback.py"
  result: "unit: 6 passed"
  files:
    - "src/ingestion/transform/image_captioner.py"
    - "src/ingestion/transform/__init__.py"
    - "config/settings.yaml"
    - "config/prompts/image_captioning.txt"
    - "tests/unit/test_image_captioner_fallback.py"
  failures: []

- phase: C8-review-1
  date: 2026-05-26
  status: PASS
  summary: DenseEncoder implementation verified (batch embedding, ChunkRecord output, settings batch_size, trace metrics)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dense_encoder.py"
  result: "unit: 7 passed"
  files:
    - "src/ingestion/embedding/dense_encoder.py"
    - "src/ingestion/embedding/__init__.py"
    - "config/settings.yaml"
    - "tests/unit/test_dense_encoder.py"
  failures: []

- phase: C9-review-1
  date: 2026-05-26
  status: PASS
  summary: SparseEncoder implementation verified (BM25-style term weighting, stopword filtering, config override, trace metrics)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_sparse_encoder.py"
  result: "unit: 7 passed"
  files:
    - "src/ingestion/embedding/sparse_encoder.py"
    - "src/ingestion/embedding/__init__.py"
    - "config/settings.yaml"
    - "tests/unit/test_sparse_encoder.py"
  failures: []

- phase: C8-C9-recheck-1
  date: 2026-05-26
  status: FAIL
  summary: Added extra adversarial tests; found DenseEncoder dimension-consistency contract gap
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dense_encoder.py tests/unit/test_sparse_encoder.py tests/unit/test_dense_sparse_encoder_contract_extra.py"
  result: "1 failed, 16 passed"
  files:
    - "src/ingestion/embedding/dense_encoder.py"
    - "src/ingestion/embedding/sparse_encoder.py"
    - "tests/unit/test_dense_sparse_encoder_contract_extra.py"
  failures:
    - test: "test_dense_encoder_rejects_inconsistent_vector_dimensions"
      error: "Failed: DID NOT RAISE <class 'ValueError'>"
      cause: "DenseEncoder accepts mixed-length vectors and forwards them into ChunkRecord without dimension-consistency validation"
      locations:
        - "src/ingestion/embedding/dense_encoder.py:53"

- phase: C8-C10-recheck-1
  date: 2026-05-26
  status: FAIL
  summary: C8 fix verified; C10 has eager-initialization bug when a path is disabled
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dense_encoder.py tests/unit/test_sparse_encoder.py tests/unit/test_dense_sparse_encoder_contract_extra.py tests/unit/test_batch_processor.py"
  result: "1 failed, 25 passed"
  files:
    - "src/ingestion/embedding/dense_encoder.py"
    - "src/ingestion/embedding/batch_processor.py"
    - "tests/unit/test_dense_sparse_encoder_contract_extra.py"
    - "tests/unit/test_batch_processor.py"
  failures:
    - test: "test_init_does_not_require_dense_encoder_when_dense_disabled"
      error: "ValueError: Missing required setting: embedding"
      cause: "BatchProcessor.__init__ always initializes DenseEncoder even when enable_dense=False"
      locations:
        - "src/ingestion/embedding/batch_processor.py:35"

- phase: C10-retest-1
  date: 2026-05-26
  status: PASS
  summary: C10 eager-initialization bug fixed; added extra init/config edge-case tests and verified full C8/C9/C10 suite
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dense_encoder.py tests/unit/test_sparse_encoder.py tests/unit/test_dense_sparse_encoder_contract_extra.py tests/unit/test_batch_processor.py tests/unit/test_batch_processor_contract_extra.py"
  result: "28 passed"
  files:
    - "src/ingestion/embedding/batch_processor.py"
    - "src/ingestion/embedding/dense_encoder.py"
    - "src/ingestion/embedding/sparse_encoder.py"
    - "tests/unit/test_batch_processor.py"
    - "tests/unit/test_batch_processor_contract_extra.py"
    - "tests/unit/test_dense_sparse_encoder_contract_extra.py"
  failures: []

- phase: C11-review-1
  date: 2026-05-26
  status: PASS
  summary: BM25Indexer logic verified with roundtrip and additional contract tests (upsert overwrite, remove persistence, tie ordering, config index_dir, invalid payload)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_bm25_indexer_roundtrip.py tests/unit/test_bm25_indexer_contract_extra.py"
  result: "9 passed"
  files:
    - "src/ingestion/storage/bm25_indexer.py"
    - "src/ingestion/storage/__init__.py"
    - "config/settings.yaml"
    - "tests/unit/test_bm25_indexer_roundtrip.py"
    - "tests/unit/test_bm25_indexer_contract_extra.py"
  failures: []

- phase: C12-review-1
  date: 2026-05-26
  status: PASS
  summary: VectorUpserter idempotency and upsert-contract behavior verified; added extra order/trace contract tests
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_vector_upserter_idempotency.py tests/unit/test_vector_upserter_contract_extra.py"
  result: "7 passed"
  files:
    - "src/ingestion/storage/vector_upserter.py"
    - "src/ingestion/storage/__init__.py"
    - "tests/unit/test_vector_upserter_idempotency.py"
    - "tests/unit/test_vector_upserter_contract_extra.py"
  failures: []

- phase: C13-review-1
  date: 2026-05-26
  status: FAIL
  summary: ImageStorage main tests pass, but extra contract tests found 2 logic gaps (negative page_num accepted; stale file leak on image_id path migration)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_image_storage.py tests/unit/test_image_storage_contract_extra.py"
  result: "2 failed, 6 passed"
  files:
    - "src/ingestion/storage/image_storage.py"
    - "tests/unit/test_image_storage.py"
    - "tests/unit/test_image_storage_contract_extra.py"
  failures:
    - test: "test_save_image_rejects_negative_page_num"
      error: "Failed: DID NOT RAISE <class 'ValueError'>"
      cause: "save_image validates page_num type but not non-negative range"
      locations:
        - "src/ingestion/storage/image_storage.py:46"
    - test: "test_upsert_existing_image_id_removes_old_file_when_path_changes"
      error: "AssertionError: old file still exists"
      cause: "upsert on same image_id updates DB path but does not delete previous on-disk file when collection/suffix changes"
      locations:
        - "src/ingestion/storage/image_storage.py:58"

- phase: C13-retest-1
  date: 2026-05-26
  status: PASS
  summary: C13 fixes verified; added stricter page_num/type and same-path overwrite safety tests
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_image_storage.py tests/unit/test_image_storage_contract_extra.py"
  result: "10 passed"
  files:
    - "src/ingestion/storage/image_storage.py"
    - "tests/unit/test_image_storage.py"
    - "tests/unit/test_image_storage_contract_extra.py"
  failures: []

- phase: C14-recheck-1
  date: 2026-05-26
  status: PASS
  summary: IngestionPipeline logic rechecked with additional force-skip and missing-image non-blocking scenarios
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_ingestion_pipeline.py"
  result: "5 passed"
  files:
    - "src/ingestion/pipeline.py"
    - "tests/integration/test_ingestion_pipeline.py"
  failures: []

- phase: C15-review-1
  date: 2026-05-26
  status: PASS
  summary: ingest CLI verified with success/skip/force/config-error/stage-error flows; added E2E edge-case coverage
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/e2e/test_data_ingestion.py"
  result: "5 passed"
  files:
    - "scripts/ingest.py"
    - "tests/e2e/test_data_ingestion.py"
  failures: []

- phase: D1-review-1
  date: 2026-05-26
  status: FAIL
  summary: QueryProcessor base tests pass, but extra contract tests found filter-pattern false-positive parsing bug
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py"
  result: "1 failed, 7 passed"
  files:
    - "src/core/query_engine/query_processor.py"
    - "tests/unit/test_query_processor.py"
    - "tests/unit/test_query_processor_contract_extra.py"
  failures:
    - test: "test_filter_prefix_inside_word_must_not_be_parsed_as_filter"
      error: "AssertionError: 'collection' unexpectedly present in filters"
      cause: "_FILTER_PATTERN lacks boundary guard and matches 'collection:...' inside larger token (e.g., mycollection:kb)"
      locations:
        - "src/core/query_engine/query_processor.py:11"
        - "src/core/query_engine/query_processor.py:99"

- phase: D1-retest-1
  date: 2026-05-26
  status: PASS
  summary: QueryProcessor filter-boundary bug fixed; base + extra contract tests all pass
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py"
  result: "8 passed"
  files:
    - "src/core/query_engine/query_processor.py"
    - "tests/unit/test_query_processor.py"
    - "tests/unit/test_query_processor_contract_extra.py"
  failures: []

- phase: D2-review-1
  date: 2026-05-26
  status: PASS
  summary: DenseRetriever logic verified with added contract tests for vector_store output/item type and invalid score handling
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py"
  result: "8 passed"
  files:
    - "src/core/query_engine/dense_retriever.py"
    - "src/core/types.py"
    - "tests/unit/test_dense_retriever.py"
    - "tests/unit/test_dense_retriever_contract_extra.py"
  failures: []

- phase: D3-review-1
  date: 2026-05-26
  status: PASS
  summary: SparseRetriever logic verified with extra contract tests for bm25/get_by_ids output validation paths
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py"
  result: "9 passed"
  files:
    - "src/core/query_engine/sparse_retriever.py"
    - "tests/unit/test_sparse_retriever.py"
    - "tests/unit/test_sparse_retriever_contract_extra.py"
  failures: []

- phase: D4-review-1
  date: 2026-05-26
  status: PASS
  summary: Fusion (RRF) logic verified with additional contract coverage for trace payload, config precedence, init validation, and metadata copy isolation
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py"
  result: "10 passed"
  files:
    - "src/core/query_engine/fusion.py"
    - "tests/unit/test_fusion_rrf.py"
    - "tests/unit/test_fusion_rrf_contract_extra.py"
  failures: []

- phase: D5-review-1
  date: 2026-05-26
  status: FAIL
  summary: HybridSearch orchestration has pre-filter top_k truncation bug; valid filtered hits can be dropped before metadata filtering
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py"
  result: "1 failed, 7 passed"
  files:
    - "src/core/query_engine/hybrid_search.py"
    - "tests/integration/test_hybrid_search.py"
    - "tests/integration/test_hybrid_search_contract_extra.py"
  failures:
    - test: "test_hybrid_search_applies_filters_before_final_top_k_trim"
      error: "AssertionError: expected ['a','c'] but got ['a']"
      cause: "HybridSearch.search passes top_k into fusion before metadata post-filtering, so candidates outside fused top_k are discarded early"
      locations:
        - "src/core/query_engine/hybrid_search.py:75"
        - "src/core/query_engine/hybrid_search.py:80"
        - "src/core/query_engine/hybrid_search.py:116"

- phase: D5-retest-1
  date: 2026-05-26
  status: PASS
  summary: D5 fix verified; HybridSearch now avoids pre-filter top_k truncation loss and passes extended contract coverage
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py"
  result: "8 passed (D5 suite); 43 passed (D1-D5 regression)"
  files:
    - "src/core/query_engine/hybrid_search.py"
    - "tests/integration/test_hybrid_search.py"
    - "tests/integration/test_hybrid_search_contract_extra.py"
  failures: []

- phase: D6-review-1
  date: 2026-05-26
  status: PASS
  summary: Core Reranker orchestration verified with extra contract tests for malformed backend outputs, unmatched/duplicate ids, and field coalescing fallback
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py"
  result: "9 passed (D6 suite); 52 passed (D1-D6 regression)"
  files:
    - "src/core/query_engine/reranker.py"
    - "tests/unit/test_reranker_fallback.py"
    - "tests/unit/test_reranker_fallback_contract_extra.py"
  failures: []

- phase: D7-review-1
  date: 2026-05-26
  status: PASS
  summary: Query CLI verified with extra contract tests for top_k guard, blank collection normalization, empty-result output, and final top_k trimming
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/e2e/test_query_cli.py tests/e2e/test_query_cli_contract_extra.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/e2e/test_query_cli_contract_extra.py"
  result: "9 passed (D7 suite); 61 passed (D1-D7 regression)"
  files:
    - "scripts/query.py"
    - "tests/e2e/test_query_cli.py"
    - "tests/e2e/test_query_cli_contract_extra.py"
  failures: []

- phase: E1-E6-review-1
  date: 2026-05-26
  status: PASS
  summary: E-stage core/server/tools/response path verified; added MCP-level image return integration for tools/call -> query_knowledge_hub (E6 acceptance)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/e2e/test_query_cli_contract_extra.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py"
  result: "16 passed (E suite); 77 passed (D+E regression)"
  files:
    - "src/mcp_server/server.py"
    - "src/mcp_server/protocol_handler.py"
    - "src/mcp_server/tools/query_knowledge_hub.py"
    - "src/core/response/multimodal_assembler.py"
    - "tests/integration/test_mcp_query_image_content.py"
  failures: []

- phase: E6-retest-1
  date: 2026-05-28
  status: PASS
  summary: E6 multimodal image return re-verified with additional edge tests (missing image path skip, unknown suffix mime fallback) and MCP-level tools/call integration
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_multimodal_assembler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_query_knowledge_hub_tool.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py"
  result: "8 passed (E6-focused); 19 passed (E-suite subset)"
  files:
    - "src/core/response/multimodal_assembler.py"
    - "src/mcp_server/tools/query_knowledge_hub.py"
    - "tests/unit/test_multimodal_assembler.py"
    - "tests/integration/test_mcp_query_image_content.py"
  failures: []

- phase: F1-review-1
  date: 2026-05-28
  status: PASS
  summary: TraceContext lifecycle and collector contract re-verified with extra edge coverage for trace_id validation, blank stage_name validation, and collector clear behavior
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_trace_context.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/e2e/test_query_cli_contract_extra.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py"
  result: "14 passed (F1 suite); 94 passed (D+E+F regression subset)"
  files:
    - "src/core/trace/trace_context.py"
    - "src/core/trace/trace_collector.py"
    - "tests/unit/test_trace_context.py"
  failures: []

- phase: F2-review-1
  date: 2026-06-01
  status: PASS
  summary: JSONL logger and TraceCollector persistence verified; added edge tests for multi-line append and invalid log path type
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_jsonl_logger.py tests/unit/test_trace_context.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_query_processor.py tests/unit/test_query_processor_contract_extra.py tests/unit/test_dense_retriever.py tests/unit/test_dense_retriever_contract_extra.py tests/unit/test_sparse_retriever.py tests/unit/test_sparse_retriever_contract_extra.py tests/unit/test_fusion_rrf.py tests/unit/test_fusion_rrf_contract_extra.py tests/integration/test_hybrid_search.py tests/integration/test_hybrid_search_contract_extra.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/e2e/test_query_cli_contract_extra.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py"
  result: "20 passed (F2 suite); 100 passed (D+E+F regression subset)"
  files:
    - "src/observability/logger.py"
    - "src/core/trace/trace_collector.py"
    - "tests/unit/test_jsonl_logger.py"
    - "tests/unit/test_trace_context.py"
  failures: []

- phase: F3-review-1
  date: 2026-06-01
  status: PASS
  summary: Query-chain tracing verified end-to-end; added backward-compatibility coverage for legacy QueryProcessor without trace kwarg
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py"
  result: "26 passed (F3-focused suite); 65 passed (query+mcp+trace regression subset)"
  files:
    - "src/core/query_engine/query_processor.py"
    - "src/core/query_engine/hybrid_search.py"
    - "tests/integration/test_hybrid_search.py"
    - "tests/unit/test_query_processor.py"
  failures: []

- phase: F4-review-1
  date: 2026-06-01
  status: PASS
  summary: Ingestion-chain trace logging verified with stricter stage payload assertions (source_path/collection/document_id and count fields) in addition to stage presence
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_ingestion_pipeline.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/integration/test_ingestion_pipeline.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py"
  result: "27 passed (F4+trace suite); 53 passed (query+ingestion+trace regression subset)"
  files:
    - "src/ingestion/pipeline.py"
    - "tests/integration/test_ingestion_pipeline.py"
    - "tests/unit/test_trace_context.py"
    - "tests/unit/test_jsonl_logger.py"
  failures: []

- phase: F5-review-1
  date: 2026-06-01
  status: PASS
  summary: Progress callback contract verified with additional force=true anti-short-circuit case; F-series end-to-end behavior remains stable
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_pipeline_progress.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py"
  result: "36 passed (F5+ingestion+trace suite); 81 passed (F-series + query/mcp regression subset)"
  files:
    - "src/ingestion/pipeline.py"
    - "tests/unit/test_pipeline_progress.py"
    - "tests/integration/test_ingestion_pipeline.py"
    - "tests/e2e/test_data_ingestion.py"
  failures: []

- phase: G1-review-1
  date: 2026-06-01
  status: PASS
  summary: Dashboard foundation verified; added robustness coverage for config-service JSON/traces edge cases and start_dashboard command/exception paths
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py"
  result: "6 passed (G1 suite); 87 passed (F-series + query/mcp/ingestion regression subset)"
  files:
    - "src/observability/dashboard/app.py"
    - "src/observability/dashboard/pages/overview.py"
    - "src/observability/dashboard/services/config_service.py"
    - "scripts/start_dashboard.py"
    - "tests/unit/test_dashboard_config_service.py"
    - "tests/unit/test_start_dashboard_script.py"
  failures: []

- phase: G2-review-1
  date: 2026-06-01
  status: PASS
  summary: DocumentManager cross-storage lifecycle verified with extra negative coverage for unknown doc_id and no-op delete path
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_document_manager.py tests/unit/test_vector_store_contract.py tests/unit/test_bm25_indexer_roundtrip.py tests/unit/test_image_storage.py tests/unit/test_file_integrity.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py tests/unit/test_document_manager.py"
  result: "34 passed (G2+storage suite); 93 passed (query/mcp/ingestion/dashboard regression subset)"
  files:
    - "src/ingestion/document_manager.py"
    - "src/libs/vector_store/chroma_store.py"
    - "src/libs/loader/file_integrity.py"
    - "tests/unit/test_document_manager.py"
  failures: []

- phase: G4-review-1
  date: 2026-06-01
  status: FAIL
  summary: G4 page implementation is still placeholder; required upload/trigger/progress controls are missing in ingestion_manager page
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_ingestion_manager.py tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py"
  result: "1 failed, 8 passed"
  files:
    - "src/observability/dashboard/pages/ingestion_manager.py"
    - "tests/unit/test_dashboard_ingestion_manager.py"
  failures:
    - test: "test_ingestion_manager_exposes_g4_operational_controls"
      error: "AssertionError: 'file_uploader' not in calls (only title/info called)"
      cause: "ingestion_manager.render currently only renders placeholder info and does not expose G4 operational widgets"
      locations:
        - "src/observability/dashboard/pages/ingestion_manager.py:1"
        - "tests/unit/test_dashboard_ingestion_manager.py:50"

- phase: G3-review-1
  date: 2026-06-01
  status: PASS
  summary: Data Browser service verified with additional coverage for collection list dedupe/sort and collection filter forwarding; existing detail/timestamp/error paths remain valid
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py tests/unit/test_dashboard_data_service.py tests/unit/test_document_manager.py"
  result: "10 passed (G3 dashboard suite); 97 passed (query/mcp/ingestion/dashboard regression subset)"
  files:
    - "src/observability/dashboard/pages/data_browser.py"
    - "src/observability/dashboard/services/data_service.py"
    - "tests/unit/test_dashboard_data_service.py"
  failures: []

- phase: G4-review-2
  date: 2026-06-01
  status: PASS
  summary: Ingestion Manager page verified with workflow-level tests for ingestion trigger (pipeline.run + progress callback) and delete action wiring (DocumentManager.delete_document + rerun)
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_ingestion_manager.py tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py tests/unit/test_dashboard_data_service.py tests/unit/test_document_manager.py tests/unit/test_dashboard_ingestion_manager.py"
  result: "13 passed (G4 dashboard suite); 100 passed (query/mcp/ingestion/dashboard regression subset)"
  files:
    - "src/observability/dashboard/pages/ingestion_manager.py"
    - "tests/unit/test_dashboard_ingestion_manager.py"
    - "tests/unit/test_dashboard_data_service.py"
  failures: []

- phase: G5-review-1
  date: 2026-06-01
  status: PASS
  summary: Ingestion traces page and trace service verified with additional limit-validation and settings-error UI-path coverage
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_trace_service.py tests/unit/test_dashboard_ingestion_traces.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_ingestion_manager.py tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py tests/unit/test_trace_service.py tests/unit/test_dashboard_ingestion_traces.py tests/integration/test_hybrid_search.py tests/unit/test_query_processor.py tests/unit/test_reranker_fallback.py tests/unit/test_reranker_fallback_contract_extra.py tests/e2e/test_query_cli.py tests/unit/test_protocol_handler.py tests/integration/test_mcp_server.py tests/integration/test_mcp_query_image_content.py tests/unit/test_response_builder.py tests/unit/test_list_collections.py tests/unit/test_get_document_summary.py tests/unit/test_query_knowledge_hub_tool.py tests/unit/test_multimodal_assembler.py tests/unit/test_trace_context.py tests/unit/test_jsonl_logger.py tests/integration/test_ingestion_pipeline.py tests/e2e/test_data_ingestion.py tests/unit/test_pipeline_progress.py tests/unit/test_document_manager.py"
  result: "7 passed (G5 suite); 107 passed (query/mcp/ingestion/dashboard regression subset)"
  files:
    - "src/observability/dashboard/services/trace_service.py"
    - "src/observability/dashboard/pages/ingestion_traces.py"
    - "tests/unit/test_trace_service.py"
    - "tests/unit/test_dashboard_ingestion_traces.py"
  failures: []
- phase: G6-review-1
  date: 2026-06-01
  status: FAIL
  summary: Query Traces page has selection mismatch when dropdown labels are duplicated; newly added counterexample test fails and confirms wrong trace payload is shown
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_trace_service.py tests/unit/test_dashboard_query_traces.py"
  result: "1 failed, 8 passed"
  files:
    - "src/observability/dashboard/pages/query_traces.py"
    - "tests/unit/test_dashboard_query_traces.py"
    - "tests/unit/test_trace_service.py"
  failures:
    - test: "test_query_traces_page_selectbox_duplicate_labels_should_map_correct_trace"
      error: "AssertionError: expected selected payload trace_id 'abcdefgh-2', got 'abcdefgh-1'"
      cause: "render() maps selected option back via labels.index(selected_label), which returns the first index for duplicate labels"
      locations:
        - "src/observability/dashboard/pages/query_traces.py:52"
        - "tests/unit/test_dashboard_query_traces.py:166"
- phase: G6-review-2
  date: 2026-06-01
  status: PASS
  summary: Query Traces duplicate-label selection issue fixed by using full trace_id in labels; query trace page and trace service checks passed with added counterexample coverage
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_trace_service.py tests/unit/test_dashboard_query_traces.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_config_service.py tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_ingestion_manager.py tests/unit/test_dashboard_ingestion_traces.py tests/unit/test_trace_service.py tests/unit/test_dashboard_query_traces.py tests/unit/test_start_dashboard_script.py"
  result: "9 passed (G6 suite); 25 passed (dashboard regression subset)"
  files:
    - "src/observability/dashboard/pages/query_traces.py"
    - "src/observability/dashboard/services/trace_service.py"
    - "tests/unit/test_dashboard_query_traces.py"
    - "tests/unit/test_trace_service.py"
  failures: []

- phase: G7-review-1
  date: 2026-06-02
  status: PASS
  summary: Dashboard bilingual wiring verified across app/page translations with added coverage for zh-CN page labels and missing-locale-key fallback to en-US
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_dashboard_i18n.py tests/unit/test_dashboard_query_traces.py tests/unit/test_dashboard_ingestion_traces.py tests/unit/test_dashboard_ingestion_manager.py tests/unit/test_dashboard_data_service.py tests/unit/test_dashboard_config_service.py tests/unit/test_start_dashboard_script.py tests/unit/test_trace_service.py"
  result: "29 passed (G7 + dashboard regression subset)"
  files:
    - "src/observability/dashboard/app.py"
    - "src/observability/dashboard/services/i18n.py"
    - "src/observability/dashboard/pages/overview.py"
    - "src/observability/dashboard/pages/data_browser.py"
    - "src/observability/dashboard/pages/ingestion_manager.py"
    - "src/observability/dashboard/pages/ingestion_traces.py"
    - "src/observability/dashboard/pages/query_traces.py"
    - "src/observability/dashboard/pages/evaluation_panel.py"
    - "tests/unit/test_dashboard_i18n.py"
    - "tests/unit/test_dashboard_query_traces.py"
  failures: []

- phase: H1-review-1
  date: 2026-06-02
  status: PASS
  summary: RagasEvaluator implementation verified with additional counterexample coverage for non-numeric metric coercion and non-mapping trace.to_dict fallback; factory registration and config-loading regression remained stable
  commands:
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_ragas_evaluator.py tests/unit/test_custom_evaluator.py"
    - ".\\.venv\\Scripts\\python -m pytest -q tests/unit/test_ragas_evaluator.py tests/unit/test_custom_evaluator.py tests/unit/test_config_loading.py tests/unit/test_dashboard_config_service.py"
  result: "17 passed (H1 suite); 23 passed (evaluation/config regression subset)"
  files:
    - "src/libs/evaluator/ragas_evaluator.py"
    - "src/libs/evaluator/evaluator_factory.py"
    - "src/observability/evaluation/ragas_evaluator.py"
    - "tests/unit/test_ragas_evaluator.py"
  failures: []
