from datetime import timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.models.baseoperator import chain
from airflow.models.dag import DAG
from airflow.providers.amazon.aws.operators.emr import (
    EmrAddStepsOperator,
    EmrCreateJobFlowOperator,
    EmrModifyClusterOperator,
    EmrTerminateJobFlowOperator,
)
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor, EmrStepSensor

from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

# EMR 클러스터 설정
JOB_FLOW_OVERRIDES = {
    "Name": "PiCalculationClusterExample",
    "ReleaseLabel": "emr-6.15.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}, {"Name": "Hive"}, {"Name": "Livy"}, {"Name": "Zeppelin"}],
    "Configurations": [
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {"PYSPARK_PYTHON": "/usr/bin/python3"},
                }
            ],


        }, 
             {
                "Classification": "hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                }
            },
            {
                "Classification": "spark-hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                }
            }       
    ],
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master node",
                "Market": "ON_DEMAND",
                "InstanceRole": "MASTER",
                "InstanceType": "r7g.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Worker nodes",
                "Market": "SPOT",
                "InstanceRole": "CORE",
                "InstanceType": "r7g.xlarge",
                "InstanceCount": 1,
            },
            {
                'Name': 'slave',
                'Market': 'SPOT',
                'InstanceRole': 'TASK',
                'InstanceType': 'r7g.xlarge',
                'InstanceCount': 2
            }           
        ],
        "KeepJobFlowAliveWhenNoSteps": False,
        "TerminationProtected": False,
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
    'VisibleToAllUsers': True,
    'Tags': [
        {
            'Key': 'Team',
            'Value': 'MLOps'
        },
        {
            'Key': 'Name',
            'Value': 'MLOPS Test Cluster'
        },
        {
            'Key': 'Owner',
            'Value': 'MLOPS Team'
        }
    ]    
}

# Spark를 이용한 Pi 계산 스텝 정의
SPARK_STEP = [
    {
        "Name": "CalculatePi",
        "ActionOnFailure": "TERMINATE_CLUSTER",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "cluster",
                "--class",
                "org.apache.spark.examples.SparkPi",
                "/usr/lib/spark/examples/jars/spark-examples.jar",
                "10",
            ],
        },
    }
]

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    "emr_job_flow_auto_terminate_dag",
    default_args=default_args,
    description="A DAG that creates an EMR cluster, adds a step, and then terminates the cluster",
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    start = DummyOperator(task_id="start")
    
    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id="create_emr_cluster",
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id="aws_default",
        region_name="ap-northeast-2",
    )
    

    
    add_steps = EmrAddStepsOperator(
        task_id="add_steps",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
        steps=SPARK_STEP,
    )
    
    step_checker = EmrStepSensor(
        task_id="watch_step",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_steps', key='return_value')[0] }}",
        aws_conn_id="aws_default",
    )
    
    # EMR 클러스터 종료
    terminate_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate_cluster",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
    )
    
    end = DummyOperator(task_id="end")
    
    start >> create_emr_cluster >> add_steps >> step_checker >> end
