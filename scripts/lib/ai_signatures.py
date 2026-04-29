"""
Authoritative pattern catalog for AI asset discovery.

This module is the *only* place where signatures live. Every scanner imports
from here so that adding a new vendor / framework / pattern is a one-line edit.

All patterns are precompiled regexes. The catalogs are intentionally wide:
false positives are cheaper than missed AI assets in the Discover step.

Categories:
- SDK_IMPORTS:       module/package import patterns for AI SDKs
- MODEL_API_HOSTS:   network destinations associated with model providers
- AI_ENV_VARS:       environment variable names that gate AI access
- API_KEY_PATTERNS:  vendor-specific API key formats (DO NOT log key values)
- MCP_HINTS:         signals that an MCP server / client is configured
- VECTOR_STORE:      vector DB / embedding store SDKs and config
- PROMPT_FILES:      filename patterns for prompts / system messages
- AGENT_FRAMEWORKS:  agent / orchestration frameworks
- RAG_HINTS:         retrieval-augmented generation framework signals
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Signature:
    """A single named regex pattern with the asset_class it implies."""

    name: str
    pattern: re.Pattern
    asset_class: str  # must align with templates/ai-asset-schema.json enum
    note: str = ""


def _ci(pat: str) -> re.Pattern:
    return re.compile(pat, re.IGNORECASE)


# ---------------------------------------------------------------------------
# SDK imports — Python, JavaScript/TypeScript, Go, etc.
# Match `import`, `from ... import`, `require(...)`, `from "..."` styles.
# ---------------------------------------------------------------------------

SDK_IMPORTS: tuple[Signature, ...] = (
    Signature("openai-python", _ci(r"\b(?:from|import)\s+openai\b"), "model_api_gateway"),
    Signature("openai-node", _ci(r"""(?:require|from)\s*\(?\s*['"]openai['"]"""), "model_api_gateway"),
    Signature("anthropic-python", _ci(r"\b(?:from|import)\s+anthropic\b"), "model_api_gateway"),
    Signature("anthropic-node", _ci(r"""(?:require|from)\s*\(?\s*['"]@anthropic-ai/sdk['"]"""), "model_api_gateway"),
    Signature("anthropic-bedrock", _ci(r"\bAnthropicBedrock\b"), "model_api_gateway"),
    Signature("anthropic-vertex", _ci(r"\bAnthropicVertex\b"), "model_api_gateway"),
    Signature("google-genai", _ci(r"\bfrom\s+google\s+import\s+genai\b|google\.generativeai"), "model_api_gateway"),
    Signature("vertex-ai", _ci(r"\bvertexai\b"), "model_api_gateway"),
    Signature("aws-bedrock", _ci(r"""bedrock-runtime|['"]bedrock['"]"""), "model_api_gateway"),
    Signature("azure-openai", _ci(r"\bAzureOpenAI\b|azure\.ai\.openai|openai\.azure\.com"), "model_api_gateway"),
    Signature("cohere", _ci(r"\b(?:from|import)\s+cohere\b|@cohere-ai/"), "model_api_gateway"),
    Signature("mistral", _ci(r"\bmistralai\b"), "model_api_gateway"),
    Signature("groq", _ci(r"\bgroq\b"), "model_api_gateway"),
    Signature("together-ai", _ci(r"\btogether\b.*\b(api|client)\b|together_ai"), "model_api_gateway"),
    Signature("replicate", _ci(r"\breplicate\b"), "model_api_gateway"),
    Signature("huggingface-hub", _ci(r"\bhuggingface_hub\b|@huggingface/"), "model_api_gateway"),
    Signature("transformers", _ci(r"\bfrom\s+transformers\b|@xenova/transformers"), "custom_internal_agent"),
    Signature("ollama", _ci(r"\bollama\b"), "model_api_gateway"),
    Signature("anthropic-claude-code-sdk", _ci(r"@anthropic-ai/claude-(?:code|agent)-sdk|claude_(?:code|agent)_sdk"), "ide_cli_agent"),
    Signature("openai-agents-sdk", _ci(r"@openai/agents|openai\.agents"), "enterprise_agent"),
    Signature("langchain", _ci(r"\b(?:from|import)\s+langchain\b|@langchain/"), "custom_internal_agent"),
    Signature("langgraph", _ci(r"\blanggraph\b"), "custom_internal_agent"),
    Signature("llamaindex", _ci(r"\bllama_index\b|llamaindex"), "custom_internal_agent"),
    Signature("haystack", _ci(r"\bhaystack\b"), "custom_internal_agent"),
    Signature("semantic-kernel", _ci(r"\bsemantic_kernel\b|@microsoft/semantic-kernel"), "custom_internal_agent"),
    Signature("autogen", _ci(r"\b(?:from|import)\s+autogen\b|pyautogen"), "custom_internal_agent"),
    Signature("crewai", _ci(r"\bcrewai\b"), "custom_internal_agent"),
    Signature("instructor", _ci(r"\b(?:from|import)\s+instructor\b"), "custom_internal_agent"),
    Signature("dspy", _ci(r"\b(?:from|import)\s+dspy\b"), "custom_internal_agent"),
)


