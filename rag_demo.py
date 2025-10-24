#!/usr/bin/env python3
"""
RAG (Retrieval Augmented Generation) Demo with Langfuse Tracing
This demonstrates a more complex LLM pipeline with document retrieval and generation.
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse
import openai
import time
import random
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# Sample knowledge base (in a real app, this would be a vector database)
KNOWLEDGE_BASE = {
    "kubernetes": [
        "Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications.",
        "Kubernetes provides features like service discovery, load balancing, storage orchestration, automated rollouts and rollbacks, and self-healing.",
        "Key Kubernetes components include the API server, etcd, kubelet, kube-proxy, and various controllers."
    ],
    "observability": [
        "Observability in cloud-native applications involves monitoring, logging, and tracing to understand system behavior.",
        "The three pillars of observability are metrics, logs, and traces.",
        "Popular observability tools include Prometheus for metrics, ELK stack for logging, and Jaeger for distributed tracing."
    ],
    "devops": [
        "DevOps is a set of practices that combines software development and IT operations to shorten the development lifecycle.",
        "Key DevOps practices include continuous integration, continuous deployment, infrastructure as code, and monitoring.",
        "DevOps tools include Jenkins, GitLab CI, Docker, Kubernetes, Terraform, and Ansible."
    ],
    "microservices": [
        "Microservices architecture is an approach to building applications as a collection of loosely coupled services.",
        "Each microservice is independently deployable and can be developed by different teams using different technologies.",
        "Microservices communicate through well-defined APIs, typically using HTTP/REST or message queues."
    ]
}

def retrieve_relevant_documents(query: str, top_k: int = 3, trace=None) -> List[str]:
    """
    Simulate document retrieval from a knowledge base
    """
    # Create a span for document retrieval
    retrieval_span = trace.start_span(name="document_retrieval", input=query) if trace else None
    
    query_lower = query.lower()
    relevant_docs = []
    
    # Simple keyword matching (in reality, you'd use vector similarity)
    for topic, docs in KNOWLEDGE_BASE.items():
        if any(keyword in query_lower for keyword in topic.split()):
            relevant_docs.extend(docs)
    
    # Return top_k documents
    result = relevant_docs[:top_k]
    
    if retrieval_span:
        retrieval_span.update(output=result, metadata={"total_docs": len(result)})
        retrieval_span.end()
    
    return result

def assemble_context(documents: List[str], query: str, trace=None) -> str:
    """
    Assemble retrieved documents into context for the LLM
    """
    # Create a span for context assembly
    context_span = trace.start_span(name="context_assembly", input={"documents": documents, "query": query}) if trace else None
    
    context = "Relevant information:\n\n"
    for i, doc in enumerate(documents, 1):
        context += f"{i}. {doc}\n\n"
    
    context += f"Question: {query}\n\n"
    context += "Please answer the question based on the provided information. If the information doesn't contain enough details, say so."
    
    if context_span:
        context_span.update(output=context, metadata={"doc_count": len(documents)})
        context_span.end()
    
    return context

def generate_answer(context: str, model: str = "gpt-3.5-turbo", trace=None) -> str:
    """
    Generate answer using LLM with retrieved context
    """
    # Create a generation observation
    generation_span = trace.start_observation(name="llm_generation", model=model, input=context, as_type="generation") if trace else None
    
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context. Be accurate and cite specific information when possible."},
                {"role": "user", "content": context}
            ],
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=600
        )
        
        result = response.choices[0].message.content
        
        if generation_span:
            generation_span.update(output=result)
            generation_span.end()
        
        return result
    except Exception as e:
        error_msg = f"Error generating answer: {str(e)}"
        if generation_span:
            generation_span.update(output=error_msg, level="ERROR")
            generation_span.end()
        return error_msg

def rag_pipeline(query: str) -> Dict[str, any]:
    """
    Complete RAG pipeline with tracing
    """
    # Start main span for RAG pipeline
    trace = langfuse.start_span(name="rag_pipeline", input=query)
    
    try:
        print(f"🔍 Processing query: {query}")
        
        # Step 1: Retrieve relevant documents
        print("📚 Retrieving relevant documents...")
        documents = retrieve_relevant_documents(query, trace=trace)
        print(f"Found {len(documents)} relevant documents")
        
        # Step 2: Assemble context
        print("🔧 Assembling context...")
        context = assemble_context(documents, query, trace=trace)
        
        # Step 3: Generate answer
        print("🤖 Generating answer...")
        answer = generate_answer(context, trace=trace)
        
        result = {
            "query": query,
            "retrieved_documents": documents,
            "context": context,
            "answer": answer
        }
        
        # Update trace with final result
        trace.update(name="rag_pipeline", output=result, metadata={"doc_count": len(documents)})
        
        return result
    finally:
        trace.end()

def run_rag_demo():
    """
    Run RAG demo with sample queries
    """
    print("🧠 RAG (Retrieval Augmented Generation) Demo")
    print("=" * 60)
    
    sample_queries = [
        "What is Kubernetes and how does it help with container orchestration?",
        "How can I implement observability in my microservices architecture?",
        "What are the key principles of DevOps and how do they apply to cloud-native development?",
        "Explain the benefits and challenges of microservices architecture"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n{'='*20} Query {i} {'='*20}")
        
        # Add realistic delay
        time.sleep(random.uniform(2, 4))
        
        result = rag_pipeline(query)
        
        print(f"\n📝 Answer:")
        print(result["answer"])
        print(f"\n📊 Retrieved {len(result['retrieved_documents'])} documents")
        print("-" * 60)
    
    print("\n✅ RAG demo completed! Check Langfuse dashboard for detailed traces.")

if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your environment or .env file")
        exit(1)
    
    if not os.getenv("LANGFUSE_PUBLIC_KEY"):
        print("❌ Please set LANGFUSE_PUBLIC_KEY in your environment or .env file")
        exit(1)
    
    run_rag_demo()
    
    # Flush any remaining traces
    langfuse.flush()
