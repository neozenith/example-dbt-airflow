# Standard Library
import platform
from pathlib import Path
from textwrap import dedent

# Third Party
import tomlkit
from invoke import Context, run, task

git_repo_root = Path(run("git rev-parse --show-toplevel", hide=True).stdout.strip())
pyproject = tomlkit.parse((git_repo_root / "pyproject.toml").read_text())
version = pyproject["tool"]["poetry"]["version"]
image_name = pyproject["tool"]["poetry"]["name"]
image_tag_latest = f"{image_name}:latest"
image_tag_versioned = f"{image_name}:{version}"
registry_name = None  # Update this to enable container uploads

compose_path = Path("containers/docker")
compose_file = compose_path / "docker-compose.airflow.yml"


@task
def tidy(c: Context) -> None:
    """Format, and sort imports."""
    c.run("md_toc --in-place github --header-levels 4 README.md", pty=True)

    c.run("ruff format .", pty=True)
    c.run("isort .", pty=True)
    c.run("ruff . --fix", pty=True)


@task
def lint(c: Context) -> None:
    """Check for linting errors."""
    c.run("ruff check .", pty=True)
    # c.run("ruff check . --unsafe-fixes", pty=True)


@task
def typecheck(c: Context) -> None:
    """Typechecking"""
    c.run("mypy .", pty=True)


@task
def test(c: Context) -> None:
    """Run test suite."""
    c.run("python3 -m pytest", pty=True)


@task
def docs(c: Context) -> None:
    """Generate documentation."""
    c.run("mkdocs build", pty=True)


@task
def docker_build(c: Context) -> None:
    """Run commands to build the docker image."""
    c.run(
        f"docker build --no-cache --file {compose_path / 'Dockerfile'} --tag {image_tag_latest} --tag {image_tag_versioned} ."  # noqa: E501
    )


@task(pre=[docker_build])
def docker_upload(c: Context) -> None:
    """Run commands to build the docker image and publish to container registry."""
    if registry_name:
        c.run(f"docker push {registry_name}/{image_tag_versioned}")


@task
def init_env_file(c: Context, overwrite: bool = False) -> None:
    """Initialise Docker Environment file."""
    env_path = compose_path / ".env"

    if not env_path.exists() or overwrite:
        UID = 50000
        if platform.system() == "Darwin":
            UID = c.run("id -u", hide=True).stdout.strip()  # Get UID of current user on macOS so that

        env_script = dedent(
            f"""
            # Created by:
            #   poetry run inv init-env-file
            #
            # See tasks.py:init_env_file for details.
            #
            # Need to set the UID as the local user UID so that local files 
            # that get mapped into containers read/write correctly
            # https://youtu.be/aTaytcxy2Ck?si=o0wrvmQu0WGVj8kT&t=323
            #
            AIRFLOW_UID={UID}
            AIRFLOW_GID=0
            AIRFLOW_PROJ_DIR=../../airflow
        """
        ).strip()
        print(env_script)
        env_path.write_text(env_script)


@task(pre=[init_env_file])
def up(c: Context) -> None:
    """Docker compose up."""
    c.run(f"docker compose -f {compose_file} up airflow-init", pty=True)
    c.run(f"docker compose -f {compose_file} up", pty=True)


@task
def down(c: Context, full: bool = False) -> None:
    """Docker compose down.

    Enable the --full flag for a thorough tear down.
    """
    full_flags = "--volumes" if full else ""
    c.run(f"docker compose -f {compose_file} down {full_flags}", pty=True)
    if full:
        c.run("docker system prune --all --force --volumes", pty=True)


@task(
    pre=[
        tidy,
        lint,
        test,
        # typecheck, # Typechecking not working at the moment, too much to resolve.
        docs,
    ]
)
def ci(c: Context) -> None:
    """Run through basic Continuous Integration tasks."""
    ...


@task(pre=[ci, docker_build, docker_upload])
def cicd(c: Context) -> None:
    """Run through basic Continuous Integration and Continuous Deployment tasks."""
    ...