# ---------------------------------------------------------------------------
# Model API hostnames / endpoints — match in code, configs, env files.
# These are the network destinations the org's egress controls should know.
# ---------------------------------------------------------------------------

MODEL_API_HOSTS: tuple[Signature, ...] = (
    Signature("openai-host", _ci(r"\bapi\.openai\.com\b"), "model_api_gateway"),
    Signature("anthropic-host", _ci(r"\bapi\.anthropic\.com\b"), "model_api_gateway"),
    Signature("anthropic-claude-host", _ci(r"\bclaude\.ai\b"), "saas_llm"),
    Signature("google-genai-host", _ci(r"\bgenerativelanguage\.googleapis\.com\b"), "model_api_gateway"),
    Signature("vertex-host", _ci(r"\baiplatform\.googleapis\.com\b"), "model_api_gateway"),
    Signature("azure-openai-host", _ci(r"\b[a-z0-9-]+\.openai\.azure\.com\b"), "model_api_gateway"),
    Signature("bedrock-host", _ci(r"\bbedrock(?:-runtime)?\.[a-z0-9-]+\.amazonaws\.com\b"), "model_api_gateway"),
    Signature("cohere-host", _ci(r"\bapi\.cohere\.(?:ai|com)\b"), "model_api_gateway"),
    Signature("mistral-host", _ci(r"\bapi\.mistral\.ai\b"), "model_api_gateway"),
    Signature("groq-host", _ci(r"\bapi\.groq\.com\b"), "model_api_gateway"),
    Signature("together-host", _ci(r"\bapi\.together\.xyz\b"), "model_api_gateway"),
    Signature("replicate-host", _ci(r"\bapi\.replicate\.com\b"), "model_api_gateway"),
    Signature("huggingface-host", _ci(r"\b(?:api-inference\.|huggingface\.co)\b"), "model_api_gateway"),
    Signature("ollama-host", _ci(r"\b(?:localhost|127\.0\.0\.1):11434\b"), "model_api_gateway"),
    Signature("openrouter-host", _ci(r"\bopenrouter\.ai\b"), "model_api_gateway"),
    Signature("perplexity-host", _ci(r"\bapi\.perplexity\.ai\b"), "saas_llm"),
    Signature("chatgpt-host", _ci(r"\bchatgpt\.com\b"), "saas_llm"),
    Signature("gemini-host", _ci(r"\bgemini\.google\.com\b"), "saas_llm"),
    Signature("copilot-microsoft-host", _ci(r"\bcopilot\.microsoft\.com\b"), "saas_llm"),
    Signature("github-copilot-host", _ci(r"\b(?:api\.githubcopilot\.com|copilot-proxy\.githubusercontent\.com)\b"), "ide_cli_agent"),
)


# ---------------------------------------------------------------------------
# Environment variables — strong signals that AI access is configured.
# ---------------------------------------------------------------------------

