# Voltage Park SDK

**Documentation**: [https://AlignmentResearch.github.io/voltage-park-sdk](https://AlignmentResearch.github.io/voltage-park-sdk)

**Source Code**: [https://github.com/AlignmentResearch/voltage-park-sdk](https://github.com/AlignmentResearch/voltage-park-sdk)

---

Python library for accessing the Voltage Park API.

## Development

This package uses [`uv`](https://docs.astral.sh/uv) to manage its toolchain.
Once you have `uv` installed, to get setup you simply need to:

* Clone this repository
* Run `uv sync` which will build a virtual environment and install all the
  requirements.

### Testing

This package uses [`pytest`](https://docs.pytest.org/en/stable/) for building
and running test-suites. To launch tests, run:

```sh
uv run pytest tests/
```

from the repository root.

### Documentation

This package uses [`mkdocs`](https://www.mkdocs.org) and
[mkdocs Material](https://squidfunk.github.io/mkdocs-material/) to build
documentation. The documentation is automatically generated from the content
of the `docs` directory and from the docstrings of the public signatures of the
source code.

To develop documentation locally, you can can run

```sh
uv run mkdocs serve
```

from the repository root. This will host the built docs locally so you can
view them in your browser. They will live update as you edit the markdown
files in the `docs/` subdirectory.

### Linting, type-checking, and pre-commit

This package uses [`ruff`](https://docs.astral.sh/ruff/) as an auto-formatter
and linter and [`mypy`](https://mypy-lang.org/) for type-checking and
enforcement. You can run these commands directly with `uv run ruff` or
`uv run mypy`, respectively, however, we prefer to bundle the entire toolchain
into [`pre-commit`](https://pre-commit.com/) hooks.

`pre-commit` is configured in the `.pre-commit-config.yaml` in the repository
root and allows us to run the entire quality toolchain (linting, formatting,
type-checking, testing) at once with

```sh
uv run pre-commit run --all-files
```

Additionally, you should run

```sh
uv run pre-commit install
```

when you set up your development environment for this package. This will
invoke `pre-commit` every time you try to make a `git` commit to ensure
your changeset meets all our quality standards.

If the pre-commit hooks take a while to run or you like to run parts of
the toolchain independently, you can alternatively set up your hooks with

```sh
pre-commit install -t pre-push
```

which will cause `pre-commit` to only be invoked on push. Note that this
means that you may have commits in your git history that do not pass quality
checks.
