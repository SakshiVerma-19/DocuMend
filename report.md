# Documend Project Report

## 1. Executive Summary

Documend is an intended research-document processing system. Its goal is to reduce the manual effort involved in discovering academic papers, extracting useful information from those papers, and synthesizing evidence into readable research outputs.

The repository currently contains the initial Python project structure. The major modules have been named, but their implementation has not yet been added. Therefore, this report describes both the current repository state and the intended system design. Statements marked as **planned** describe the target architecture, not functionality that is currently available.

## 2. Project Objectives

The project is intended to:

- Find relevant academic papers from supported research sources.
- Retrieve paper metadata and available document content.
- Extract structured facts, methods, results, and citations from documents.
- Combine evidence from multiple papers into a coherent synthesis.
- Preserve enough source context to make generated conclusions traceable.
- Provide a maintainable foundation for future research automation and deployment.

The central design principle is to separate retrieval, extraction, synthesis, and persistence so that each stage can be tested and improved independently.

## 3. Current Repository Status

The repository is presently a scaffold rather than a working application.

| Area | Current state |
| --- | --- |
| Application entry point | `main.py` exists but is not implemented |
| Agent modules | Extraction, crawler, and synthesis modules exist but are not implemented |
| Shared tools | Package directory exists with an initializer only |
| Dependencies | `requirements.txt` is currently empty |
| Tests | Test package exists but contains no test cases |
| Deployment | Directory exists but contains no deployment configuration |
| Memory | Directory exists but contains no persistence implementation |
| Documentation | `README.md` and this report document the planned direction |

This status is important: the architecture below is a design target and should not be interpreted as evidence that the full workflow already runs.

## 4. Technology Stack

### 4.1 Confirmed or intended technologies

| Technology | Role | Status and rationale |
| --- | --- | --- |
| Python | Primary implementation language | Used for the project scaffold; well suited to document processing, web requests, NLP, and AI integration |
| Google Generative AI | Planned language-model provider | Suggested by the existing `GOOGLE_API_KEY` and `GOOGLE_GENAI_USE_VERTEXAI` configuration variables; intended for extraction and synthesis |
| NCBI services | Planned scientific literature source | Suggested by the existing `NCBI_API_KEY`; intended for biomedical and life-science paper discovery or metadata retrieval |
| Environment variables | Configuration and secret management boundary | Used through `.env`-style variable names so credentials do not need to be embedded in source code |
| Pytest | Planned testing framework | Referenced by the documented test command; test dependencies still need to be added |

### 4.2 Dependency status

No runtime dependencies are currently pinned in `requirements.txt`. Before the application can run, the project will need to select and document packages for at least:

- Environment loading and configuration validation.
- HTTP requests and API clients.
- Paper metadata and document retrieval.
- Document parsing and text extraction.
- Google GenAI access.
- Testing and mocking external services.

The exact package choices should be made alongside the first implementation rather than assumed from the directory names.

### 4.3 Configuration variables

The current local configuration contains these variable names:

```dotenv
GOOGLE_API_KEY=your-google-api-key
NCBI_API_KEY=your-ncbi-api-key
GOOGLE_GENAI_USE_VERTEXAI=0
```

Their planned purposes are:

- `GOOGLE_API_KEY`: authenticates requests to Google AI services when API-key authentication is selected.
- `NCBI_API_KEY`: authenticates or increases the permitted request rate for NCBI services.
- `GOOGLE_GENAI_USE_VERTEXAI`: selects whether the Google integration uses Vertex AI rather than the direct API-key path.

Real credentials must remain outside version control. Any credentials that have been exposed should be revoked and replaced.

## 5. System Architecture

The target system is organized as a staged pipeline:

```text
User request
    |
    v
Application orchestration (`main.py`)
    |
    v
Paper discovery and retrieval (`agents/paper_crawler.py`)
    |
    v
Document parsing and fact extraction (`agents/extraction.py`)
    |
    v
Evidence storage and shared tools (`memory/`, `tools/`)
    |
    v
Cross-document synthesis (`agents/synthesis.py`)
    |
    v
Traceable research output
```

### 5.1 `main.py`

`main.py` is intended to be the application entry point and orchestration layer. It should be responsible for:

- Loading and validating configuration.
- Accepting a research question or request.
- Creating or invoking the required agents.
- Coordinating the order of pipeline stages.
- Handling user-facing errors and exit codes.
- Returning or saving the final result.

It should avoid containing the detailed crawling, extraction, and synthesis logic itself.

### 5.2 Paper crawler agent

`agents/paper_crawler.py` is intended to discover relevant literature and retrieve source information. A useful crawler contract would include:

- Search query construction.
- Source-specific request handling.
- Rate limiting and retry behavior.
- Result normalization into a common paper metadata format.
- Deduplication using identifiers such as DOI, PMID, or a normalized title.
- Clear handling of missing abstracts, inaccessible full text, and API errors.

