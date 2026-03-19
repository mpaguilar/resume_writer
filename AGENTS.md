# Agent Guidelines: resume-writer

## Overview

This document provides project-specific guidance for AI agents working with the resume-writer codebase. It complements `CONVENTIONS.md` (coding standards) and `ARCHITECTURE.md` (system design) by documenting how to handle existing technical debt, coverage gaps, and project-specific workflows.

**Project Context:**
- **Name:** resume-writer
- **Purpose:** Converts structured text resumes to various output formats (.docx, HTML, Markdown)
- **Status:** Production codebase undergoing incremental cleanup
- **Approach:** Conservative changes - prioritize stability over rapid refactoring

---

## 1. Agent Interaction Principles

### 1.1 Conservative Change Policy

This is an **in-production** project. When making changes:

1. **Preserve existing behavior** unless explicitly asked to change it
2. **Prefer small, incremental changes** over large refactorings
3. **Run tests frequently** - both existing tests and any new tests you add
4. **When in doubt, ask** - don't assume refactoring is desired

### 1.2 Research Before Implementation

Before modifying existing code:

1. **Read the existing implementation** - understand the current approach
2. **Check test coverage** - see if tests exist and what they verify
3. **Identify dependencies** - understand what other code depends on this
4. **Document your findings** in the requirements document

### 1.3 Code Change Checklist

For every code modification:

- [ ] Understand the current implementation and its purpose
- [ ] Run existing tests to establish baseline
- [ ] Make minimal changes to achieve the goal
- [ ] Add/update tests for new functionality
- [ ] Run full test suite: `uv run pytest tests/`
- [ ] Run ruff checks: `uv run ruff check resume_writer/`
- [ ] Run mypy checks: `uv run mypy resume_writer/`
- [ ] Verify no regressions in existing behavior

---

## 2. Testing Strategy

### 2.1 Coverage Expectations

The codebase currently has **variable test coverage**:

| Module | Current Coverage | Target |
|--------|-----------------|--------|
| `models/` (parsers) | 84-100% | 100% |
| `resume_render/basic/` | 49-91% | 100% |
| `resume_render/ats/` | 0% | TBD |
| `resume_render/plain/` | 0-82% | TBD |
| `resume_render/html/` | 0% | TBD |
| `resume_render/markdown/` | 0% | TBD |
| `main.py` | 0% | TBD |

### 2.2 Testing Priorities

**Priority 1 (Required for all new code):**
- Parser modules (`models/parsers.py`, model files)
- Utility functions with business logic
- Settings/configuration handling

**Priority 2 (Gradual improvement):**
- `resume_render/basic/` - has some tests, improve to 100%
- `main.py` CLI entry point

**Priority 3 (Lower priority / Special handling):**
- `.docx output renderers** (`ats/`, `plain/`)
  - Binary format makes automated testing difficult
  - Visual output requires manual verification
  - Focus on testing logic paths, not visual output
  - Use mocking where appropriate

### 2.3 Testing Approach for Renderers

For renderers that output .docx:

1. **Test logic paths** - verify correct branches are taken based on settings
2. **Mock the document** - verify correct methods are called with expected arguments
3. **Manual verification** - for visual changes, generate output and visually inspect
4. **Integration tests** - run full pipeline with sample data, verify no exceptions

Example pattern:
```python
def test_personal_section_renders_name():
    """Test that personal section renders name when enabled."""
    mock_doc = Mock()
    settings = RenderSettings(personal_settings=PersonalSettings(name=True))
    renderer = PersonalSection(mock_doc, personal_data, settings)
    renderer.render()
    mock_doc.add_paragraph.assert_called_with("John Doe")
