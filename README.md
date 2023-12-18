# Example DBT Airflow
Example project learning dbt on MWAA and provisioning via cdk.
Also including local development workflows.

## Table of Contents

<!--TOC-->

- [Example DBT Airflow](#example-dbt-airflow)
  - [Table of Contents](#table-of-contents)
- [Quickstart Local Development](#quickstart-local-development)
  - [Local Interactive Instances](#local-interactive-instances)
  - [Pytest Fixtures Using TestContainers](#pytest-fixtures-using-testcontainers)
    - [`tests/conftest.py`](#testsconftestpy)
    - [`tests/test_airflow_local.py`](#teststest_airflow_localpy)
  - [Quickstart MWAA (AWS CDK)](#quickstart-mwaa-aws-cdk)
- [User Guide](#user-guide)
  - [Project Structure](#project-structure)
  - [Architecture](#architecture)
- [Development Guide](#development-guide)
- [Publishing](#publishing)
- [Contributing](#contributing)
- [TODO](#todo)
  - [Nice to Haves](#nice-to-haves)

<!--TOC-->

# Quickstart Local Development

[Data with Marc: Running Airflow 2.0 with Docker in 5 mins](https://www.youtube.com/watch?v=aTaytcxy2Ck)

> **WARNING: `docker compose` will pull ~ 3Gb of docker images on first run.**

## Local Interactive Instances

```sh
poetry run inv up
# Open https://localhost:8080
# Username: airflow
# Password: airflow
# Ctrl-C to stop the stack
```

And tidy up once you're done.

```sh
poetry run inv down
# OR This version will run docker system prune which removes
# dangling containers / images / volumes / networks / build cache
poetry run inv down --full
```

## Pytest Fixtures Using TestContainers

```sh
poetry run invoke test
```

For extra context there is a test fixture available for the duration of the entire pytest `session` when you have the following in your `conftest.py`.

### `tests/conftest.py`
```python
# Third Party
import pytest
from testcontainers.compose import DockerCompose

@pytest.fixture(name="dockercompose", scope="session")
def _docker_compose():
    with DockerCompose(filepath="containers/docker/", compose_file_name="docker-compose.airflow.yml", pull=True, build=True) as compose:
        compose.wait_for("http://localhost:8080/")
        yield compose

```

And here is an example test using it:

### `tests/test_airflow_local.py`
```python
# Third Party
import pytest
import aiohttp
import base64

HOST = "http://localhost:8080/api/v1/dags"
BASIC_AUTH = base64.b64encode("airflow:airflow".encode()).decode()

headers={"Authorization": f"Basic {BASIC_AUTH}"}


@pytest.mark.asyncio
@pytest.mark.docker
async def test_airflow_local(dockercompose) -> None:
    """Start docker compose fixture and run dbcheck endpoint."""
    print(headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST, headers=headers) as response:
            data = await response.json()
    
    assert "dags" in data.keys()
    assert len(data["dags"]) > 0
```

## Quickstart MWAA (AWS CDK)

> **🚧 WORK IN PROGRESS 🚧**

```sh
npm install -g aws-cdk
cdk bootstrap aws://YOUR_ACCOUNT_ID/YOUR_REGION
poetry install
```

```sh
cd cdk 
. ./.venv/bin/activate
pyhton3 -m pip install -r requirements.txt
cdk synth
cdk deploy -c vpcId=<YOUR_VPC_ID>
```
---
# User Guide

## Project Structure

TODO: @neozenith

## Architecture

TODO: Produce diagram for deployed cloud infrastructure

----

# Development Guide

These are purely notes for the repo author / maintainers.

 - The CDK directory nesting at the moment is causing issues so not commiting it as yet until further reading completed.

---



# Publishing

To publish a new version create a release from `main` (after pull request).

# Contributing

At all times, you have the power to fork this project, make changes as you see fit and then:

```sh
pip install https://github.com/user/repository/archive/branch.zip
```
[Stackoverflow: pip install from github branch](https://stackoverflow.com/a/24811490/622276)

That way you can run from your own custom fork in the interim or even in-house your work and simply use this project as a starting point. That is totally ok.

However if you would like to contribute your changes back, then open a Pull Request "across forks".

Once your changes are merged and published you can revert to the canonical version of `pip install`ing this package.

If you're not sure how to make changes or _if_ you should sink the time and effort, then open an Issue instead and we can have a chat to triage the issue.


# TODO

- Local testing of DBT project

  - DBT Core on ECS Fargate
   - https://data-dive.com/deploy-dbt-on-aws-using-ecs-fargate-with-airflow-scheduling/
   
 - AWS Fargate + SQS
   - Figure out how to get a Fargate autoscaling cluster to scale to zero based on SQS depth.
   - Figure out how to trash an MWAA deployment on Fargate safely when scaling to zero
   - Get MWAA to scale up from zero when SQS depth > 0.
   
 - CDK + MWAA
   - https://medium.com/geekculture/deploying-amazon-managed-apache-airflow-with-aws-cdk-7376205f0128

- DBT
 
 - DBT Docs Secure publishing
   - S3 Static Site hosting https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html
   - Authorization@Edge https://aws.amazon.com/blogs/networking-and-content-delivery/authorizationedge-how-to-use-lambdaedge-and-json-web-tokens-to-enhance-web-application-security/
   - https://github.com/aws-samples/cloudfront-authorization-at-edge
   - - dbt_checkpoint for documenbtation enforcement https://github.com/dbt-checkpoint/dbt-checkpoint


 - DBT QA
   - Add elementary to the dbt package? https://docs.elementary-data.com/oss/quickstart/quickstart-cli-package
   - Add project evaluator https://hub.getdbt.com/dbt-labs/dbt_project_evaluator/latest/
   - Add dbt_utils generic tests https://github.com/dbt-labs/dbt-utils
   - Add dbt_audit_helper for comparing relations https://hub.getdbt.com/dbt-labs/audit_helper/latest/
   
   - sqlfluff precommit config https://blog.montrealanalytics.com/automating-dbt-development-workflows-with-pre-commit-b6c7ca708f7
   - Add support for external tables: https://hub.getdbt.com/dbt-labs/dbt_external_tables/latest/
   - Add support for these generic tests https://hub.getdbt.com/calogica/dbt_expectations/latest/

## Nice to Haves
- Use Metabase
  - https://github.com/gouline/dbt-metabase
  
- VSCode for Web in a Container on ECS
     - https://www.youtube.com/watch?v=Z5meMS-s9uk
     - https://hub.docker.com/r/ruanbekker/vscode-server/
     - https://blog.ruanbekker.com/blog/2019/09/14/running-vs-code-in-your-browser-with-docker/
   - VSCode container should be able to git clone a dbt project to make a cheap dbt-cloud-like IDE experience.
