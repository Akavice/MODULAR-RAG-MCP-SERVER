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
