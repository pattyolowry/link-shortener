# Ref: https://fastapi.tiangolo.com/deployment/docker/
# Ref: https://docs.astral.sh/uv/guides/integration/docker/

# Install python image and uv
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.11.5 /uv /uvx /bin/

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Change the working directory to the `app` directory
WORKDIR /app

# Activate the project virtual env
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["fastapi", "run", "app/main.py", "--port", "80"]