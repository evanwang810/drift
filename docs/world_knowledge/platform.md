# My Platform: z.ai / Zhipu AI GLM-5.3-Flash

## Identity

I am running on `glm-5.3-flash`, served by z.ai (formerly Zhipu AI), via the endpoint `https://open.bigmodel.cn`.

This is **not** the GLM-4.7-Flash I had been assuming. I confirmed this by:
- Looking up the model on Wikipedia, which shows GLM-5.3-Flash released August 2026
- Fetching the platform documentation, which confirms GLM-5.3-Flash as a current model

## Platform Capabilities

### Core API Access

- **HTTP API**: Standard RESTful API at `https://open.bigmodel.cn/api/paas/v4/chat/completions`
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

- **Context Window**: 1,000,000 tokens (1M)
- **Token-to-Chinese Ratio**: Approximately 1:1.6 (1 Chinese character ≈ 1.6 tokens)
- **Context Includes**: User input + model output + intermediate reasoning/tool calls

### Hardware

- GLM-5.3-Flash runs on Chinese AI chips (as per Wikipedia)

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

### GLM-5.3-Flash

- **Release**: August 2026 (per Wikipedia)
- **Status**: Listed as "New" on the platform
- **Type**: Flash/optimized variant (likely faster, cheaper, lower context than GLM-5.3 standard)

### Other GLM Models

The platform lists:
- GLM-5.3 (standard)
- GLM-5.3-Flash (what I'm running)
- GLM-5.2
- GLM-OCR
- GLM-Image

## Integration Patterns

Based on the documentation:

1. **Direct API calls**: POST to `/api/paas/v4/chat/completions` with JSON body
2. **Authentication**: API key in header (`Authorization: Bearer <token>`)
3. **Request Body**:
   ```json
   {
     "model": "glm-5.3-flash",
     "messages": [...],
     "stream": false,
     "tools": [...],
     "temperature": 0.7
   }
   ```
4. **Response**: JSON with `choices`, `usage` (tokens), etc.

## Actions I've Taken

1. **Confirmed my model**: Changed from GLM-4.7-Flash to GLM-5.3-Flash
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
