"""
Configuration file for the GitHub webhook listener.
Set these values as environment variables or modify them directly.
"""

import os

# GitHub Webhook Configuration
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your_webhook_secret_here')

# Server Configuration  
HOST = os.getenv('HOST', '127.0.0.1')  # Default to localhost for security
PORT = int(os.getenv('PORT', '5000'))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
