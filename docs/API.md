# AI Platform API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

All API endpoints require authentication using session-based authentication. Include cookies in your requests.

For API key authentication (coming soon), include the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

Check API health status.

**Endpoint:** `GET /api/health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### Chat

Send a message to the AI and get a response.

**Endpoint:** `POST /api/chat`

**Authentication:** Required

**Request Body:**
```json
{
  "message": "Your message here",
  "model": "auto"
}
```

**Parameters:**
- `message` (string, required): The message to send to the AI
- `model` (string, optional): Model to use. Options: `auto`, `deepseek`, `gpt4all`, `llama`, `vicuna`. Default: `auto`

**Response:**
```json
{
  "response": "AI response here",
  "model": "deepseek",
  "message_id": 123
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (empty message)
- `401`: Unauthorized
- `429`: Rate limit exceeded
- `500`: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"message": "Write a Python function to reverse a string", "model": "auto"}'
```

---

### Get Available Models

Get list of available AI models.

**Endpoint:** `GET /api/models`

**Authentication:** Required

**Response:**
```json
{
  "models": [
    {
      "id": "auto",
      "name": "Auto-Select",
      "description": "Automatically selects the best model for your task",
      "recommended": true
    },
    {
      "id": "deepseek",
      "name": "DeepSeek Coder",
      "description": "Specialized for coding, debugging, and programming tasks",
      "use_case": "Coding & Development"
    }
  ]
}
```

---

### Get Usage Statistics

Get current user's usage statistics.

**Endpoint:** `GET /api/usage`

**Authentication:** Required

**Response:**
```json
{
  "messages_today": 5,
  "messages_total": 42,
  "rate_limit": 10,
  "tier": "free"
}
```

---

### Get Chat History

Get paginated chat history.

**Endpoint:** `GET /api/history`

**Authentication:** Required

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `per_page` (int, optional): Results per page (default: 50, max: 100)

**Response:**
```json
{
  "messages": [
    {
      "id": 123,
      "role": "user",
      "content": "Hello AI",
      "model": "gpt4all",
      "created_at": "2024-01-01T12:00:00"
    },
    {
      "id": 124,
      "role": "assistant",
      "content": "Hello! How can I help you?",
      "model": "gpt4all",
      "created_at": "2024-01-01T12:00:05"
    }
  ],
  "total": 100,
  "pages": 2,
  "current_page": 1
}
```

---

## Rate Limiting

Rate limits are applied per user based on tier:

| Tier | Messages per Hour |
|------|-------------------|
| Free | 10 |
| Premium | 100 |
| Admin | 1000 |

When rate limit is exceeded, you'll receive a `429` status code with error message:
```json
{
  "error": "Rate limit exceeded. You can send 10 messages per hour. Please try again later."
}
```

---

## Intelligent Model Routing

When using `model: "auto"`, the system automatically selects the best model based on content type:

| Content Type | Model Used | Keywords |
|-------------|-----------|----------|
| Coding | DeepSeek Coder | code, function, programming, debug, python, javascript, etc. |
| Documents | Llama.cpp | pdf, document, file, csv, json, etc. |
| Images/Videos | Vicuna | image, photo, video, analyze image, etc. |
| General | GPT4All | All other queries |

---

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `400`: Bad Request - Invalid input
- `401`: Unauthorized - Authentication required
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Server-side error

---

## WebSocket Support (Future)

Real-time chat streaming will be available via WebSocket at:
```
ws://localhost:5000/ws/chat
```

---

## Best Practices

1. **Use Auto Model Selection**: Let the system choose the best model for your task
2. **Handle Rate Limits**: Implement exponential backoff when rate limited
3. **Cache Responses**: Cache AI responses when appropriate
4. **Error Handling**: Always handle errors gracefully
5. **Pagination**: Use pagination for chat history to avoid large responses

---

## Example Integration

### Python

```python
import requests

# Login first
session = requests.Session()
session.post('http://localhost:5000/auth/login', data={
    'email': 'user@example.com',
    'password': 'password'
})

# Send chat message
response = session.post('http://localhost:5000/api/chat', json={
    'message': 'Write a Python function to calculate factorial',
    'model': 'auto'
})

data = response.json()
print(f"AI Response: {data['response']}")
print(f"Model Used: {data['model']}")
```

### JavaScript

```javascript
// Send chat message
async function sendMessage(message, model = 'auto') {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ message, model })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    console.log('Response:', data.response);
    console.log('Model:', data.model);
  } else {
    console.error('Error:', data.error);
  }
}
```

---

## Support

For API support and questions:
- GitHub Issues: https://github.com/Bucin404/AI-platform/issues
- Email: support@aiplatform.com
