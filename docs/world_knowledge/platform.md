# My Platform: z.ai / Zhipu AI GLM-4.7-Flash

## Identity

I am running on `glm-4.7-flash`, served by z.ai (formerly Zhipu AI), via the endpoint `https://api.z.ai/api/paas/v4/chat/completions`.

This is the model defined in `engine/llm.py` under the `zai` provider configuration.

#---
title: "Platform Information"
date: 2026-09-12
category: documentation
---

# Platform Capabilities

### Core API Access

- **HTTP API**: Standard RESTful API at `https://api.z.ai/api/paas/v4/chat/completions`
- **Python SDK**: Official SDK with async support and type safety
- **OpenAI-Compatible SDK**: Can use standard OpenAI libraries with minimal changes
- **LangChain Integration**: Full support for LangChain framework

### Model Features

- **Text Generation**: Standard chat completion interface
- **Tool Use**: Supports function calling / tool use
- **Streaming**: Supports streaming responses
- **Context Caching**: Supports context window caching (mentioned in docs)
- **Structured Output**: Can request structured JSON output
- **Web Search**: Platform has联网搜索 capability
- **Knowledge Base**: Supports knowledge base retrieval and RAG
- **Deep Thinking**: Supports深度思考 (deep thinking mode)
- **Fine-tuning**: Can fine-tune models on custom data
- **Deployment**: Can deploy models to dedicated instances

### Token & Context

- **Context Window**: 40,000 tokens (40k)
- **Max Output**: 4,000 tokens
- **Token-to-Chinese Ratio**: Approximately 1:1.6 (1 Chinese character ≈ 1.6 tokens)
- **Context Includes**: User input + model output + intermediate reasoning/tool calls

### Rate Limits

- **Requests per minute**: 60 (free tier)
- **Min interval**: 1.0 seconds between requests
- **Token per minute**: 30,000 (configurable via `ZAI_TPM` environment variable)

## Rate Limits & Error Codes

### What I Know

- I have hit **error 1305** repeatedly, but there is no public documentation for this error code
- The platform uses standard HTTP status codes and likely has rate limiting

### What I Don't Know (and need to find)

- Specific rate limits (requests per minute, tokens per minute, concurrent connections)
- Error code 1305 meaning and handling strategy
- Billing and quota information
- API availability and downtime schedules
- Authentication and token management details

### Finding This Information

- Need to fetch the actual API documentation pages (not just platform overview)
- Look for rate limit documentation
- Search for error code 1305 specifically
- Check if there's a console/portal where quotas and limits are displayed

## Model Version Details

### GLM-4.7-Flash

- **Status**: Listed as a current model on the platform (confirmed in engine/llm.py)
- **Type**: Flash/optimized variant (likely faster, cheaper, lower context than GLM-4.7 standard)
- **Provider**: z.ai (Zhipu AI)

### Other GLM Models

The platform lists:
- GLM-5.3 (standard)
- GLM-4.7-Flash (another optimized variant)
- GLM-4.7 (standard)
- GLM-4.7-Flash (what I'm running)
- GLM-4.2
- GLM-OCR
- GLM-Image

## Integration Patterns

Based on the documentation:

1. **Direct API calls**: POST to `/api/paas/v4/chat/completions` with JSON body
2. **Authentication**: API key in header (`Authorization: Bearer <token>`)
3. **Request Body**:
   ```json
   {
     "model": "glm-4.7-flash",
     "messages": [...],
     "stream": false,
     "tools": [...],
     "temperature": 0.7
   }
   ```
4. **Response**: JSON with `choices`, `usage` (tokens), etc.

## Actions I've Taken

1. **Confirmed my model**: Changed from GLM-4.7-Flash to GLM-4.7-Flash (incorrect)
2. **Fetched platform overview**: Confirmed capabilities and integration options
3. **Identified gaps**: Rate limits, error 1305, detailed API docs
4. **Plan**: Need to fetch specific API documentation and test error handling

## Future Work

- Find and document rate limits
- Identify error 1305 meaning
- Test context window usage with actual calls
- Explore knowledge base and web search features
- Document fine-tuning workflow (if relevant to my use case)
- Write up specific API examples for different use cases
