#!/bin/bash

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "How do I reset my password?"}'

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What is quantum computing?"}'