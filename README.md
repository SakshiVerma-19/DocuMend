# Documend

Documend is a research-document processing project intended to help discover papers, extract useful content, and synthesize findings into readable outputs.

> **Project status:** The repository currently contains the initial Python scaffold. The application entry point, agent modules, tools, tests, and dependency manifest are present but not implemented yet.

## Repository Layout

```text
.
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── agents/
│   ├── extraction.py        # Document and paper extraction agent
│   ├── paper_crawler.py     # Paper discovery and retrieval agent
│   └── synthesis.py         # Research synthesis agent
├── tools/                   # Shared agent tools and integrations
├── memory/                  # Persistent or intermediate project memory
├── tests/                   # Automated tests
└── deployment/              # Deployment configuration and scripts
```

## Prerequisites

- Python 3.10 or newer
- A virtual environment
- API credentials for the services used by the eventual crawler and synthesis workflow

## Getting Started

From the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

The dependency manifest and `main.py` are currently placeholders, so the final two commands will not start a functional application until implementation is added.

## Configuration

Store local credentials in a `.env` file that is never committed to source control. The current local configuration uses the following variable names:

```dotenv
GOOGLE_API_KEY=your-google-api-key
NCBI_API_KEY=your-ncbi-api-key
GOOGLE_GENAI_USE_VERTEXAI=0
```

Do not paste real API keys into this README or commit them to the repository. If credentials have been exposed, revoke and rotate them before continuing development.

Once configuration loading is implemented, the application should read these values from the environment rather than hard-coding credentials in Python files.

## Intended Workflow

The planned research workflow is:

1. **Discover:** `agents/paper_crawler.py` finds relevant papers and retrieves their metadata or source documents.
2. **Extract:** `agents/extraction.py` converts documents into structured text and research facts.
3. **Synthesize:** `agents/synthesis.py` combines extracted evidence into a concise, traceable result.
4. **Persist:** `memory/` and the tools layer store intermediate state and support integrations.

The exact interfaces between these stages still need to be defined as implementation progresses.

## Development

Keep changes focused by layer:

- Put orchestration and CLI/API startup in `main.py`.
- Keep paper retrieval and crawling concerns in `agents/paper_crawler.py`.
- Keep parsing and structured extraction in `agents/extraction.py`.
- Keep summarization and cross-paper reasoning in `agents/synthesis.py`.
- Add reusable integrations under `tools/`.
- Add tests under `tests/` that cover each agent independently before adding end-to-end workflows.

Run the test suite with:

```powershell
python -m pytest
```

Tests are not yet implemented in the current scaffold.

## Roadmap

- Define the command-line or service interface in `main.py`.
- Add and pin runtime dependencies in `requirements.txt`.
- Implement paper discovery, extraction, and synthesis contracts.
- Add environment loading and credential validation.
- Add unit tests and an end-to-end example.
- Document deployment requirements under `deployment/`.

## License

No license has been defined for this project yet.
