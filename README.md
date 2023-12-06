# example-dbt-airflow
Example project learning dbt on MWAA and provisioning via cdk


## Quickstart

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

# TODO:
 - https://medium.com/geekculture/deploying-amazon-managed-apache-airflow-with-aws-cdk-7376205f0128