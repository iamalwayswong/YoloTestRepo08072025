"""
Example custom handlers for GitHub pull request webhooks.

This file demonstrates how to extend the webhook listener with custom logic
for different pull request events. Copy and modify these functions as needed.
"""

import requests
import json
from typing import Dict, Any


def send_slack_notification(webhook_url: str, message: str) -> None:
    """Send a notification to Slack using a webhook URL."""
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Slack notification sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack notification: {e}")


def send_discord_notification(webhook_url: str, message: str) -> None:
    """Send a notification to Discord using a webhook URL."""
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Discord notification sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord notification: {e}")


def create_jira_ticket(pr_data: Dict[str, Any]) -> None:
    """Create a Jira ticket for a pull request (example implementation)."""
    # This is a placeholder - implement based on your Jira API
    pr = pr_data['pull_request']
    repo = pr_data['repository']
    
    ticket_data = {
        "fields": {
            "project": {"key": "PROJ"},
            "summary": f"Review PR: {pr['title']}",
            "description": f"Pull Request: {pr['html_url']}\nRepository: {repo['full_name']}",
            "issuetype": {"name": "Task"}
        }
    }
    
    print(f"Would create Jira ticket for PR: {pr['title']}")
    # Implement actual Jira API call here


def handle_pull_request_opened_custom(payload: Dict[str, Any]) -> None:
    """Custom handler for when a pull request is opened."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    # Example: Send Slack notification
    slack_message = f"🚀 New PR opened: #{pr['number']} - {pr['title']}\n"
    slack_message += f"Repository: {repo['full_name']}\n"
    slack_message += f"Author: {sender['login']}\n"
    slack_message += f"URL: {pr['html_url']}"
    
    # Uncomment and configure your Slack webhook URL
    # send_slack_notification("YOUR_SLACK_WEBHOOK_URL", slack_message)
    
    # Example: Create Jira ticket
    # create_jira_ticket(payload)
    
    # Example: Log to file
    with open("pr_events.log", "a") as f:
        f.write(f"PR Opened: {pr['number']} - {pr['title']} by {sender['login']}\n")
    
    print(f"Custom handler: New PR opened: #{pr['number']} - {pr['title']}")


def handle_pull_request_merged_custom(payload: Dict[str, Any]) -> None:
    """Custom handler for when a pull request is merged."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    # Example: Send Discord notification
    discord_message = f"✅ PR merged: #{pr['number']} - {pr['title']}\n"
    discord_message += f"Repository: {repo['full_name']}\n"
    discord_message += f"Merged by: {sender['login']}"
    
    # Uncomment and configure your Discord webhook URL
    # send_discord_notification("YOUR_DISCORD_WEBHOOK_URL", discord_message)
    
    # Example: Trigger deployment
    # trigger_deployment(repo['full_name'], pr['base']['ref'])
    
    print(f"Custom handler: PR merged: #{pr['number']} - {pr['title']}")


def handle_pull_request_review_requested_custom(payload: Dict[str, Any]) -> None:
    """Custom handler for when a pull request review is requested."""
    pr = payload['pull_request']
    repo = payload['repository']
    requested_reviewer = payload.get('requested_reviewer')
    requested_team = payload.get('requested_team')
    
    # Example: Send notification to specific reviewer
    if requested_reviewer:
        message = f"👀 Review requested for PR: #{pr['number']} - {pr['title']}\n"
        message += f"Repository: {repo['full_name']}\n"
        message += f"URL: {pr['html_url']}"
        
        # Send notification to reviewer (implement based on your notification system)
        print(f"Notify {requested_reviewer['login']}: {message}")
    
    print(f"Custom handler: Review requested for PR: #{pr['number']}")


def trigger_deployment(repo_name: str, branch: str) -> None:
    """Trigger a deployment for a specific repository and branch."""
    # Example: Trigger GitHub Actions workflow
    # This would require GitHub API authentication
    print(f"Would trigger deployment for {repo_name} on branch {branch}")


def update_project_management_tool(pr_data: Dict[str, Any]) -> None:
    """Update a project management tool with PR information."""
    pr = pr_data['pull_request']
    
    # Example: Update Asana, Trello, or other PM tools
    # This would require API integration with your chosen tool
    print(f"Would update PM tool with PR: {pr['title']}")


# Example of how to integrate these custom handlers into the main webhook listener
def integrate_custom_handlers():
    """
    Example of how to integrate custom handlers into the main webhook listener.
    
    In your main github_webhook_listener.py file, you would replace the default
    handlers with these custom ones:
    
    from example_handlers import (
        handle_pull_request_opened_custom,
        handle_pull_request_merged_custom,
        handle_pull_request_review_requested_custom
    )
    
    # Then in your webhook() function:
    if action == 'opened':
        handle_pull_request_opened_custom(data)
    elif action == 'merged':
        handle_pull_request_merged_custom(data)
    elif action == 'review_requested':
        handle_pull_request_review_requested_custom(data)
    """
    pass
