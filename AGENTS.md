# Agents

Zipline CLI, a Python 3 CLI File Uploader for [Diced/Zipline](https://github.com/diced/zipline) v3/v4 Upload Server.

- Zipline: https://zipline.diced.sh/

## Structure

- [src/zipline](src/zipline) - Package
  - `cli.py` - Typer CLI (entry point `zipline.cli:app`)
  - `zipline.py` - Upload API client (`Zipline`, `ZipURL`) and MIME type detection from magic bytes
  - `_utils.py` - Helpers (config file lookup, random names, human file sizes)
  - `_version.py` - Version from `GITHUB_REF_NAME` env, falls back to `0.0.1`
  - `__init__.py`, `py.typed`
- [tests](tests) - CI helper scripts that fetch tokens (`get_token_v3.py`, `get_token_v4.py`)
- [docs](docs) - Zensical (MkDocs fork), see `zensical.toml`
- [files](files) - Sample files for manual upload testing
- [.github/workflows](.github/workflows) - build, lint, test, release, docs, dev, issue, labeler
- [pyproject.toml](pyproject.toml) - Project config and `[tool.scripts]`

## Environment

- Use the `venv` at the repo root (Python 3.13). Activate with `.\venv\Scripts\activate`.
- Install dev dependencies with `python -m pip install --group dev` (pip >= 25.1).
- Global tools on PATH (not in the dev group): `zensical`, `yamllint`.
- `run` (from `toml-run`) is part of the dev group. Re-run `python -m pip install --group dev` after editing the group to pick up new members.

## Commands

Scripts are run via [toml-run](https://github.com/cssnr/toml-run) from [pyproject.toml](pyproject.toml):

| Command      | What it does                                  |
| ------------ | --------------------------------------------- |
| `run build`  | `python -m build` (wheel + sdist to `dist/`)  |
| `run format` | Full format: always run before finishing work |
| `run lint`   | Full lint: always run before finishing work   |

Sub-scripts (also runnable individually): `bandit`, `mypy`, `ruff`, `validate` (validate-pyproject), `yamllint`. Add `-v` for verbose output (e.g. `run lint -v`).

## Runtime Config

- The CLI reads `~/.zipline` for defaults (see `.zipline.example`).
- Env vars: `ZIPLINE_URL`, `ZIPLINE_TOKEN`, `ZIPLINE_FORMAT`, `ZIPLINE_VERBOSE`, `ZIPLINE_EMBED`, `ZIPLINE_EXPIRE`.

## Notes

- Testing against a live server requires Docker (`test.yaml` runs `diced/zipline` v3/v4 + postgres). Docker only runs on the remote server: give the user the exact `docker` commands to run and wait for their output.
- `zipline.zipline.get_type` detects MIME from magic bytes; use the samples in `files/` to test uploads.
