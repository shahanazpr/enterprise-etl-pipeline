from notifications.email_alert import send_email
from notifications.slack_alert import send_slack_message


def notify_failure(context):
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

    try:
        send_email(
            subject=f"[FAILED] {dag_id}",
            body=message,
            receiver=None,
        )
    except Exception as e:
        print(f"Email notification error: {e}")

    try:
        send_slack_message(message)
    except Exception as e:
        print(f"Slack notification error: {e}")