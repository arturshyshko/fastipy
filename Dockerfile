# Combined techniques from:
# https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
# https://hynek.me/articles/docker-uv/
# https://pdm-project.org/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile
############### BUILDER
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app

ARG UV_INSTALL_ARGS="" # Pass --no-dev for prod image
ENV UV_INSTALL_ARGS=${UV_INSTALL_ARGS}

# Only install deps (layers caching).
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project $UV_INSTALL_ARGS

############### APP
FROM python:3.13-slim-bookworm
RUN useradd --create-home --shell /bin/bash worker
USER worker
WORKDIR /app/src

COPY --from=builder --chown=worker:worker /app /app
COPY ./src /app/src

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/.venv/bin"
ENV PYTHONFAULTHANDLER=1

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
