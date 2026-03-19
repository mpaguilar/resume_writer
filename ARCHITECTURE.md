# Architecture: resume-writer

## 1. System Overview

**Purpose:** Convert structured text resumes to various output formats (.docx, HTML, Markdown)

**Architecture Pattern:** Pipeline processing with multiple output formats

```
Input (Markdown-like text)
    ↓
Parser Layer (models/)
    ↓
Data Models (models/)
    ↓
Renderer Layer (resume_render/)
    ↓
Output (.docx, HTML, Markdown)
```

**Key Characteristics:**
- Single input format (structured text)
- Multiple output formats (.docx, HTML, Markdown)
- Settings-driven rendering (TOML configuration)
- Modular renderer architecture

---

## 2. Component Structure

### 2.1 Directory Layout

```
resume_writer/
├── main.py                    # CLI entry point
├── models/                    # Data models and parsers
│   ├── parsers.py            # Base parsing infrastructure
│   ├── resume.py             # Root resume model
│   ├── personal.py           # Personal info model
│   ├── education.py          # Education model
│   ├── experience.py         # Work experience model
│   └── certifications.py     # Certifications model
├── resume_render/             # Output renderers
│   ├── render_settings.py    # Settings/configuration classes
│   ├── resume_render_base.py # Base renderer classes
│   ├── resume_render_text_base.py  # Text-based renderer base
│   ├── docx_hyperlink.py     # .docx hyperlink utilities
│   ├── basic/                # Text-based renderer (testable)
│   ├── ats/                  # ATS-optimized .docx renderer
│   ├── plain/                # Plain .docx renderer
│   ├── html/                 # HTML renderer
│   └── markdown/             # Markdown renderer
├── utils/                     # Utility functions
│   ├── skills_matrix.py     # Skills matrix generation
│   ├── skills_splitter.py   # Skills text processing
│   ├── executive_summary.py   # Executive summary generation
│   ├── resume_stats.py       # Resume statistics
│   ├── date_format.py        # Date formatting
│   ├── markdown_parser.py    # Markdown parsing utilities
│   ├── text_doc.py           # Text document abstraction
│   ├── html_doc.py           # HTML document utilities
│   └── markdown_doc.py       # Markdown document utilities
└── renderers/                 # Additional renderers
    ├── html_renderer.py
    └── markdown_renderer.py
```

### 2.2 Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `main.py` | CLI parsing, file I/O, orchestration |
| `models/` | Parse input text into structured data models |
| `resume_render/` | Render data models to output formats |
| `utils/` | Business logic utilities (skills processing, summaries) |
| `renderers/` | Alternative rendering implementations |

---

## 3. Data Flow

### 3.1 Input Processing Flow

```
1. CLI receives input file path and options
   ↓
2. main.py reads file content
   ↓
3. ParseContext created with lines and line number tracking
   ↓
4. Resume.parse() processes top-level sections
   ↓
5. Each section has dedicated parser (Personal.parse(), Education.parse(), etc.)
   ↓
6. Result: Populated Resume object with all sections
```

### 3.2 Rendering Flow

```
1. Resume object passed to renderer
   ↓
2. Renderer reads settings (RenderSettings)
   ↓
3. For each section:
   a. Check if section is enabled in settings
   b. If enabled, call section renderer
   c. Section renderer formats and outputs content
   ↓
4. Output document saved to file
```

### 3.3 Settings Flow

```
1. Settings TOML file loaded (optional)
   ↓
2. RenderSettings aggregates all section settings
   ↓
3. Each renderer receives relevant settings subset
   ↓
4. Settings control:
   - Which sections are rendered
   - Formatting options (fonts, spacing, etc.)
   - Content inclusion flags
```

---

## 4. Core Components

### 4.1 Parser Infrastructure

**Key Classes:**

```python
# parsers.py
class ParseContext:
    """Tracks parsing state: lines, current line number, errors."""
    lines: list[str]
    line_num: int

class BaseParser:
    """Base class for all parsers."""
    @classmethod
    def parse(cls, context: ParseContext) -> Self:
        ...
```

**Parsing Pattern:**

1. Input file split into lines
2. ParseContext created with lines starting at line 0
3. Each parser consumes lines it recognizes
4. ParseContext.line_num advances as lines are consumed
5. Unknown lines or errors reported via context

