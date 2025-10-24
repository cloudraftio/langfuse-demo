# Langfuse Cloud Screenshot Guide

This guide will help you capture the most effective screenshots for your LLM observability blog post using Langfuse Cloud.

## 🎯 Key Screenshots to Capture

### 1. Langfuse Dashboard Overview
**URL:** https://cloud.langfuse.com  
**What to show:**
- Recent traces and sessions
- Activity feed
- Quick stats (total traces, sessions, etc.)

**Tips:**
- Make sure you have some traces from running the demos
- Capture the clean, modern interface
- Show the navigation sidebar

### 2. Trace Detail View
**URL:** https://cloud.langfuse.com/traces/[trace-id]  
**What to show:**
- Individual trace with timing breakdown
- Input/output data
- Nested spans for complex workflows
- Performance metrics (latency, token count)

**Tips:**
- Click on a trace from the RAG demo for complex nested spans
- Show the timeline view
- Highlight the token usage and cost information

### 3. Sessions View
**URL:** https://cloud.langfuse.com/sessions  
**What to show:**
- Grouped conversations
- User journey mapping
- Session-level analytics

**Tips:**
- Run the conversation demos first to create sessions
- Show how conversations are grouped together
- Highlight the session timeline

### 4. Analytics Dashboard
**URL:** https://cloud.langfuse.com/analytics  
**What to show:**
- Token usage charts over time
- Cost analysis by model
- Performance metrics (latency, throughput)
- Error rates

**Tips:**
- Run multiple demos to generate data
- Show different time ranges (last hour, day, week)
- Highlight cost tracking features

### 5. Prompts Management
**URL:** https://cloud.langfuse.com/prompts  
**What to show:**
- Prompt library
- Version comparison
- A/B testing interface
- Prompt performance metrics

**Tips:**
- This might be empty initially, but shows the capability
- Focus on the interface design and features

### 6. Settings/API Keys
**URL:** https://cloud.langfuse.com/settings  
**What to show:**
- API key management
- Project settings
- Integration options

**Tips:**
- Show the clean settings interface
- Highlight the API key generation process

## 📸 Screenshot Best Practices

### Before Taking Screenshots

1. **Run the demos first:**
   ```bash
   python run_all_demos.py
   ```

2. **Wait for data to appear:**
   - Give Langfuse a few minutes to process traces
   - Refresh the dashboard to see latest data

3. **Clean up the interface:**
   - Close any unnecessary browser tabs
   - Use a clean browser window
   - Consider using incognito mode for cleaner look

### Screenshot Settings

- **Resolution:** Use high DPI (Retina) if available
- **Browser:** Chrome or Firefox work best
- **Window size:** Use a reasonable window size (not full screen)
- **Zoom:** 100% zoom level

### What to Highlight

1. **Performance Metrics:**
   - Latency graphs
   - Token usage charts
   - Error rates

2. **User Experience:**
   - Clean, intuitive interface
   - Easy navigation
   - Rich data visualization

3. **Technical Features:**
   - Distributed tracing
   - Nested spans
   - Real-time updates
   - Cost tracking

## 🎬 Demo Sequence for Screenshots

1. **Get your API keys:**
   - Visit https://cloud.langfuse.com
   - Create account and get API keys
   - Update .env file with your keys

2. **Run demos in sequence:**
   ```bash
   # Run all demos
   python run_all_demos.py
   
   # Or run individually for more control
   python simple_chat_demo.py
   # Wait 2-3 minutes, then take screenshots
   
   python rag_demo.py
   # Wait 2-3 minutes, then take more screenshots
   
   python langchain_demo.py
   # Final screenshots
   ```

3. **Capture different views:**
   - Dashboard overview
   - Individual trace details
   - Analytics charts
   - Session groupings

## 🔧 Troubleshooting Screenshots

### If traces don't appear:
- Check that your API keys are correct
- Verify your Langfuse account is active
- Wait a few minutes for processing
- Check your internet connection

### If interface looks empty:
- Run the demos first to generate data
- Refresh the page
- Check different time ranges in analytics

### If demos fail:
- Verify OpenAI API key is valid
- Check internet connection
- Review error messages in terminal

## 📝 Caption Ideas

### For Dashboard Screenshot:
"Langfuse provides a clean, intuitive dashboard for monitoring LLM applications in real-time, with comprehensive trace visibility and performance metrics."

### For Trace Detail Screenshot:
"Detailed trace view shows the complete request flow with nested spans, timing breakdown, and token usage - essential for debugging complex LLM workflows."

### For Analytics Screenshot:
"Built-in analytics track token usage, costs, and performance over time, enabling data-driven optimization of LLM deployments."

### For Sessions Screenshot:
"Session grouping automatically organizes related conversations and workflows, making it easy to understand user interactions and system behavior."

## 🚀 Quick Start for Screenshots

```bash
# 1. Setup environment
cd langfuse-demo
./setup.sh

# 2. Get API keys from https://cloud.langfuse.com
# 3. Update .env file
# 4. Run demos
python run_all_demos.py

# 5. Take screenshots at https://cloud.langfuse.com
```

Happy screenshotting! 📸