AI_ENV_VARS: tuple[Signature, ...] = (
    Signature("OPENAI_API_KEY", _ci(r"\bOPENAI_API_KEY\b"), "model_api_gateway"),
    Signature("OPENAI_ORG_ID", _ci(r"\bOPENAI_ORG_ID\b"), "model_api_gateway"),
    Signature("AZURE_OPENAI_API_KEY", _ci(r"\bAZURE_OPENAI_API_KEY\b"), "model_api_gateway"),
    Signature("AZURE_OPENAI_ENDPOINT", _ci(r"\bAZURE_OPENAI_ENDPOINT\b"), "model_api_gateway"),
    Signature("ANTHROPIC_API_KEY", _ci(r"\bANTHROPIC_API_KEY\b"), "model_api_gateway"),
    Signature("CLAUDE_API_KEY", _ci(r"\bCLAUDE_API_KEY\b"), "model_api_gateway"),
    Signature("GOOGLE_API_KEY", _ci(r"\bGOOGLE_API_KEY\b"), "model_api_gateway"),
    Signature("GEMINI_API_KEY", _ci(r"\bGEMINI_API_KEY\b"), "model_api_gateway"),
    Signature("GOOGLE_APPLICATION_CREDENTIALS", _ci(r"\bGOOGLE_APPLICATION_CREDENTIALS\b"), "model_api_gateway"),
    Signature("AWS_BEDROCK", _ci(r"\bAWS_BEDROCK_[A-Z_]+\b|\bBEDROCK_[A-Z_]+\b"), "model_api_gateway"),
    Signature("COHERE_API_KEY", _ci(r"\bCOHERE_API_KEY\b"), "model_api_gateway"),
    Signature("MISTRAL_API_KEY", _ci(r"\bMISTRAL_API_KEY\b"), "model_api_gateway"),
    Signature("GROQ_API_KEY", _ci(r"\bGROQ_API_KEY\b"), "model_api_gateway"),
    Signature("TOGETHER_API_KEY", _ci(r"\bTOGETHER_API_KEY\b"), "model_api_gateway"),
    Signature("REPLICATE_API_TOKEN", _ci(r"\bREPLICATE_API_TOKEN\b"), "model_api_gateway"),
    Signature("HUGGINGFACE_TOKEN", _ci(r"\b(?:HUGGINGFACE|HF)_(?:TOKEN|API_KEY)\b"), "model_api_gateway"),
    Signature("PINECONE_API_KEY", _ci(r"\bPINECONE_API_KEY\b"), "vector_database"),
    Signature("WEAVIATE_API_KEY", _ci(r"\bWEAVIATE_API_KEY\b"), "vector_database"),
    Signature("QDRANT_API_KEY", _ci(r"\bQDRANT_API_KEY\b"), "vector_database"),
    Signature("CHROMA", _ci(r"\bCHROMA_[A-Z_]+\b"), "vector_database"),
    Signature("OLLAMA_HOST", _ci(r"\bOLLAMA_HOST\b"), "model_api_gateway"),
    Signature("LANGCHAIN_API_KEY", _ci(r"\bLANGCHAIN_API_KEY\b|\bLANGSMITH_API_KEY\b"), "custom_internal_agent"),
)


# ---------------------------------------------------------------------------
# API-key formats — vendor-specific, used to flag *exposed* credentials.
# CRITICAL: scanners must NEVER log the matched value. Only the file/line/type.
# ---------------------------------------------------------------------------

API_KEY_PATTERNS: tuple[Signature, ...] = (
    # OpenAI: sk-... , sk-proj-..., variable lengths over time.
    Signature("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{20,}\b"), "model_api_gateway",
              note="OpenAI API key"),
    # Anthropic: sk-ant-...
    Signature("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"), "model_api_gateway",
              note="Anthropic API key"),
    # Google AI Studio: AIza... (40 chars typical)
    Signature("google-ai-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "model_api_gateway",
              note="Google AI / Gemini key"),
    # Hugging Face: hf_...
    Signature("hf-token", re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"), "model_api_gateway",
              note="Hugging Face token"),
    # Cohere
    Signature("cohere-key", re.compile(r"\bco-[A-Za-z0-9]{30,}\b"), "model_api_gateway",
              note="Cohere key (heuristic)"),
    # Replicate
    Signature("replicate-token", re.compile(r"\br8_[A-Za-z0-9]{30,}\b"), "model_api_gateway",
              note="Replicate token"),
    # Groq
    Signature("groq-key", re.compile(r"\bgsk_[A-Za-z0-9]{30,}\b"), "model_api_gateway",
              note="Groq key"),
    # Mistral
    Signature("mistral-key", re.compile(r"\b[A-Za-z0-9]{32,}\b(?=.*mistral)", re.IGNORECASE), "model_api_gateway",
              note="Mistral key (context heuristic)"),
)


# ---------------------------------------------------------------------------
# MCP servers / clients
# ---------------------------------------------------------------------------

MCP_HINTS: tuple[Signature, ...] = (
    Signature("mcp-config", _ci(r"\bmcpServers\b"), "enterprise_agent",
              note="Claude Desktop / Code MCP config block"),
    Signature("mcp-sdk-py", _ci(r"\bfrom\s+mcp\b|@modelcontextprotocol/"), "enterprise_agent"),
    Signature("mcp-server-decl", _ci(r"\bMCP\s+server\b|model[-_ ]context[-_ ]protocol"), "enterprise_agent"),
)


# ---------------------------------------------------------------------------
# Vector stores
# ---------------------------------------------------------------------------

