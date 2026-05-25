# Test Review Progress (Agent-Friendly)

## 规则
- 固定记录文件：`TEST_REVIEW_PROGRESS.md`
- 记录格式：列表（每个阶段一条），并带结构化字段
- 状态枚举：`PASS` | `FAIL` | `PENDING`

## 阶段状态列表
- phase: C1
  date: 2026-05-25
  status: PASS
  summary: 核心数据类型契约检查通过
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
  summary: SHA256 与 SQLite 去重契约检查通过（含扩展边界测试）
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
  summary: Loader 抽象与 PDF Loader 存在 2 处确定性问题
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
      cause: "text_extractor 非字符串输出被静默转换为字符串，未 fail-fast"
      locations:
        - "src/libs/loader/pdf_loader.py:54"
    - test: "test_pdf_loader_ignores_invalid_image_items_without_crashing"
      error: "ValueError: metadata.images[1].id must be a non-empty string"
      cause: "图片提取结果未在 Loader 侧过滤最小必填字段，坏记录进入 Document 校验后导致 load 失败"
      locations:
        - "src/libs/loader/pdf_loader.py:72"
        - "src/core/types.py:67"

- phase: C3-retest-1
  date: 2026-05-25
  status: PASS
  summary: C3 修复后复测通过，覆盖更多边界与异常路径
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
  summary: C4 ��ǰδʵ�֣���Ϊռλ�ļ�����ȱ�ٶ�Ӧ����
  commands:
    - "Get-Content src/ingestion/chunking/document_chunker.py"
    - "rg --files tests | rg \"chunker|chunking|document_chunker\""
  result: "document_chunker.py ��ռλ�ĵ��ַ�����δ���� C4 ��ز���"
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
  summary: C5 ChunkRefiner �����߼��뵥��ͨ�������ɲ���ȱ�� OPENAI_API_KEY ����
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
  summary: C4 �� C5 ͳһ�ع����ͨ����C5 ʵ�� LLM ���ɲ��԰�Ԥ������
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