```

---

## 3. Type Checking Strategy

### 3.1 MyPy Configuration

Third-party libraries without type stubs are handled via `pyproject.toml`:

```toml
[[tool.mypy.overrides]]
module = [
    "nltk",
    "nltk.*",
    "docx",
    "docx.*",
]
ignore_missing_imports = true
```

### 3.2 Agent Guidelines

When encountering mypy errors:

1. **Fix legitimate type issues** - add proper annotations, handle None cases
2. **Use type: ignore sparingly** - only for known library limitations
3. **Install stubs when available** - add to dev dependencies if types-* package exists
4. **Document complex type workarounds** - add comments explaining why

### 3.3 Priority Order for Type Issues

1. **Fix type errors in new code** - all new code must pass mypy
2. **Fix type errors in modified code** - if you touch a file, fix its type issues
3. **Address None handling** - Union[None, X] errors are usually legitimate bugs
4. **Ignore third-party issues** - already configured in pyproject.toml

---

## 4. Code Complexity Strategy

### 4.1 Current State

Several functions exceed the max complexity of 5:

| File | Function | Complexity |
|------|----------|------------|
| `main.py` | `main` | 6 |
| `models/education.py` | `__init__` | 6 |
| `models/parsers.py` | `parse` | 6-8 |
| `resume_render/ats/` | Multiple render methods | 6-9 |

### 4.2 Complexity Policy

**For existing high-complexity functions:**
- **Grandfathered** - do not refactor solely to reduce complexity
- **Mark with comments** - indicate these are legacy exceptions
- **Add tests** - ensure complex paths are covered

**For new code:**
- **Maximum complexity: 5** - no exceptions
- **Refactor early** - if approaching limit, split into smaller functions

**When modifying existing complex functions:**
- **Leave complexity as-is** if just making small changes
- **Consider refactoring** if making substantial changes (opportunity to improve)
- **Add tests** for any new branches you introduce

### 4.3 Refactoring Guidelines

When you do refactor complex functions:

1. **Extract helper functions** - each with single responsibility
2. **Preserve behavior** - all existing tests must pass
3. **Add tests for helpers** - ensure extracted functions are tested
4. **Document the change** - note complexity reduction in commit message

---

## 5. Working with Renderers

### 5.1 Renderer Structure

The project has multiple output formats:

```
resume_render/
├── basic/          # Text-based renderer (testable, has test suite)
├── ats/            # ATS-optimized .docx renderer (0% coverage)
├── plain/          # Plain .docx renderer (0-82% coverage)
├── html/           # HTML renderer (0% coverage)
└── markdown/       # Markdown renderer (0% coverage)
```

### 5.2 Adding a New Renderer

To create a new output format:

1. **Copy `basic/` folder** - it has the most complete test suite
2. **Update imports** in `resume_main.py`
3. **Update `main.py`** - add new resume-type option
4. **Write tests** - follow the `basic/` test patterns
5. **Generate sample output** - verify visually

### 5.3 Modifying Existing Renderers

When changing renderer logic:

1. **Check if tests exist** - `basic/` has tests, others may not
2. **Run existing tests** - ensure no regressions
3. **Add tests for changes** - even if module has 0% coverage, add tests for your changes
4. **Generate output** - verify visual appearance if applicable

---

## 6. Working with Parsers

### 6.1 Parser Architecture

Parsers use a `ParseContext` pattern:

```python
from resume_writer.models.parsers import ParseContext

context = ParseContext(lines, line_num)
result = SomeClass.parse(context)
```

### 6.2 Adding New Parsers

When adding new parsing functionality:

1. **Follow existing patterns** - use `ParseContext`, inherit from base classes
2. **Add comprehensive tests** - parsers must have 100% coverage
3. **Handle edge cases** - empty input, malformed data, missing fields
4. **Document expected format** - add examples in docstrings

### 6.3 Parser Testing Requirements

Parser tests must cover:

- [ ] Happy path - valid input parses correctly
- [ ] Empty input - graceful handling
- [ ] Malformed input - appropriate errors
- [ ] Partial input - missing optional fields
- [ ] Line number tracking - correct context propagation

---

## 7. Dependencies and Environment

### 7.1 Dependency Management

Use `uv` for all dependency operations:

```bash
# Add production dependency
uv add <package>

# Add development dependency
uv add --dev <package>

# Run commands
uv run pytest tests/
uv run ruff check resume_writer/
uv run mypy resume_writer/
```

### 7.2 Required Environment Variables

The application expects these environment variables:

- `LLM_API_KEY` - For LLM functionality (if used)
- `SERPER_API_KEY` - For web search functionality (if used)

### 7.3 Development Setup

```bash
# Install dependencies
uv sync

# Run tests with coverage
uv run pytest tests/ --cov=resume_writer --cov-branch --cov-report=term-missing

