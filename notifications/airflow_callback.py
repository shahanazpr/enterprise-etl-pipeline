from notifications.email_alert import send_email
from notifications.slack_alert import send_slack_message


def notify_failure(context):
    """
    Airflow callback executed whenever a task fails.
    """

    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["execution_date"]
    exception = context.get("exception")

    message = f"""
ETL Pipeline Failure

DAG: {dag_id}
Task: {task_id}
Execution Time: {execution_date}

Error:
{exception}
"""

    # Email Alert
    send_email(
        subject=f"[FAILED] {dag_id}",
        body=message,
        receiver="admin@example.com"
    )

    # Slack Alert
    send_slack_message(
        message=message,
        webhook_url="YOUR_SLACK_WEBHOOK_URL"
    )