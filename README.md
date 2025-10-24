# Langfuse Cloud Demo Setup

This repository contains sample applications that demonstrate LLM observability and tracing capabilities using Langfuse Cloud.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Langfuse Cloud account (free at https://cloud.langfuse.com)
- OpenAI API key (for demo purposes)

### 1. Get Your Langfuse API Keys

1. Visit https://cloud.langfuse.com and create a free account
2. Go to Settings → API Keys
3. Copy your Public Key and Secret Key
4. Create a `.env` file:

```bash
cp env.example .env
# Edit .env with your actual keys
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Demo Applications

```bash
# Run all demos at once
python run_all_demos.py

# Or run individually
python simple_chat_demo.py
python rag_demo.py
python langchain_demo.py
```

## 📊 What You'll See in Langfuse

After running the demos, visit https://cloud.langfuse.com to see:

### 1. Traces Dashboard
- Real-time traces of all LLM calls
- Request/response details
- Performance metrics (latency, token usage)
- Error tracking

### 2. Sessions View
- Grouped conversations and workflows
- User interaction patterns
- Session-level analytics

### 3. Analytics
- Token usage and costs
- Model performance comparison
- Usage patterns over time

### 4. Prompts Management
- Prompt versioning and testing
- A/B testing capabilities
- Prompt optimization insights

## 🎯 Demo Scenarios

### Simple Chat Demo (`simple_chat_demo.py`)
- Basic LLM conversation tracing
- Multiple question-answer pairs
- Performance metrics collection

### RAG Demo (`rag_demo.py`)
- Document retrieval simulation
- Context assembly
- Multi-step LLM pipeline
- Complex workflow tracing

### LangChain Demo (`langchain_demo.py`)
- LangChain integration
- Conversation memory
- Multi-step workflows
- Chain composition tracing

## 📸 Screenshots for Blog

Here are the key screenshots you should capture:

1. **Langfuse Dashboard Home**
   - Overview of traces and sessions
   - Recent activity feed

2. **Trace Detail View**
   - Individual trace with timing
   - Input/output data
   - Nested spans for complex workflows

3. **Analytics Dashboard**
   - Token usage charts
   - Cost analysis
   - Performance metrics

4. **Sessions View**
   - Grouped conversations
   - User journey mapping

5. **Prompts Management**
   - Prompt library
   - Version comparison
   - A/B testing interface

## 🔧 Configuration

### Environment Variables

```bash
# Langfuse Cloud Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-your-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
```

### Customizing Demos

You can modify the demo scripts to:
- Add your own prompts and questions
- Integrate with different LLM providers
- Add custom metrics and tags
- Test different model parameters

## 🛠️ Troubleshooting

### Common Issues

1. **API key errors**
   - Ensure your `.env` file is in the same directory
   - Verify keys are copied correctly from Langfuse cloud dashboard
   - Check that your Langfuse account is active

2. **OpenAI API errors**
   - Verify your OpenAI API key is valid
   - Check you have sufficient credits
   - Ensure you're using a supported model

3. **Connection errors**
   - Check your internet connection
   - Verify the Langfuse host URL is correct
   - Ensure your firewall allows HTTPS connections

### Quick Reset

```bash
# Remove .env file and recreate
rm .env
cp env.example .env
# Edit .env with your actual keys
```

## 📚 Additional Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [OpenTelemetry Integration](https://langfuse.com/docs/integrations/opentelemetry)
- [LangChain Integration](https://langfuse.com/docs/integrations/langchain)
- [API Reference](https://langfuse.com/docs/api)

## 🎉 Next Steps

After exploring the demos:

1. Integrate Langfuse into your own LLM applications
2. Set up custom metrics and alerts
3. Explore advanced features like evaluations and prompt management
4. Consider upgrading to paid plans for production use

Happy tracing! 🚀
