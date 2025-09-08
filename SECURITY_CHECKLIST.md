# Security Checklist for GitHub Webhook Listener

## ✅ Fixed Issues
- [x] **Removed hardcoded secrets** - Now uses config.py properly
- [x] **Disabled debug mode** - Set to `debug=False` for production
- [x] **Default to localhost** - Changed from `0.0.0.0` to `127.0.0.1`

## 🔒 Before Going Live - Required Actions

### 1. Set Environment Variables
```bash
export WEBHOOK_SECRET="your_strong_secret_here_min_32_chars"
export HOST="127.0.0.1"  # For local only, or 0.0.0.0 if exposing
export PORT="5000"
```

### 2. Generate a Strong Webhook Secret
```bash
# Generate a strong secret (use this value)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Additional Security Measures

#### For Production Deployment:
- [ ] **Use HTTPS/TLS** - Never expose webhook endpoints over HTTP
- [ ] **Add rate limiting** - Use Flask-Limiter or nginx rate limiting
- [ ] **Set max request size** - Add `MAX_CONTENT_LENGTH` to Flask config
- [ ] **Use a WSGI server** - Replace Flask dev server with Gunicorn/uWSGI
- [ ] **Add reverse proxy** - Use nginx/Apache in front of the application
- [ ] **Enable logging** - Use proper logging with rotation
- [ ] **Monitor traffic** - Set up monitoring and alerting

#### Recommended Flask Configuration:
```python
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB limit
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
```

#### For Local Development with Tunnels:
- [ ] **Use authentication** - Add basic auth if exposing via ngrok/localtunnel
- [ ] **Validate webhook signatures** - Never disable signature verification
- [ ] **Monitor tunnel URLs** - Don't share tunnel URLs publicly
- [ ] **Use temporary secrets** - Use different secrets for dev/prod

## 🚨 Never Do These:
- ❌ Don't commit secrets to git
- ❌ Don't disable signature verification
- ❌ Don't run in debug mode in production
- ❌ Don't expose on 0.0.0.0 unless needed
- ❌ Don't ignore SSL/TLS certificate errors
- ❌ Don't log sensitive webhook payloads

## 📋 Pre-Deployment Testing:
1. Test with invalid signatures (should fail)
2. Test with malformed JSON (should handle gracefully)
3. Test with oversized payloads
4. Verify all handlers work correctly
5. Check logs don't contain sensitive data

## 🔄 Regular Maintenance:
- Update dependencies monthly: `pip install -r requirements.txt --upgrade`
- Rotate webhook secrets quarterly
- Review logs for suspicious activity
- Monitor for Flask/Werkzeug security updates

