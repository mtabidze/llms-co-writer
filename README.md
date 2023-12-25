# Large Language Models (LLMs) Co-Writer

---

[![GitHub Last Commit](https://img.shields.io/github/last-commit/mtabidze/llms-co-writer.svg?branch=main)](https://github.com/mtabidze/llms-co-writer/commits/main)
[![Testing Workflow Status](https://github.com/mtabidze/llms-co-writer/actions/workflows/testing-flow.yml/badge.svg?branch=main)](https://github.com/mtabidze/llm-co-writer/actions/workflows/testing-flow.yml)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/mtabidze/llms-co-writer.svg)](https://github.com/mtabidze/llms-co-writer/pulls)
[![GitHub Release](https://img.shields.io/github/release/mtabidze/llms-co-writer.svg)](https://github.com/mtabidze/llms-co-writer/releases)

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=flat&logo=swagger&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=flat&logo=openai&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white)
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=flat&logo=Amazon%20DynamoDB&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=flat&logo=gnu-bash&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Debian](https://img.shields.io/badge/Debian-D70A53?style=flat&logo=debian&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=flat&logo=macos&logoColor=F0F0F0)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=flat&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Atom](https://img.shields.io/badge/Atom-%2366595C.svg?style=flat&logo=atom&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)
![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=flat&logo=dependabot&logoColor=white)

---

## Introduction

The LLMs Co-Writer API is a powerful RESTful service that leverages the prowess of large language models (LLMs), such as OpenAI's GPT, to assist in textual completion, co-writing, and other creative tasks. Built with Python and FastAPI, this application integrates cutting-edge AI, efficient caching via Redis, and reliable storage with DynamoDB.

---

## Features

- Utilizes OpenAI API for advanced text completions.
- Designed to incorporate additional LLMs in the future.
- Redis-powered caching to enhance speed and efficiency.
- DynamoDB-driven persistence of request and inference data.
- Docker compatibility for easy deployment and scalability.
- Integrated GitHub Actions for automated testing and CI.

---

## Architecture Diagram (Draft)
![Architecture Diagram](docs/ArchitectureDiagram.png?raw=true)

---

## Usage
### BLING
Here's an example demonstrating how to submit a request using the BLING models endpoint:
```shell
curl -X 'POST' \
  'http://localhost:8000/v1/bling/responses' \
  -H 'accept: application/json' \
  -H 'secret-key: abc123...' \
  -H 'Content-Type: application/json' \
  -d '{
  "context": "A. The cat quickly climbed the tall tree. \n B. She have not seen that movie yet. \n C. They are going to the beach this weekend.",
  "query": "Can you identify any grammar mistakes in the provided context?"
}'
```

#### Response

Here's an example illustrating an API response from the BLING models endpoint:
```json
{
  "response": " B. She have not seen that movie yet."
}
```

### OpenAI
#### Making a Request
Here's an example demonstrating how to submit a request using the OpenAI models endpoint:
```shell
curl -X 'POST' \
  'http://localhost:8000/v1/openai/chat/completions' \
  -H 'accept: application/json' \
  -H 'secret-key: abc123...' \
  -H 'Content-Type: application/json' \
  -d '{
  "chat_messages": [
    {
      "content": "You are a laconic assistant for tasks related to text completion, co-writing, and various creative assignments.",
      "role": "system"
    },
    {
      "content": "Correct grammatical mistakes",
      "role": "user"
    },
    {
      "content": "She do not like the cold weather in winter.",
      "role": "user"
    }
  ]
}'
```

#### Response

Here's an example illustrating an API response from the OpenAI models endpoint:
```json
{
  "message": "She dislikes the frigid temperatures of winter."
}
```


---

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process.