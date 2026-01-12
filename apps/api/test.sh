#!/bin/bash

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"model": "faq-chat", "messages": [{"role": "user", "content": "How do I reset my password?"}]}'

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"model": "faq-chat", "messages": [{"role": "user", "content": "What is quantum computing?"}]}'