**Parser Hierarchy:**

```
BaseParser (parsers.py)
├── Resume.parse() (resume.py)
├── Personal.parse() (personal.py)
├── Education.parse() (education.py)
├── Experience.parse() (experience.py)
└── Certifications.parse() (certifications.py)
```

### 4.2 Data Models

**Core Models:**

| Model | File | Contains |
|-------|------|----------|
| Resume | resume.py | Root container with all sections |
| Personal | personal.py | Contact info, websites, visa status |
| Education | education.py | Degrees, institutions, dates |
| Experience | experience.py | Work history, roles, projects |
| Certifications | certifications.py | Professional certifications |

**Model Pattern:**

```python
@dataclass
class SomeSection:
    """Section data with parsing capability."""
    field1: str
    field2: str | None
    parse_context: ParseContext

    @classmethod
    def parse(cls, context: ParseContext) -> Self:
        """Parse section from text."""
        ...
```

### 4.3 Renderer Infrastructure

**Base Classes:**

```python
# resume_render_base.py
class RenderBase:
    """Base for all renderers."""
    document: Document  # python-docx Document
    settings: RenderSettings

    def render(self) -> None:
        """Render content to document."""
        ...

# resume_render_text_base.py
class TextDocRenderer:
    """Base for text-based renderers (HTML, Markdown)."""
    lines: list[str]
    settings: RenderSettings
```

**Renderer Organization:**

Each output format has a package with section renderers:

```
resume_render/<format>/
├── __init__.py              # Package exports
├── resume_main.py           # Main renderer orchestration
├── personal_section.py      # Personal info rendering
├── education_section.py     # Education rendering
├── experience_section.py    # Experience rendering
├── certifications_section.py # Certifications rendering
├── skills_matrix_section.py # Skills matrix rendering
└── executive_summary_section.py # Summary rendering
```

### 4.4 Settings System

**Settings Classes:**

```python
# render_settings.py
@dataclass
class RenderSettings:
    """Root settings container."""
    personal_settings: PersonalSettings
    education_settings: EducationSettings
    experience_settings: ExperienceSettings
    ...

@dataclass
class PersonalSettings:
    """Settings for personal section."""
    name: bool = True
    email: bool = True
    phone: bool = True
    ...
```

**Settings Inheritance:**

1. Default values defined in settings classes
2. TOML file overrides specific values
3. Missing settings use defaults
4. All settings are optional

---

## 5. Output Formats

### 5.1 Format Comparison

| Format | Purpose | Test Coverage | Notes |
|--------|---------|---------------|-------|
| **basic** | Testing/debugging | High | Text-based, easily testable |
| **plain** | Human-readable | Low | .docx, loosely based on EngineeringResumes subreddit format |
| **ats** | ATS parsing | None | .docx, no columns/tables/bullets |
| **html** | Web display | None | Unstyled HTML output |
| **markdown** | Text processing | None | Markdown output |

### 5.2 Format Selection Logic

```python
# main.py
if resume_type == "basic":
    renderer = BasicResumeRenderer(...)
elif resume_type == "plain":
    renderer = PlainResumeRenderer(...)
elif resume_type == "ats":
    renderer = ATSResumeRenderer(...)
elif resume_type == "html":
    renderer = HTMLResumeRenderer(...)
```

---

## 6. Key Design Patterns

### 6.1 ParseContext Pattern

**Problem:** Track parsing state across multiple parsers

**Solution:** Immutable context object passed through parse chain

```python
context = ParseContext(lines, line_num=0)
resume = Resume.parse(context)
# context.line_num now at end of consumed lines
```

### 6.2 Settings-Driven Rendering

**Problem:** Control output format without code changes

**Solution:** TOML settings file controls renderer behavior

```toml
[personal]
name = true
email = true
phone = false  # Omit phone number
```

### 6.3 Renderer Inheritance

**Problem:** Share common rendering logic across formats

**Solution:** Base classes with format-specific overrides

```python
class RenderBase:
    def add_heading(self, text: str, level: int) -> None:
        """Add heading - implemented by subclasses."""
        ...

class PlainPersonalSection(PlainRenderBase):
    def render(self) -> None:
        if self.settings.name:
            self.add_heading(self.personal.name, level=1)
```