### 5.3 Extraction agent

`agents/extraction.py` is intended to convert retrieved documents into structured evidence. Potential extraction fields include:

- Paper identity and citation metadata.
- Research question or objective.
- Population, dataset, or experimental material.
- Methodology and study design.
- Main findings and reported measurements.
- Limitations identified by the authors.
- Important quotations or source spans.

The extraction stage should retain source references for each important claim. This reduces the risk that the synthesis stage produces unsupported conclusions.

### 5.4 Synthesis agent

`agents/synthesis.py` is intended to compare extracted evidence across papers and produce a readable answer. It should distinguish:

- Direct findings from interpretation.
- Agreement and disagreement between sources.
- Strong evidence from weak or incomplete evidence.
- Reported facts from model-generated summaries.
- Known gaps from conclusions that are not supported by the retrieved material.

The synthesis output should include citations or paper identifiers wherever possible.

### 5.5 Tools layer

`tools/` is intended for reusable integrations and cross-cutting helpers, such as:

- API clients.
- HTTP and retry utilities.
- Document download and parsing helpers.
- Prompt construction and response validation.
- Citation formatting.
- Logging and observability.

Keeping these concerns outside the agent modules will make the agents easier to test and replace.

### 5.6 Memory layer

`memory/` is intended to hold intermediate or persistent project state. A future implementation may store:

- Search requests and normalized results.
- Extracted paper records.
- Cached documents and hashes.
- Synthesis inputs and outputs.
- Processing status and failure information.

The storage strategy has not yet been selected. It should account for privacy, retention, reproducibility, and the size of downloaded documents.

### 5.7 Deployment layer

`deployment/` is reserved for deployment configuration. Possible future contents include container definitions, environment templates, service configuration, health checks, and deployment instructions.

## 6. End-to-End System Flow

The intended flow is as follows.

### Step 1: Receive a research request

The user provides a question, topic, or search criteria. The orchestration layer validates that the request is non-empty and applies any limits such as maximum papers or date range.

### Step 2: Discover papers

The crawler translates the request into source-specific searches. It queries supported literature services, normalizes the results, removes duplicates, and returns a bounded set of candidate papers.

### Step 3: Retrieve available content

For each candidate, the system retrieves metadata, abstracts, and full text where access is available. It records failures rather than silently dropping papers.

### Step 4: Extract structured evidence

The extraction agent processes the retrieved content and produces structured records. Each record should carry its paper identity and, where feasible, the text span or section supporting each extracted claim.

### Step 5: Validate extracted records

The system checks that required fields are present, that the response can be parsed, and that extracted claims remain associated with their sources. Invalid records should be flagged for retry or exclusion.

### Step 6: Synthesize findings

The synthesis agent receives the validated evidence records, compares them, identifies patterns and disagreements, and generates a response appropriate to the original request.

### Step 7: Present and persist the result

The final response is returned to the user with citations and limitations. The system may persist normalized metadata, evidence, and processing status for later reuse, subject to an explicit retention policy.

## 7. Why This Design

### Modular agents

Separate agents allow retrieval, extraction, and synthesis to evolve independently. A better paper source can be added without rewriting synthesis, and a new extraction strategy can be evaluated without changing the crawler.

### Python

Python has a mature ecosystem for HTTP clients, scientific metadata, document parsing, testing, and AI SDKs. It also makes it practical to prototype the workflow quickly while preserving a path to production services.

### External literature APIs

Using structured literature services is more reliable than depending solely on general web scraping. APIs can provide stable identifiers, metadata, query parameters, and clearer usage limits. NCBI is particularly relevant for biomedical literature.

### Generative AI for extraction and synthesis

Language models can help convert inconsistent paper prose into a common structure and can compare evidence across many documents. The model should be constrained by retrieved source material and validated output schemas rather than treated as an authoritative database.

### Environment-based configuration

Environment variables keep credentials and deployment-specific settings outside application code. This supports local development, CI, and deployment environments without requiring source changes.

### Explicit memory boundary

Separating memory from the agents makes caching, reproducibility, and future persistence choices visible. It also prevents agent logic from becoming tightly coupled to one storage implementation.

## 8. Advantages

- **Reduced research effort:** Automates repetitive discovery, reading, and comparison tasks.
- **Separation of responsibilities:** Each pipeline stage has a clear purpose and can be tested independently.
- **Source-aware results:** The planned evidence model can associate conclusions with their originating papers.
- **Extensibility:** Additional literature sources, parsers, or model providers can be introduced behind focused interfaces.
- **Repeatability:** Persisted normalized records can make repeated research requests faster and easier to audit.
- **Domain flexibility:** Although NCBI suggests a biomedical starting point, the architecture can support other scholarly domains.
- **Operational control:** Rate limiting, caching, retries, and validation can be implemented in shared tools rather than duplicated across agents.