# Run quality checks
uv run ruff check resume_writer/
uv run mypy resume_writer/
```

---

## 8. Common Tasks

### 8.1 Adding a New Resume Output Format

1. Copy `resume_render/basic/` to `resume_render/<new_format>/`
2. Update class names and imports
3. Modify rendering logic for your format
4. Add tests following `tests/render/basic/` pattern
5. Update `main.py` to accept new `--resume-type`
6. Add settings class in `render_settings.py` if needed

### 8.2 Adding a New Model/Parser

1. Create model class in `models/`
2. Inherit from appropriate base class
3. Implement `parse()` method using `ParseContext`
4. Add comprehensive tests in `tests/parser/`
5. Update `models/__init__.py` exports

### 8.3 Modifying Settings

1. Locate relevant settings class in `render_settings.py`
2. Add new setting with type annotation and default
3. Add validation in `__post_init__` if needed
4. Update tests in `tests/render_settings/`
5. Document in settings TOML file comments

### 8.4 Fixing Quality Issues

**Ruff errors:**
```bash
# Check
uv run ruff check resume_writer/

# Auto-fix where possible
uv run ruff check resume_writer/ --fix
```

**MyPy errors:**
```bash
# Check
uv run mypy resume_writer/

# Fix legitimate type issues
# Add type: ignore[code] only for known library issues
```

**Test failures:**
```bash
# Run with debug logging
uv run pytest tests/ -v --log-cli-level=DEBUG

# Run specific test
uv run pytest tests/parser/test_parse_resume.py -v
```

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue: Tests pass individually but fail together**
- Check for shared state/mutable defaults
- Look for file system or environment side effects

**Issue: MyPy errors in unmodified files**
- May be due to missing stubs: check `pyproject.toml` overrides
- May be pre-existing issues - check if error is in your changes

**Issue: Ruff complexity errors in existing code**
- Legacy code is grandfathered - don't refactor just for this
- Mark with comment: `# Legacy: complexity exceeds limit, see AGENTS.md`

**Issue: .docx output looks wrong**
- Visual testing required - generate and inspect manually
- Check settings are being applied correctly
- Verify document structure with `python-docx` debugging

### 9.2 Getting Help

When stuck:

1. **Check existing patterns** - similar functionality likely exists
2. **Read the tests** - they document expected behavior
3. **Check ARCHITECTURE.md** - understand system design
4. **Ask specific questions** - provide context and what you've tried

---

## 10. Checklist for Agent Tasks

Before submitting work:

- [ ] Code follows CONVENTIONS.md standards
- [ ] Tests added/updated and passing
- [ ] Ruff checks pass: `uv run ruff check resume_writer/`
- [ ] MyPy checks pass (for new/modified code)
- [ ] No regressions in existing tests
- [ ] Documentation updated if needed
- [ ] Requirements document updated if applicable

---

**Last Updated:** 2026-03-19  
**Branch:** opencode-convert  
**Status:** Phase 2 complete - easy deficiencies addressed

### Phase 2 Completion Notes

The following easy deficiencies from the quality checks have been addressed:

1. **Ruff C420 errors** - Fixed unnecessary dict comprehensions in `models/parsers.py` (lines 263, 407)
2. **Ruff FBT001 errors** - Made boolean parameters keyword-only in:
   - `models/personal.py` - `require_sponsorship` parameter
   - `resume_render/render_settings.py` - all `default_init` parameters
   - `resume_render/resume_render_base.py` - `bold` and `italic` parameters in `add_hyperlink()`
3. **Type annotations** - Added missing type annotations to:
   - `utils/text_doc.py` - instance variables
   - `utils/skills_matrix.py` - `_skills_matrix` variable
   - `utils/skills_splitter.py` - `_current_fragment` variable
   - `utils/markdown_parser.py` - `line` parameter
   - `utils/skills_splitter_revamped.py` - return type for `download_nltk_data()`
4. **Type stub packages** - Added `types-pytz` and `types-dateparser` to dev dependencies
5. **Test coverage** - Improved coverage for `resume_render/basic/` modules:
   - `education_section.py`: 83% → 100%
   - `executive_summary_section.py`: 49% → 100%
   - `experience_section.py`: 82% → 93%
   - `personal_section.py`: 82% → 100%

**Test Results:** 117 tests passing, no regressions
**Ruff Status:** All non-complexity violations resolved (complexity violations grandfathered per policy)
