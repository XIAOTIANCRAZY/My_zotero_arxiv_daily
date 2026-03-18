from datetime import datetime
from copy import deepcopy
from types import SimpleNamespace

import feedparser

from zotero_arxiv_daily.retriever import arxiv_retriever as retriever_module
from zotero_arxiv_daily.retriever.arxiv_retriever import ArxivRetriever


def make_paper(
    paper_id: str,
    published: str,
    primary_category: str = "cs.AI",
    categories: list[str] | None = None,
):
    return SimpleNamespace(
        title=f"title-{paper_id}",
        authors=[SimpleNamespace(name="author-1"), SimpleNamespace(name="author-2")],
        summary=f"summary-{paper_id}",
        entry_id=f"https://arxiv.org/abs/{paper_id}",
        pdf_url=f"https://arxiv.org/pdf/{paper_id}",
        primary_category=primary_category,
        categories=categories or [primary_category],
        published=datetime.fromisoformat(published),
    )


def test_arxiv_retriever_uses_latest_feed_ids(config, monkeypatch):
    config = deepcopy(config)
    parsed_result = feedparser.parse("tests/retriever/arxiv_rss_example.xml")
    paper_by_id = {
        entry.id.removeprefix("oai:arXiv.org:"): make_paper(
            entry.id.removeprefix("oai:arXiv.org:"),
            "2025-08-20T00:00:00+00:00",
        )
        for entry in parsed_result.entries
        if entry.get("arxiv_announce_type", "new") == "new"
    }

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def results(self, search):
            return [paper_by_id[paper_id] for paper_id in search.id_list]

    monkeypatch.setattr(retriever_module.feedparser, "parse", lambda _: parsed_result)
    monkeypatch.setattr(retriever_module.arxiv, "Client", FakeClient)

    retriever = ArxivRetriever(config)
    papers = retriever._retrieve_raw_papers()

    assert len(papers) == len(paper_by_id)
    assert {paper.entry_id for paper in papers} == {
        f"https://arxiv.org/abs/{paper_id}" for paper_id in paper_by_id
    }


def test_arxiv_retriever_filters_target_date_and_cross_list(config, monkeypatch):
    config = deepcopy(config)
    config.executor.target_date = "2025-08-20"
    config.source.arxiv.category = ["cs.AI"]
    config.source.arxiv.include_cross_list = True

    results = [
        make_paper("2508.99999", "2025-08-21T00:00:00+00:00"),
        make_paper("2508.13434", "2025-08-20T00:00:00+00:00", "cs.AI"),
        make_paper(
            "2508.13435",
            "2025-08-20T00:00:00+00:00",
            "econ.EM",
            ["econ.EM", "cs.AI"],
        ),
        make_paper("2508.10000", "2025-08-19T00:00:00+00:00"),
    ]

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def results(self, search):
            return iter(results)

    monkeypatch.setattr(retriever_module.arxiv, "Client", FakeClient)

    retriever = ArxivRetriever(config)
    papers = retriever._retrieve_raw_papers()

    assert [paper.entry_id for paper in papers] == [
        "https://arxiv.org/abs/2508.13434",
        "https://arxiv.org/abs/2508.13435",
    ]


def test_arxiv_convert_to_paper_does_not_fetch_full_text(config):
    config = deepcopy(config)
    raw_paper = make_paper("2508.13434", "2025-08-20T00:00:00+00:00")

    retriever = ArxivRetriever(config)
    paper = retriever.convert_to_paper(raw_paper)

    assert paper.title == raw_paper.title
    assert paper.abstract == raw_paper.summary
    assert paper.pdf_url == raw_paper.pdf_url
    assert paper.full_text is None
