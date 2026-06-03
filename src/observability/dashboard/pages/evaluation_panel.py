"""Dashboard evaluation panel page."""

from __future__ import annotations

from typing import Any

from core.query_engine.hybrid_search import HybridSearch
from core.settings import load_settings
from libs.evaluator.evaluator_factory import EvaluatorFactory
from observability.dashboard.services.i18n import locale_from_context, t
from observability.evaluation.eval_runner import EvalRunner


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("evaluation_panel.title", locale=locale))
    st.caption(t("evaluation_panel.caption", locale=locale))

    settings_path = _resolve_settings_path(context)
    backend = _call_st(
        st,
        "selectbox",
        t("evaluation_panel.backend", locale=locale),
        ["custom", "ragas"],
        index=0,
    )
    test_set_path = _call_st(
        st,
        "text_input",
        t("evaluation_panel.test_set", locale=locale),
        value="tests/fixtures/golden_test_set.json",
    )
    top_k = _call_st(
        st,
        "number_input",
        t("evaluation_panel.top_k", locale=locale),
        min_value=1,
        value=5,
        step=1,
    )
    dry_run = _call_st(
        st,
        "checkbox",
        t("evaluation_panel.dry_run", locale=locale),
        value=True,
        help=t("evaluation_panel.dry_run_help", locale=locale),
    )

    if not st.button(t("evaluation_panel.run", locale=locale), type="primary"):
        return

    try:
        report = _run_evaluation(
            settings_path=settings_path,
            backend=str(backend or "custom"),
            test_set_path=str(test_set_path or "tests/fixtures/golden_test_set.json"),
            top_k=int(top_k) if isinstance(top_k, int) else 5,
            dry_run=bool(dry_run),
        )
    except Exception as exc:
        _notify(st, "error", t("evaluation_panel.error", locale=locale, error=exc))
        return

    _notify(st, "success", t("evaluation_panel.success", locale=locale, cases=len(report.cases)))
    st.subheader(t("evaluation_panel.metrics", locale=locale))
    metric_items = list(report.metrics.items())
    if metric_items:
        columns = st.columns(min(4, len(metric_items)))
        for index, (name, value) in enumerate(metric_items):
            columns[index % len(columns)].metric(name, _format_metric(value))

    st.subheader(t("evaluation_panel.case_details", locale=locale))
    st.dataframe(
        [
            {
                t("evaluation_panel.table.query", locale=locale): item.query,
                t("evaluation_panel.table.expected", locale=locale): ", ".join(
                    item.expected_chunk_ids or item.expected_sources
                ),
                t("evaluation_panel.table.retrieved", locale=locale): ", ".join(item.retrieved_ids),
                t("evaluation_panel.table.hit_rate", locale=locale): item.metrics.get("hit_rate", 0.0),
                t("evaluation_panel.table.mrr", locale=locale): item.metrics.get("mrr", 0.0),
            }
            for item in report.cases
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.json(report.to_dict())


def _run_evaluation(
    *,
    settings_path: str,
    backend: str,
    test_set_path: str,
    top_k: int,
    dry_run: bool,
) -> Any:
    settings = load_settings(settings_path)
    evaluation_settings = dict(settings.evaluation)
    evaluation_settings["provider"] = backend.strip() or "custom"
    evaluator = EvaluatorFactory.create(evaluation_settings)
    hybrid_search = _DryRunHybridSearch() if dry_run else HybridSearch(settings)
    return EvalRunner(
        settings=settings,
        hybrid_search=hybrid_search,
        evaluator=evaluator,
        top_k=top_k,
    ).run(test_set_path)


class _DryRunHybridSearch:
    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[Any]:
        _ = query, top_k, filters
        return []


def _resolve_settings_path(context: dict[str, Any] | None) -> str:
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "config/settings.yaml"


def _format_metric(value: float) -> str:
    return f"{value:.3f}"


def _notify(st: Any, level: str, message: str) -> None:
    fn = getattr(st, level, None)
    if callable(fn):
        fn(message)
        return
    fallback = getattr(st, "info", None)
    if callable(fallback):
        fallback(message)


def _call_st(st: Any, method: str, *args: Any, **kwargs: Any) -> Any:
    fn = getattr(st, method, None)
    if callable(fn):
        return fn(*args, **kwargs)
    return None