---

## 7. Extension Points

### 7.1 Adding a New Output Format

1. **Create directory** `resume_render/<format>/`
2. **Copy structure** from `resume_render/basic/`
3. **Implement renderers** for each section
4. **Add tests** following `tests/render/basic/` pattern
5. **Update main.py** to accept new `--resume-type`

### 7.2 Adding a New Section

1. **Create model** in `models/<section>.py`
2. **Add to Resume** model as optional field
3. **Create parsers** for the section
4. **Add renderers** in each output format
5. **Add settings** class in `render_settings.py`
6. **Write tests** for parser and at least `basic` renderer

### 7.3 Adding New Settings

1. **Add field** to relevant settings class in `render_settings.py`
2. **Set default** value
3. **Add validation** in `__post_init__` if needed
4. **Use in renderer** to control behavior
5. **Add tests** in `tests/render_settings/`

---

## 8. Dependencies

### 8.1 Production Dependencies

| Package | Purpose |
|---------|---------|
| `python-docx` | Word document generation |
| `click` | CLI framework |
| `mistune` | Markdown parsing |
| `jinja2` | Templating |
| `nltk` | Natural language processing |
| `dateparser` | Date parsing |
| `pytz` | Timezone handling |
| `rich` | Terminal formatting |

### 8.2 Development Dependencies

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `pytest-cov` | Coverage reporting |
| `mypy` | Type checking |
| `ruff` | Linting and formatting |
| `types-pytz` | Type stubs for pytz |
| `types-dateparser` | Type stubs for dateparser |

### 8.3 Dependency Notes

- **python-docx**: No type stubs available, configured to ignore in mypy
- **nltk**: No type stubs available, configured to ignore in mypy
- **dateparser**: types-dateparser available, install for better type checking
- **pytz**: types-pytz available, install for better type checking

---

## 9. Testing Architecture

### 9.1 Test Organization

```
tests/
├── parser/              # Parser tests (high coverage)
├── render/basic/        # Basic renderer tests
├── render_settings/     # Settings tests
├── test_executive_summary.py
└── test_stats.py
```

### 9.2 Test Patterns

**Parser Tests:**
- Test valid input parsing
- Test empty/malformed input handling
- Test line number tracking
- 100% coverage requirement

**Renderer Tests:**
- Mock document object
- Verify correct methods called
- Test settings-driven behavior
- Visual verification for .docx output

### 9.3 Coverage Strategy

| Component | Target | Notes |
|-----------|--------|-------|
| Parsers | 100% | Business logic, must be fully tested |
| Models | 100% | Data integrity critical |
| Utils | 90%+ | Business logic utilities |
| Renderers | Gradual | .docx renderers require manual verification |
| main.py | TBD | CLI integration testing |

---

## 10. Configuration

### 10.1 pyproject.toml

Key configurations:
- **Ruff rules**: Extensive linting rules enabled
- **MyPy overrides**: Ignores missing stubs for third-party libs
- **Pytest**: Test discovery and coverage settings
- **Mccabe**: Max complexity set to 5

### 10.2 Settings Files

Sample settings files provided:
- `settings_nosummary_resume.toml` - No summary section
- `settings_summary_resume.toml` - Summary only
- `settings_full_resume.toml` - Full resume with summary
- `settings_ats_resume.toml` - ATS-optimized settings

---

## 11. Known Limitations

### 11.1 Current Technical Debt

1. **Test Coverage**: Many renderers at 0% coverage
2. **Type Checking**: 355 mypy errors, mostly in renderers
3. **Complexity**: Several functions exceed complexity 5
4. **Documentation**: Some modules lack comprehensive docs

### 11.2 Design Constraints

1. **Parser Strictness**: Input format is rigid, error messages could be improved
2. **Visual Testing**: .docx output requires manual visual verification
3. **Stub Limitations**: Some dependencies lack type stubs

---

## 12. Related Documents

- **CONVENTIONS.md**: Coding standards and style guidelines
- **AGENTS.md**: Project-specific guidance for AI agents
- **README.md**: User-facing documentation
- **docs/format_details.md**: Input format specification

---

**Last Updated:** 2026-03-19  
**Version:** 0.2.0  
**Branch:** opencode-convert