VECTOR_STORE: tuple[Signature, ...] = (
    Signature("pinecone", _ci(r"\bpinecone\b"), "vector_database"),
    Signature("weaviate", _ci(r"\bweaviate\b"), "vector_database"),
    Signature("qdrant", _ci(r"\bqdrant\b"), "vector_database"),
    Signature("chroma", _ci(r"\bchromadb\b|chroma_client"), "vector_database"),
    Signature("milvus", _ci(r"\bmilvus\b"), "vector_database"),
    Signature("pgvector", _ci(r"\bpgvector\b|vector\(\d+\)"), "vector_database"),
    Signature("opensearch-knn", _ci(r"\bknn_vector\b"), "vector_database"),
    Signature("faiss", _ci(r"\bfaiss\b"), "vector_database"),
)


# ---------------------------------------------------------------------------
# Prompt / system message files
# ---------------------------------------------------------------------------

# Filename patterns (matched against basename, case-insensitive).
PROMPT_FILE_PATTERNS: tuple[re.Pattern, ...] = (
    _ci(r"^prompt(s)?\.(md|txt|yaml|yml|json|tmpl)$"),
    _ci(r"^system_?prompt\.(md|txt|yaml|yml|json|tmpl)$"),
    _ci(r"^.+\.prompt(\.md|\.txt|\.tmpl)?$"),
    _ci(r"^claude\.md$"),  # Claude Code project memory
    _ci(r"^agents?\.md$"),
)


# ---------------------------------------------------------------------------
# Agent / orchestration frameworks (filename or import-level signals
# beyond what SDK_IMPORTS catches)
# ---------------------------------------------------------------------------

AGENT_FRAMEWORKS: tuple[Signature, ...] = (
    Signature("agents-toml", _ci(r"^\[agents?\]"), "custom_internal_agent",
              note="agents.toml or similar config block"),
    Signature("tools-decl", _ci(r"\b@?tool\b\s*\(|def\s+tool[s]?\s*\("), "custom_internal_agent"),
    Signature("function-calling", _ci(r"\bfunction_call(s)?\b|\btool_choice\b|\btool_use\b"), "custom_internal_agent"),
)


# ---------------------------------------------------------------------------
# RAG-specific signals
# ---------------------------------------------------------------------------

RAG_HINTS: tuple[Signature, ...] = (
    Signature("embeddings-api", _ci(r"\.embeddings\.create|embedding_model|embed_documents"), "rag_system"),
    Signature("retriever", _ci(r"\bretriever\b|VectorStoreRetriever|as_retriever\("), "rag_system"),
    Signature("rag", _ci(r"\bRAG\b|retrieval[-_ ]augmented"), "rag_system"),
)


# ---------------------------------------------------------------------------
# Combined catalogs for scanners that just want everything.
# ---------------------------------------------------------------------------

ALL_CONTENT_SIGNATURES: tuple[Signature, ...] = (
    *SDK_IMPORTS,
    *MODEL_API_HOSTS,
    *AI_ENV_VARS,
    *API_KEY_PATTERNS,
    *MCP_HINTS,
    *VECTOR_STORE,
    *AGENT_FRAMEWORKS,
    *RAG_HINTS,
)


# Files we never want to scan content of (binary / large / lockfiles).
SKIP_FILE_NAMES: frozenset[str] = frozenset({
    ".DS_Store", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Pipfile.lock", "Cargo.lock", "go.sum",
    "uv.lock",
})

SKIP_DIR_NAMES: frozenset[str] = frozenset({
    ".git", "node_modules", ".venv", "venv", "env",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    "dist", "build", ".next", ".nuxt", "target", "out",
    ".idea", ".vscode",
})

# Extensions whose content we will scan as text.
TEXT_EXTENSIONS: frozenset[str] = frozenset({
    ".py", ".pyi", ".pyw",
    ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx",
    ".go", ".rs", ".rb", ".java", ".kt", ".kts", ".scala",
    ".cs", ".php", ".swift", ".m", ".mm",
    ".sh", ".bash", ".zsh", ".fish", ".ps1",
    ".env", ".envrc", ".ini", ".cfg", ".conf",
    ".json", ".jsonc", ".yaml", ".yml", ".toml",
    ".md", ".mdx", ".rst", ".txt", ".tmpl",
    ".tf", ".hcl",
    ".dockerfile", "Dockerfile", "Makefile",
    ".gradle", ".sbt",
})

# Names (no extension) we still treat as text.
TEXT_FILENAMES: frozenset[str] = frozenset({
    "Dockerfile", "Makefile", "Procfile", ".env", ".envrc",
})


def is_text_path(basename: str, suffix: str) -> bool:
    """Return True if a file should be opened as text and scanned."""
    if basename in SKIP_FILE_NAMES:
        return False
    if basename in TEXT_FILENAMES:
        return True
    return suffix.lower() in TEXT_EXTENSIONS
