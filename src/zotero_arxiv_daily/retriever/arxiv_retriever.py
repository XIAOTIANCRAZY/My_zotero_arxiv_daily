from .base import BaseRetriever, register_retriever
import arxiv
from arxiv import Result as ArxivResult
from ..protocol import Paper
from ..utils import get_target_date
import feedparser
from tqdm import tqdm
from loguru import logger


@register_retriever("arxiv")
class ArxivRetriever(BaseRetriever):
    def __init__(self, config):
        super().__init__(config)
        if self.config.source.arxiv.category is None:
            raise ValueError("category must be specified for arxiv.")

    def _retrieve_raw_papers(self) -> list[ArxivResult]:
        client = arxiv.Client(num_retries=10, delay_seconds=10)
        target_date = get_target_date(self.config)
        if target_date is not None:
            return self._retrieve_raw_papers_by_date(client, target_date)
        return self._retrieve_latest_raw_papers(client)

    def _retrieve_latest_raw_papers(self, client: arxiv.Client) -> list[ArxivResult]:
        query = "+".join(self.config.source.arxiv.category)
        include_cross_list = self.config.source.arxiv.get("include_cross_list", False)

        feed = feedparser.parse(f"https://rss.arxiv.org/atom/{query}")
        if "Feed error for query" in feed.feed.title:
            raise Exception(f"Invalid ARXIV_QUERY: {query}.")

        allowed_announce_types = {"new", "cross"} if include_cross_list else {"new"}
        all_paper_ids = [
            entry.id.removeprefix("oai:arXiv.org:")
            for entry in feed.entries
            if entry.get("arxiv_announce_type", "new") in allowed_announce_types
        ]
        if self.config.executor.debug:
            all_paper_ids = all_paper_ids[:10]

        raw_papers = []
        bar = tqdm(total=len(all_paper_ids))
        for i in range(0, len(all_paper_ids), 20):
            search = arxiv.Search(id_list=all_paper_ids[i:i + 20])
            batch = list(client.results(search))
            bar.update(len(batch))
            raw_papers.extend(batch)
        bar.close()
        return raw_papers

    def _retrieve_raw_papers_by_date(self, client: arxiv.Client, target_date) -> list[ArxivResult]:
        include_cross_list = self.config.source.arxiv.get("include_cross_list", False)
        categories = set(self.config.source.arxiv.category)
        search = arxiv.Search(
            query=" OR ".join(f"cat:{category}" for category in categories),
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        logger.info(f"Retrieving arXiv papers for target date {target_date.isoformat()}")
        raw_papers = []
        seen_ids = set()
        for paper in client.results(search):
            published_date = paper.published.date()
            if published_date < target_date:
                break
            if published_date > target_date:
                continue
            if not self._match_categories(paper, categories, include_cross_list):
                continue
            if paper.entry_id in seen_ids:
                continue

            seen_ids.add(paper.entry_id)
            raw_papers.append(paper)
            if self.config.executor.debug and len(raw_papers) >= 10:
                break
        return raw_papers

    def _match_categories(self, paper: ArxivResult, categories: set[str], include_cross_list: bool) -> bool:
        if include_cross_list:
            paper_categories = set(getattr(paper, "categories", []))
            primary_category = getattr(paper, "primary_category", None)
            if primary_category is not None:
                paper_categories.add(primary_category)
            return bool(paper_categories & categories)
        return getattr(paper, "primary_category", None) in categories

    def convert_to_paper(self, raw_paper: ArxivResult) -> Paper:
        return Paper(
            source=self.name,
            title=raw_paper.title,
            authors=[author.name for author in raw_paper.authors],
            abstract=raw_paper.summary,
            url=raw_paper.entry_id,
            pdf_url=raw_paper.pdf_url,
            full_text=None,
        )
