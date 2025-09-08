#!/usr/bin/env python3
"""
GitHub Pull Request Webhook Listener

This Flask application listens for GitHub webhook events, specifically pull request events.
It verifies webhook signatures for security and provides handlers for different PR actions.

Based on: https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request
"""

import hmac
import hashlib
import json
import logging
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
from config import WEBHOOK_SECRET, PORT, HOST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify the GitHub webhook signature to ensure the request is authentic.
    
    Args:
        payload: The raw request payload
        signature: The X-Hub-Signature-256 header value
        secret: The webhook secret configured in GitHub
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    if not signature or not secret:
        logger.warning("Missing signature or secret")
        return False
    
    # GitHub sends signature as "sha256=<hash>"
    if not signature.startswith('sha256='):
        logger.warning("Invalid signature format")
        return False
    
    expected_signature = signature[7:]  # Remove 'sha256=' prefix
    
    # Calculate expected signature
    calculated_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(expected_signature, calculated_signature)


def handle_pull_request_opened(payload: Dict[str, Any]) -> None:
    """Handle when a pull request is opened."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    logger.info(f"New PR opened: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    logger.info(f"Author: {sender['login']}")
    logger.info(f"URL: {pr['html_url']}")
    
    # Add your custom logic here
    # For example: send notifications, create tasks, etc.


def handle_pull_request_closed(payload: Dict[str, Any]) -> None:
    """Handle when a pull request is closed."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    logger.info(f"PR closed: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    logger.info(f"Closed by: {sender['login']}")
    logger.info(f"Merged: {pr['merged']}")
    
    # Add your custom logic here


def handle_pull_request_merged(payload: Dict[str, Any]) -> None:
    """Handle when a pull request is merged."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    logger.info(f"PR merged: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    logger.info(f"Merged by: {sender['login']}")
    logger.info(f"Merge commit: {pr['merge_commit_sha']}")
    
    # Add your custom logic here


def handle_pull_request_review_requested(payload: Dict[str, Any]) -> None:
    """Handle when a pull request review is requested."""
    pr = payload['pull_request']
    repo = payload['repository']
    requested_reviewer = payload.get('requested_reviewer')
    requested_team = payload.get('requested_team')
    
    logger.info(f"Review requested for PR: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    
    if requested_reviewer:
        logger.info(f"Requested reviewer: {requested_reviewer['login']}")
    if requested_team:
        logger.info(f"Requested team: {requested_team['name']}")
    
    # Add your custom logic here


def handle_pull_request_review_submitted(payload: Dict[str, Any]) -> None:
    """Handle when a pull request review is submitted."""
    pr = payload['pull_request']
    repo = payload['repository']
    review = payload['review']
    sender = payload['sender']
    
    logger.info(f"Review submitted for PR: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    logger.info(f"Reviewer: {sender['login']}")
    logger.info(f"Review state: {review['state']}")
    
    if review.get('body'):
        logger.info(f"Review comment: {review['body']}")
    
    # Add your custom logic here


def handle_pull_request_synchronize(payload: Dict[str, Any]) -> None:
    """Handle when a pull request is updated (new commits pushed)."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    logger.info(f"PR updated: #{pr['number']} - {pr['title']}")
    logger.info(f"Repository: {repo['full_name']}")
    logger.info(f"Updated by: {sender['login']}")
    logger.info(f"New commit: {pr['head']['sha']}")
    
    # Add your custom logic here


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint that receives GitHub webhook events.
    """
    try:
        # Get the raw payload
        payload = request.get_data()
        
        # Get the signature from headers
        signature = request.headers.get('X-Hub-Signature-256')
        
        # Verify the webhook signature
        if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
            logger.warning("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse the JSON payload
        data = json.loads(payload.decode('utf-8'))
        
        # Get the event type
        event_type = request.headers.get('X-GitHub-Event')
        
        # Handle pull request events
        if event_type == 'pull_request':
            action = data.get('action')
            logger.info(f"Received pull_request event: {action}")
            
            # Route to appropriate handler based on action
            if action == 'opened':
                handle_pull_request_opened(data)
            elif action == 'closed':
                handle_pull_request_closed(data)
            elif action == 'merged':
                handle_pull_request_merged(data)
            elif action == 'review_requested':
                handle_pull_request_review_requested(data)
            elif action == 'submitted':
                handle_pull_request_review_submitted(data)
            elif action == 'synchronize':
                handle_pull_request_synchronize(data)
            else:
                logger.info(f"Unhandled pull request action: {action}")
        
        # Handle other event types if needed
        elif event_type == 'ping':
            logger.info("Received ping event from GitHub")
            return jsonify({'message': 'Pong'}), 200
        
        else:
            logger.info(f"Unhandled event type: {event_type}")
        
        return jsonify({'message': 'Webhook received successfully'}), 200
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with basic information."""
    return jsonify({
        'message': 'GitHub Webhook Listener',
        'endpoints': {
            'webhook': '/webhook',
            'health': '/health'
        },
        'supported_events': ['pull_request', 'ping']
    }), 200


if __name__ == '__main__':
    logger.info(f"Starting GitHub webhook listener on {HOST}:{PORT}")
    logger.info(f"Webhook endpoint: http://{HOST}:{PORT}/webhook")
    logger.info("Make sure to set WEBHOOK_SECRET environment variable")
    
    app.run(host=HOST, port=PORT, debug=False)
