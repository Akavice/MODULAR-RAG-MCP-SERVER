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
