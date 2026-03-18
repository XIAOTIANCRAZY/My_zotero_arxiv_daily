<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="assets/logo.svg" alt="logo"></a>
</p>

<h3 align="center">Zotero-arXiv-Daily</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  ![Stars](https://img.shields.io/github/stars/TideDra/zotero-arxiv-daily?style=flat)
  [![GitHub Issues](https://img.shields.io/github/issues/TideDra/zotero-arxiv-daily)](https://github.com/TideDra/zotero-arxiv-daily/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/TideDra/zotero-arxiv-daily)](https://github.com/TideDra/zotero-arxiv-daily/pulls)
  [![License](https://img.shields.io/github/license/TideDra/zotero-arxiv-daily)](/LICENSE)
  [<img src="https://api.gitsponsors.com/api/badge/img?id=893025857" height="20">](https://api.gitsponsors.com/api/badge/link?p=PKMtRut1dWWuC1oFdJweyDSvJg454/GkdIx4IinvBblaX2AY4rQ7FYKAK1ZjApoiNhYEeduIEhfeZVIwoIVlvcwdJXVFD2nV2EE5j6lYXaT/RHrcsQbFl3aKe1F3hliP26OMayXOoZVDidl05wj+yg==)

</div>

---

<p align="center"> Recommend new arxiv papers of your interest daily according to your Zotero library.
    <br> 
</p>

> [!IMPORTANT]
> Please keep an eye on this repo, and merge your forked repo in time when there is any update of this upstream, in order to enjoy new features and fix found bugs.

## 🧐 About <a name = "about"></a>

> Track new scientific researches of your interest by just forking (and staring) this repo!😊

*Zotero-arXiv-Daily* finds arxiv papers that may attract you based on the context of your Zotero library, and then sends the result to your mailbox📮. It can be deployed as Github Action Workflow with **zero cost**, **no installation**, and **few configuration** of Github Action environment variables for daily **automatic** delivery.

## ✨ Features
- Totally free! All the calculation can be done in the Github Action runner locally within its quota (for public repo).
- AI-generated TL;DR for you to quickly pick up target papers.
- Affiliations of the paper are resolved and presented.
- Links of PDF and code implementation (if any) presented in the e-mail.
- List of papers sorted by relevance with your recent research interest.
- Fast deployment via fork this repo and set environment variables in the Github Action Page.
- Support LLM API for generating TL;DR of papers.
- Ignore unwanted Zotero papers using glob pattern.
- Support multiple sources of papers to retrieve:
  - arxiv
  - biorxiv
  - medrxiv

## 📷 Screenshot
![screenshot](./assets/screenshot.png)

## 🚀 Usage
### Quick Start
1. Fork (and star😘) this repo.
![fork](./assets/fork.png)

2. Set Github Action environment variables.
![secrets](./assets/secrets.png)

Below are all the secrets you need to set. They are invisible to anyone including you once they are set, for security.

| Key |Description | Example |
| :---  | :---  | :--- |
| ZOTERO_ID  | User ID of your Zotero account. **User ID is not your username, but a sequence of numbers**Get your ID from [here](https://www.zotero.org/settings/security). You can find it at the position shown in this [screenshot](https://github.com/TideDra/zotero-arxiv-daily/blob/main/assets/userid.png). | 12345678  |
| ZOTERO_KEY | An Zotero API key with read access. Get a key from [here](https://www.zotero.org/settings/security).  | AB5tZ877P2j7Sm2Mragq041H   |
| SENDER | The email account of the SMTP server that sends you email. | abc@qq.com |
| SENDER_PASSWORD | The password of the sender account. Note that it's not necessarily the password for logging in the e-mail client, but the authentication code for SMTP service. Ask your email provider for this.   | abcdefghijklmn |
| RECEIVER | The e-mail address that receives the paper list. | abc@outlook.com |
| OPENAI_API_KEY | API Key when using the API to access LLMs. You can get FREE API for using advanced open source LLMs in [SiliconFlow](https://cloud.siliconflow.cn/i/b3XhBRAm). | sk-xxx |
| OPENAI_API_BASE | API URL when using the API to access LLMs. | https://api.siliconflow.cn/v1 |

Then you should also set a public variable `CUSTOM_CONFIG` for your custom configuration.
![vars](./assets/repo_var.png)
![custom_config](./assets/config_var.png)
Paste the following content into the value of `CUSTOM_CONFIG` variable:
```yaml
zotero:
  user_id: ${oc.env:ZOTERO_ID}
  api_key: ${oc.env:ZOTERO_KEY}
  include_path: null

email:
  sender: ${oc.env:SENDER}
  receiver: ${oc.env:RECEIVER}
  smtp_server: smtp.qq.com
  smtp_port: 465
  sender_password: ${oc.env:SENDER_PASSWORD}

llm:
  api:
    key: ${oc.env:OPENAI_API_KEY}
    base_url: ${oc.env:OPENAI_API_BASE}
  generation_kwargs:
    model: gpt-4o-mini

source:
  arxiv:
    category: ["cs.AI","cs.CV","cs.LG","cs.CL"]
    include_cross_list: false # Set to true to include arXiv cross-list papers in these categories.

executor:
  debug: ${oc.env:DEBUG,null}
  target_date: ${oc.env:TARGET_DATE,null} # Optional. Example: 2026-03-16
  source: ['arxiv']
```
Set `source.arxiv.include_cross_list: true` if you want cross-listed papers included.
>[!NOTE]
> `${oc.env:XXX,yyy}` means the value of the environment variable `XXX`. If the variable is not set, the default value `yyy` will be used.

Here is the full configuration, `???` means the value must be filled in:
```yaml
zotero:
  user_id: ??? # User ID of your Zotero account.
  api_key: ??? # An Zotero API key with read access.
  include_path: null # A glob pattern marking the Zotero collections that should be included. Example: "2026/survey/**"

source:
  arxiv:
    category: null # The categories of target arxiv papers. Find the abbr of your research area from [here](https://arxiv.org/category_taxonomy). Example: ["cs.AI","cs.CV","cs.LG","cs.CL"]
    include_cross_list: false # Whether to include arXiv cross-list papers in subscribed categories. Example: true
  biorxiv:
    category: null # The categories of target biorxiv papers. Find categories from [here](https://www.biorxiv.org/). Example: ["biochemistry","animal behavior and cognition"]
  medrxiv:
    category: null # The categories of target medrxiv papers. Find categories from [here](https://www.medrxiv.org/) Example: ["psychiatry and clinical psychology", "neurology"]

email:
  sender: ??? # The email account of the SMTP server that sends you email. Example: abc@qq.com
  receiver: ??? # The email account that receives the paper list. Example: abc@outlook.com
  smtp_server: ??? # The SMTP server that sends the email. Ask your email provider (Gmail, QQ, Outlook, ...) for its SMTP server. Example: smtp.qq.com
  smtp_port: ??? # The port of SMTP server. Example: 465
  sender_password: ??? # The password of the sender account. Note that it's not necessarily the password for logging in the e-mail client, but the authentication code for SMTP service. Ask your email provider for this. Example: abcdefghijklmn

llm:
  api:
    key: ??? # API Key of your LLM API. Example: sk-xxx
    base_url: ??? # API URL of your LLM API. Example: https://api.openai.com/v1
  generation_kwargs:
  # Arguments for the LLM API. See [here](https://platform.openai.com/docs/api-reference/chat/create) for more details.
    max_tokens: 16384
    model: ???
  language: English # Preferred language for the TL;DR. Example: English

reranker:
  local:
    model: jinaai/jina-embeddings-v5-text-nano # The Hugging Face model name of the local embedding model. Example: jinaai/jina-embeddings-v5-text-nano
    encode_kwargs:
    # The kwargs for the encode method of the local embedding model. Details see [here](https://www.sbert.net/docs/package_reference/SentenceTransformer.html#sentence_transformers.SentenceTransformer.encode)
      task: retrieval
      prompt_name: document
  api:
    key: null # API Key of your embedding model API. Example: sk-xxx
    base_url: null # API URL of your embedding model API. Example: https://api.openai.com/v1
    model: null # The model name of the embedding model. Example: text-embedding-3-large
    batch_size: null # The batch size for embedding API requests. Adjust to match your provider's limit. Example: 64

executor:
  debug: false # Whether to use debug mode. Example: true
  send_empty: false # Whether to send an empty email even if no new papers today. Example: true
  target_date: null # Optional target paper date in YYYY-MM-DD format. Example: "2026-03-16"
  max_workers: 4 # Concurrent workers for processing papers. Example: 4
  max_paper_num: 100 # The maximum number of the papers presented in the email. Example: 100
  source: ??? # The sources of papers to retrieve. Example: ['arxiv','biorxiv','medrxiv']
  reranker: local # The reranker to use. Example: 'local' or 'api'
```

That's all! Now you can test the workflow by manually triggering it:
![test](./assets/test.png)

> [!NOTE]
> The Test-Workflow Action is the debug version of the main workflow (Send-emails-daily). You can optionally pass a `target_date` input in `YYYY-MM-DD` format, or set the `TARGET_DATE` secret, to backfill a specific day's arXiv papers. When `target_date` is empty, the workflow uses the latest daily release. There is no new arxiv paper at weekends and holiday, in which case you may see "No new papers found" in the log of main workflow.

Then check the log and the receiver email after it finishes.

By default, the main workflow runs at 02:00 UTC on Monday-Friday, which corresponds to 10:00 Beijing time and is late enough to include the full daily arXiv announcement batch. You can change this time by editting the workflow config `.github/workflows/main.yml`.

### Time and backfill notes
If you use Beijing time / 如果你使用北京时间：

- The scheduled workflow runs at 10:00 Beijing time on Monday-Friday.
  自动定时任务会在每周一到周五北京时间 10:00 运行。
- This is intentionally later than the daily arXiv announcement release window, so the workflow can retrieve the full daily batch more reliably.
  这个时间刻意晚于 arXiv 每日公告发布时间，因此更容易稳定拿到当天完整批次的论文。
- The `Test` workflow is only for debugging and may not return the full paper list.
  `Test` workflow 仅用于调试，可能不会返回完整论文列表。
- Use `Send emails daily` when you want the full scheduled behavior or a manual backfill.
  如果你希望获得完整流程结果，或者手动补发某一天的论文，请使用 `Send emails daily`。

### arXiv update schedule and your delivery time
The workflow follows the arXiv announcement cycle rather than the Beijing calendar day.
这个工作流跟随的是 arXiv 官方公告批次，而不是北京时间自然日的 00:00-24:00。

According to the arXiv announcement rules:
根据 arXiv 官方公告规则：

- arXiv accepts submissions continuously, but new papers are announced in batches.
  arXiv 可以持续接收投稿，但新论文是按批次统一公告的。
- The announcement cut-off time is 14:00 ET, and the announcement is released at 20:00 ET.
  每日公告的截稿时间是美东时间 14:00，正式公告发布时间是美东时间 20:00。
- There are no regular announcements on Friday or Saturday ET.
  美东时间周五和周六通常没有新的公告批次。

For Beijing time users, 20:00 ET is usually 08:00 or 09:00 the next morning in Beijing, depending on daylight saving time.
对北京时间用户来说，美东时间 20:00 通常对应北京时间次日 08:00 或 09:00，具体取决于美国夏令时。

This repository is configured to run at 10:00 Beijing time on Monday-Friday, so it can retrieve the full daily announcement batch more reliably.
本仓库默认设置为每周一到周五北京时间 10:00 运行，这样可以更稳定地获取当天完整的 arXiv 公告批次。

In normal weeks without holidays, your email schedule is:
在不考虑节假日的正常情况下，你收到邮件的大致节奏如下：

- Monday 10:00 Beijing time: the batch announced by arXiv on Sunday 20:00 ET.
  周一北京时间 10:00：收到 arXiv 在美东周日 20:00 公告的那一批论文。
- Tuesday 10:00 Beijing time: the batch announced by arXiv on Monday 20:00 ET.
  周二北京时间 10:00：收到 arXiv 在美东周一 20:00 公告的那一批论文。
- Wednesday 10:00 Beijing time: the batch announced by arXiv on Tuesday 20:00 ET.
  周三北京时间 10:00：收到 arXiv 在美东周二 20:00 公告的那一批论文。
- Thursday 10:00 Beijing time: the batch announced by arXiv on Wednesday 20:00 ET.
  周四北京时间 10:00：收到 arXiv 在美东周三 20:00 公告的那一批论文。
- Friday 10:00 Beijing time: the batch announced by arXiv on Thursday 20:00 ET.
  周五北京时间 10:00：收到 arXiv 在美东周四 20:00 公告的那一批论文。

Why there is usually no email on Saturday or Sunday / 为什么周六周日通常没有邮件：

- arXiv can still receive submissions during the weekend.
  arXiv 在周末仍然可以接收投稿。
- However, those submissions are not announced immediately as a separate public batch.
  但是这些投稿不会立刻形成一个新的公开公告批次。
- Since arXiv usually does not publish regular announcements on Friday or Saturday ET, weekend-adjacent submissions are rolled into the next available announcement batch.
  由于 arXiv 通常不会在美东周五和周六发布常规公告，因此周末前后的投稿会被合并到下一次可用的公告批次中。

In other words, what you receive is the latest official arXiv announcement batch, not a real-time stream of all papers submitted during the Beijing calendar day.
换句话说，你收到的是 arXiv 最新一次“官方公告批次”的完整论文列表，而不是“北京时间当天实时投稿流”。

### Backfill a specific date
If today is `2026-03-18` in Beijing time and you want the papers of `2026-03-16`, follow these steps:
如果今天是北京时间 `2026-03-18`，而你想获取 `2026-03-16` 的论文，可以按下面步骤操作：

1. Make sure your `CUSTOM_CONFIG` contains:
   请确认你的 `CUSTOM_CONFIG` 中包含以下配置：
```yaml
executor:
  debug: ${oc.env:DEBUG,null}
  target_date: ${oc.env:TARGET_DATE,null}
  source: ['arxiv']
```

2. Open your forked repository on GitHub and go to `Actions`.
   打开你自己的 GitHub 仓库，进入 `Actions` 页面。

3. Select the workflow `Send emails daily`.
   选择工作流 `Send emails daily`。

4. Click `Run workflow`.
   点击 `Run workflow`。

5. Fill in the input `target_date` with:
   在输入框 `target_date` 中填写：
```text
2026-03-16
```

6. Run the workflow and wait for it to finish. The workflow will retrieve the arXiv papers for `2026-03-16`, rerank them, and send the email after completion.
   运行后等待任务完成。该工作流会检索 `2026-03-16` 的 arXiv 论文、完成排序，并在结束后发送邮件。

>[!TIP]
> It is recommended to pass `target_date` from the manual workflow input instead of storing `TARGET_DATE` as a long-lived secret. Otherwise, future scheduled runs may keep using the same fixed date until you remove or change that secret.
> 建议通过手动运行 workflow 时填写 `target_date`，而不是长期把 `TARGET_DATE` 存成 secret。否则之后的定时任务可能会一直重复使用这个固定日期，直到你手动修改或删除该 secret。

### Local Running
Supported by [uv](https://github.com/astral-sh/uv), this workflow can easily run on your local device if uv is installed:
```bash
# set all the environment variables
# export ZOTERO_ID=xxxx
# ...
cd zotero-arxiv-daily
uv run main.py
```

## 🚀 Sync with the latest version
This project is in active development. You can subscribe this repo via `Watch` so that you can be notified once we publish new release.

![Watch](./assets/subscribe_release.png)


## 📖 How it works
*Zotero-arXiv-Daily* firstly retrieves all the papers in your Zotero library and all the papers in the latest daily release or a configured `target_date`, via corresponding API. Then it calculates the embedding of each paper's title and abstract against the abstracts in your Zotero library. The score of a paper is its weighted average similarity over all your Zotero papers (newer paper added to the library has higher weight). The TLDR of each paper is generated by LLM from the title and abstract, without downloading the paper PDF during reranking or email generation.

## 📌 Limitations
- The recommendation algorithm is very simple, it may not accurately reflect your interest. Welcome better ideas for improving the algorithm!
- High `MAX_PAPER_NUM` can lead the execution time exceed the limitation of Github Action runner (6h per execution for public repo, and 2000 mins per month for private repo). Commonly, the quota given to public repo is definitely enough for individual use. If you have special requirements, you can deploy the workflow in your own server, or use a self-hosted Github Action runner, or pay for the exceeded execution time.

## 👯‍♂️ Contribution
Any issue and PR are welcomed! But remember that **each PR should merge to the `dev` branch**.

## 📃 License
Distributed under the AGPLv3 License. See `LICENSE` for detail.

## ❤️ Acknowledgement
- [pyzotero](https://github.com/urschrei/pyzotero)
- [arxiv](https://github.com/lukasschwab/arxiv.py)
- [sentence_transformers](https://github.com/UKPLab/sentence-transformers)
