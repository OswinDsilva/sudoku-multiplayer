FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

EXPOSE 8000

WORKDIR /usr/src/app

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --no-install-project

COPY src/ ./src/

RUN uv sync

CMD ["uv", "run", "uvicorn", "src.sudoku.main:app", "--host", "0.0.0.0"]
