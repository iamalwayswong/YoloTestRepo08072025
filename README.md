# GitHub Pull Request Webhook Listener

A Python Flask application that listens for GitHub webhook events, specifically pull request events. This webhook listener verifies webhook signatures for security and provides handlers for different PR actions.

Based on the [GitHub Webhook Events and Payloads documentation](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request).

## Features

- ✅ **Secure**: Verifies GitHub webhook signatures using HMAC-SHA256
- ✅ **Comprehensive**: Handles all major pull request events
- ✅ **Extensible**: Easy to add custom logic for different PR actions
- ✅ **Production Ready**: Includes health checks and proper error handling
- ✅ **Well Documented**: Clear code structure and comprehensive logging

## Supported Events

The webhook listener handles the following pull request events:

- `opened` - When a new pull request is created
- `closed` - When a pull request is closed
- `merged` - When a pull request is merged
- `review_requested` - When a review is requested
- `submitted` - When a review is submitted
- `synchronize` - When new commits are pushed to the PR

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd github-webhook-listener
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export WEBHOOK_SECRET="your_github_webhook_secret"
   export HOST="0.0.0.0"
   export PORT="5000"
   ```

   Or create a `.env` file:
   ```
   WEBHOOK_SECRET=your_github_webhook_secret
   HOST=0.0.0.0
   PORT=5000
   ```

## Usage

### Running the Server

```bash
python github_webhook_listener.py
```

The server will start on `http://0.0.0.0:5000` by default.

### Endpoints

- `GET /` - Home endpoint with basic information
- `POST /webhook` - Main webhook endpoint for GitHub events
- `GET /health` - Health check endpoint

### Testing the Webhook

You can test the webhook using curl:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test webhook endpoint (this will fail signature verification without proper headers)
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## GitHub Webhook Setup

1. **Go to your GitHub repository settings**
2. **Navigate to Webhooks section**
3. **Click "Add webhook"**
4. **Configure the webhook:**
   - **Payload URL**: `http://your-server.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Set a strong secret (use the same value as `WEBHOOK_SECRET`)
   - **Events**: Select "Pull requests" or "Let me select individual events"
   - **Active**: Check this box

5. **Click "Add webhook"**

## Customization

### Adding Custom Logic

You can customize the behavior by modifying the handler functions in `github_webhook_listener.py`:

```python
def handle_pull_request_opened(payload: Dict[str, Any]) -> None:
    """Handle when a pull request is opened."""
    pr = payload['pull_request']
    repo = payload['repository']
    sender = payload['sender']
    
    # Your custom logic here
    # Examples:
    # - Send notifications to Slack/Discord
    # - Create Jira tickets
    # - Trigger CI/CD pipelines
    # - Update project management tools
    pass
```

### Available Payload Data

The webhook payload contains rich information about the pull request event. Key fields include:

- `pull_request` - Complete PR object with title, body, author, etc.
- `repository` - Repository information
- `sender` - User who triggered the event
- `action` - The specific action that occurred

For complete payload structure, see the [GitHub webhook documentation](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request).

## Security

- **Signature Verification**: All webhook requests are verified using HMAC-SHA256
- **Secret Management**: Use environment variables for sensitive configuration
- **Error Handling**: Proper error responses and logging

## Production Deployment

### Using a WSGI Server

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 github_webhook_listener:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "github_webhook_listener.py"]
```

Build and run:

```bash
docker build -t github-webhook-listener .
docker run -p 5000:5000 -e WEBHOOK_SECRET=your_secret github-webhook-listener
```

### Using a Reverse Proxy

For production, use nginx or Apache as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /webhook {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Common Issues

1. **Signature verification fails**
   - Ensure `WEBHOOK_SECRET` matches the secret configured in GitHub
   - Check that the webhook is sending the correct signature header

2. **Webhook not receiving events**
   - Verify the webhook URL is accessible from the internet
   - Check GitHub webhook delivery logs for error details
   - Ensure the webhook is active and subscribed to the correct events

3. **Server not starting**
   - Check if the port is already in use
   - Verify all dependencies are installed
   - Check the logs for error messages

### Debugging

Enable debug logging by setting the log level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
