# Third Party
from invoke import task


@task
def tidy(c):
    """Format, and sort imports."""
    c.run("ruff format .", pty=True)
    c.run("ruff . --fix", pty=True)
    c.run("isort .", pty=True)
    c.run("md_toc --in-place github --header-levels 4 README.md", pty=True)


@task
def lint(c):
    """Check for linting errors."""
    c.run("ruff check .", pty=True)
    c.run("ruff check . --unsafe-fixes", pty=True)


@task
def typecheck(c):
    """Typechecking"""
    c.run("mypy .", pty=True)


@task
def test(c):
    """Run test suite."""
    c.run("python3 -m pytest", pty=True)

@task
def docs(c):
    """Generate documentation."""
    c.run("mkdocs build", pty=True)

@task(pre=[tidy, lint, test, typecheck, docs])
def ci(c):
    """Run through basic Continuous Integration tasks."""
    ...