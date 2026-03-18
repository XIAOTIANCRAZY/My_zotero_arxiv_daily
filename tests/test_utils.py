from copy import deepcopy

from zotero_arxiv_daily.utils import build_email_subject, get_target_date


def test_get_target_date(config):
    config = deepcopy(config)
    config.executor.target_date = "2026-03-16"

    assert get_target_date(config).isoformat() == "2026-03-16"


def test_get_target_date_accepts_empty_string(config):
    config = deepcopy(config)
    config.executor.target_date = ""

    assert get_target_date(config) is None


def test_build_email_subject_uses_target_date(config):
    config = deepcopy(config)
    config.executor.target_date = "2026-03-16"

    assert build_email_subject(config) == "Daily arXiv 2026/03/16"