## 9. Limitations and Risks

### Current implementation gap

The largest limitation is that the current repository does not yet contain an executable workflow. The modules, dependencies, tests, and deployment files must be implemented before the project can be evaluated in practice.

### Retrieval coverage

Not every paper will be accessible in full text. Paywalls, missing abstracts, publisher restrictions, and source-specific rate limits can produce incomplete evidence.

### Model reliability

Generative models can hallucinate, misread technical language, omit qualifications, or combine findings incorrectly. Structured prompts and output validation reduce these risks but cannot remove them entirely.

### Citation quality

A citation attached to a paragraph does not guarantee that every sentence in that paragraph is supported. The system will need claim-level source references and checks for unsupported statements.

### API and cost constraints

External services may impose quotas, latency, availability limits, or usage costs. Large document batches can make both retrieval and model inference expensive.

### Document variability

PDFs, HTML pages, XML records, scanned documents, tables, figures, and supplementary material require different parsing strategies. Extraction quality will vary by format.

### Privacy and retention

Downloaded papers, user questions, and generated reports may contain sensitive or proprietary information. Storage, logging, and model-provider policies must be reviewed before production use.

### Reproducibility

Model outputs can change as providers update models. Reproducible reports will require recorded model versions, prompts, source identifiers, timestamps, and processing settings.

## 10. Testing and Quality Strategy

The project should introduce tests in layers:

1. **Unit tests:** Validate query construction, metadata normalization, deduplication, parsers, configuration, and response validation.
2. **Agent tests:** Run crawler, extraction, and synthesis logic against fixtures and mocked external services.
3. **Contract tests:** Confirm that each stage produces the fields required by the next stage.
4. **Integration tests:** Exercise the complete pipeline with a small controlled dataset.
5. **Evaluation tests:** Compare generated extraction and synthesis against reviewed examples for factuality, completeness, and citation support.

External API tests should use mocks or recorded fixtures by default. Live service tests should be explicit, rate-limited, and excluded from ordinary local test runs.

## 11. Security and Operations

- Never commit `.env` files or API credentials.
- Rotate any credentials that have been exposed.
- Validate configuration at startup and fail with actionable messages.
- Apply timeouts, retry limits, and rate limits to external requests.
- Avoid logging complete documents or credentials.
- Sanitize user input before including it in prompts or external queries.
- Track source identifiers and processing timestamps for auditability.
- Add structured logging and health checks before deployment.
- Define data retention and deletion behavior for cached papers and generated reports.

## 12. Future Enhancements

### Near-term implementation

- Define typed data models for papers, documents, evidence, and synthesis results.
- Implement configuration loading and validation.
- Add the first NCBI search and metadata retrieval flow.
- Add a minimal extraction and synthesis path using a controlled prompt contract.
- Populate `requirements.txt` with pinned, reviewed dependencies.
- Add unit tests for the first working slice.

### Reliability improvements

- Add retries with exponential backoff and provider-specific rate limits.
- Cache normalized metadata and document hashes.
- Add schema validation and automatic retry for malformed model responses.
- Detect duplicate papers across sources.
- Preserve claim-level provenance and source excerpts.
- Add observability for latency, failures, token usage, and cost.

### Product improvements

- Support interactive refinement of search queries.
- Add configurable date, source, topic, and paper-count filters.
- Provide export formats such as Markdown, JSON, and citation files.
- Add a web or API interface around the pipeline.
- Allow users to inspect the evidence behind each conclusion.
- Add saved research projects and resumable workflows.

### Advanced capabilities

- Add additional scholarly sources and domain-specific parsers.
- Support table and figure extraction.
- Add hybrid keyword and semantic search.
- Add human review checkpoints for high-impact reports.
- Evaluate multiple model providers and fallback strategies.
- Add scheduled literature monitoring and change notifications.

## 13. Recommended Implementation Order

2. Define typed interfaces for the crawler, extractor, synthesizer, and storage boundary.
3. Implement configuration loading and a simple command-line entry point.
4. Implement one reliable literature-source integration.
5. Add document normalization and extraction fixtures.
6. Add a constrained synthesis flow with citations.
7. Add unit, integration, and evaluation tests.
8. Add caching, observability, and deployment configuration.

## 14. Conclusion

Documend has a sensible initial separation of concerns for an AI-assisted research workflow: discovery, extraction, synthesis, shared tools, memory, tests, and deployment are already represented in the directory structure. Its current limitation is not architectural complexity but implementation completeness. The next milestone should be a small, testable end-to-end slice with one paper source, structured evidence, and traceable synthesis before expanding coverage or deployment features.