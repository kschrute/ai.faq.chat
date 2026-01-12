# FAQ Chat

Question-answering system for an FAQ without fine-tuning a language model. Instead of training a model, it uses Retrieval-Augmented Generation (RAG), leveraging a pre-trained embedding model and a vector search index to retrieve answers from a pre-existing FAQ dataset. 

This approach is simpler and faster to set up than fine-tuning, as it requires no model training, making it ideal for small FAQ datasets or rapid prototyping. It embeds FAQ questions into a vector space, searches for the most similar question to a user’s query, and returns the corresponding answer. If no sufficiently similar question is found, it returns `false`.

## Demo

The demo is avaialble at [ai-faq-chat.fly.dev](https://ai-faq-chat.fly.dev)

![Demo](demo.jpeg)

## Prerequisites

- [pnpm](https://pnpm.io)
- [uv](https://astral.sh/uv)

## Getting Started

To install the dependencies run:

```shell
./install.sh
```

And to start the API and the Web app run this after:

```shell
./dev.sh
```

## Updating FAQ

If you update FAQ in the `apps/api/faq.json` file, run the following to rebuild the index:

```shell
./build.sh
```

## Testing the API

You can use `curl` to test the API or use the UI at http://localhost:5173

```shell
curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "How do I reset my password?"}'
```

You should see a response like this:

```json
{ "answer": "Go to settings and click 'Reset Password'." }
```

And if you ask something that's not in the FAQ:

```shell
curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What is quantum computing?"}'
```

The response should be:

```json
{ "answer": false }
```
