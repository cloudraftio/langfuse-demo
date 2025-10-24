#!/usr/bin/env python3
"""
LangChain Integration Demo with Langfuse Tracing
This demonstrates how to use Langfuse with LangChain for more complex workflows.
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

def simple_llm_chain_demo():
    """
    Simple LLM chain demo with Langfuse tracing
    """
    print("🔗 Simple LLM Chain Demo")
    print("=" * 40)
    
    # Sample topics and audiences
    topics = [
        ("Kubernetes", "a beginner developer"),
        ("Microservices", "a DevOps engineer"),
        ("Observability", "a product manager"),
        ("Container Security", "a security analyst")
    ]
    
    for topic, audience in topics:
        print(f"\n📝 Explaining {topic} to {audience}...")
        
        # Start span for explanation chain
        trace = langfuse.start_span(name="explanation_chain", input={"topic": topic, "audience": audience})
        
        try:
            # Add delay for realistic demo
            time.sleep(random.uniform(1, 2))
            
            # Create prompt
            prompt = f"Explain {topic} to {audience} in simple terms. Include practical examples."
            
            # Create generation observation
            generation = trace.start_observation(
                name="llm_explanation",
                model="gpt-3.5-turbo",
                input=prompt,
                as_type="generation"
            )
            
            try:
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful technical expert who explains complex topics clearly."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                
                result = response.choices[0].message.content
                generation.update(output=result)
                generation.end()
                trace.update(name="explanation_chain", output=result)
                
                print(f"🤖 Response: {result}")
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                generation.update(output=error_msg, level="ERROR")
                generation.end()
                trace.update(name="explanation_chain", output=error_msg, level="ERROR")
                print(f"❌ {error_msg}")
        finally:
            trace.end()
        
        print("-" * 30)

def conversation_chain_demo():
    """
    Conversation chain demo with Langfuse tracing
    """
    print("\n💬 Conversation Chain Demo")
    print("=" * 45)
    
    # Start main conversation span
    conversation_trace = langfuse.start_span(name="conversation_chain")
    
    try:
        # Sample conversation
        conversation_steps = [
            "Hi! I'm working on a cloud-native application. Can you help me understand the basics?",
            "What are the key components I need to consider for monitoring?",
            "How does this differ from traditional application monitoring?",
            "What tools would you recommend for a Kubernetes environment?"
        ]
        
        conversation_history = []
        
        for i, message in enumerate(conversation_steps, 1):
            print(f"\n👤 User: {message}")
            
            # Add delay
            time.sleep(random.uniform(1, 3))
            
            # Create span for this conversation turn
            turn_span = conversation_trace.start_span(name=f"conversation_turn_{i}", input=message)
            
            try:
                # Build context with conversation history
                context_messages = [
                    {"role": "system", "content": "You are a helpful cloud-native expert. Continue the conversation naturally based on the previous context."}
                ]
                context_messages.extend(conversation_history)
                context_messages.append({"role": "user", "content": message})
                
                try:
                    # Get response
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=context_messages,
                        temperature=0.7,
                        max_tokens=300
                    )
                    
                    result = response.choices[0].message.content
                    turn_span.update(output=result)
                    
                    # Add to conversation history
                    conversation_history.append({"role": "user", "content": message})
                    conversation_history.append({"role": "assistant", "content": result})
                    
                    print(f"🤖 Assistant: {result}")
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    turn_span.update(output=error_msg, level="ERROR")
                    print(f"❌ {error_msg}")
            finally:
                turn_span.end()
            
            print("-" * 30)
        
        # Update conversation trace
        conversation_trace.update(
            name="conversation_chain",
            output=f"Completed conversation with {len(conversation_steps)} turns",
            metadata={"total_turns": len(conversation_steps)}
        )
    finally:
        conversation_trace.end()

def multi_step_workflow_demo():
    """
    Multi-step workflow demo with Langfuse tracing
    """
    print("\n🔄 Multi-Step Workflow Demo")
    print("=" * 35)
    
    # Sample problems
    problems = [
        "Our microservices are experiencing high latency and we can't identify the bottleneck",
        "We need to implement zero-downtime deployments for our Kubernetes applications",
        "Our application logs are scattered across multiple services and hard to correlate"
    ]
    
    for problem in problems:
        print(f"\n🔍 Problem: {problem}")
        
        # Start workflow span
        workflow_trace = langfuse.start_span(name="multi_step_workflow", input=problem)
        
        try:
            # Step 1: Analysis
            print("📊 Step 1: Analyzing problem...")
            time.sleep(random.uniform(2, 3))
            
            analysis_span = workflow_trace.start_span(name="problem_analysis", input=problem)
            try:
                analysis_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cloud-native expert. Analyze problems and identify key challenges and potential solutions."},
                        {"role": "user", "content": f"Analyze this cloud-native problem: {problem}. Identify the key challenges and potential solutions."}
                    ],
                    temperature=0.3,
                    max_tokens=400
                )
                
                analysis = analysis_response.choices[0].message.content
                analysis_span.update(output=analysis)
                print(f"Analysis: {analysis}")
            except Exception as e:
                error_msg = f"Analysis error: {str(e)}"
                analysis_span.update(output=error_msg, level="ERROR")
                print(f"❌ {error_msg}")
                analysis_span.end()
                workflow_trace.end()
                continue
            finally:
                analysis_span.end()
            
            # Step 2: Solution
            print("\n💡 Step 2: Generating solution...")
            time.sleep(random.uniform(2, 3))
            
            solution_span = workflow_trace.start_span(name="solution_generation", input={"problem": problem, "analysis": analysis})
            try:
                solution_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cloud-native expert. Provide detailed implementation plans with specific tools and steps."},
                        {"role": "user", "content": f"Based on this analysis: {analysis}\n\nFor the original problem: {problem}\n\nProvide a detailed implementation plan with specific tools and steps."}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                solution = solution_response.choices[0].message.content
                solution_span.update(output=solution)
                print(f"Solution: {solution}")
            except Exception as e:
                error_msg = f"Solution error: {str(e)}"
                solution_span.update(output=error_msg, level="ERROR")
                print(f"❌ {error_msg}")
            finally:
                solution_span.end()
            
            # Update workflow trace
            workflow_trace.update(
                name="multi_step_workflow",
                output=f"Completed analysis and solution for: {problem}",
                metadata={"problem": problem}
            )
        finally:
            workflow_trace.end()
        
        print("-" * 50)

def run_langchain_demo():
    """
    Run all LangChain demos
    """
    print("🚀 LangChain + Langfuse Integration Demo")
    print("=" * 50)
    
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your environment or .env file")
        return
    
    if not os.getenv("LANGFUSE_PUBLIC_KEY"):
        print("❌ Please set LANGFUSE_PUBLIC_KEY in your environment or .env file")
        return
    
    try:
        # Run different demos
        simple_llm_chain_demo()
        conversation_chain_demo()
        multi_step_workflow_demo()
        
        print("\n✅ LangChain demo completed! Check Langfuse dashboard for traces.")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
    
    finally:
        # Flush any remaining traces
        langfuse.flush()

if __name__ == "__main__":
    run_langchain_demo()
