#!/usr/bin/env python3
"""
Simple Chat Demo with Langfuse Tracing
This demonstrates basic LLM tracing with a simple chat interface.
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse
import openai
import time
import random

# Load environment variables
load_dotenv()

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_llm(user_message: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Simple chat completion with tracing
    """
    # Start a span for this chat completion
    span = langfuse.start_span(name="chat_completion", input=user_message)
    try:
        # Start a generation observation
        generation = langfuse.start_observation(name="llm_call", model=model, input=user_message, as_type="generation")
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant specializing in cloud-native technologies and DevOps."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        generation.update(output=result)
        generation.end()
        span.update(output=result)
        span.end()
        
        return result
    except Exception as e:
        print(f"Error in chat completion: {e}")
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        generation.update(output=error_msg, level="ERROR")
        generation.end()
        span.update(output=error_msg, level="ERROR")
        span.end()
        return error_msg

def run_conversation():
    """
    Run a sample conversation with multiple exchanges
    """
    # Start a span for the entire conversation session
    session_span = langfuse.start_span(name="conversation_session")
    
    print("🤖 Starting CloudRaft AI Assistant Demo")
    print("=" * 50)
    
    # Sample conversation topics
    topics = [
        "What is Kubernetes and why is it important for cloud-native applications?",
        "How can I implement observability for microservices?",
        "What are the best practices for container security?",
        "Explain the difference between Docker and Kubernetes",
        "How do I set up monitoring with Prometheus and Grafana?"
    ]
    
    responses = []
    
    try:
        for i, topic in enumerate(topics, 1):
            print(f"\n💬 Question {i}: {topic}")
            
            # Add some realistic delay
            time.sleep(random.uniform(1, 3))
            
            response = chat_with_llm(topic)
            responses.append({"question": topic, "answer": response})
            print(f"🤖 Answer: {response}")
            print("-" * 30)
        
        # Update session span with summary
        session_span.update(
            output=f"Completed conversation with {len(topics)} questions",
            metadata={"total_questions": len(topics), "topics": topics}
        )
        
        print("\n✅ Conversation completed! Check Langfuse dashboard for traces.")
    finally:
        session_span.end()

if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your environment or .env file")
        exit(1)
    
    if not os.getenv("LANGFUSE_PUBLIC_KEY"):
        print("❌ Please set LANGFUSE_PUBLIC_KEY in your environment or .env file")
        exit(1)
    
    run_conversation()
    
    # Flush any remaining traces
    langfuse.flush()
