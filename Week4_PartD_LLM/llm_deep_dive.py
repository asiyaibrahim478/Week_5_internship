"""
Week 4 — Part D: LLM APIs In Depth Demonstration Script
Author: Asiya
Topics: Conversation History, Streaming, Temperature Comparison, and Structured JSON Parsing.
"""

import json
import time

def demo_conversation_history():
    print("--- 1. Multi-turn Conversation History Demo ---")
    history = [
        {"role": "user", "content": "Hello! My name is Asiya and I am working on the Library AI Project."}
    ]
    # Simulated Assistant Response 1
    assistant_reply = "Hello Asiya! Nice to meet you. How can I help with your Library AI Project today?"
    history.append({"role": "assistant", "content": assistant_reply})
    
    # Follow-up User Message relying on context
    history.append({"role": "user", "content": "What is my name and what project am I working on?"})
    print(f"Full Conversation Payload Sent ({len(history)} messages):")
    for msg in history:
        print(f"  [{msg['role'].upper()}]: {msg['content']}")
    
    # Model uses the whole payload to recall context
    simulated_reply = "Your name is Asiya, and you are working on the Library AI Project!"
    print(f"\nModel Output: {simulated_reply}\n")


def demo_streaming_simulation():
    print("--- 2. Token Streaming Demo ---")
    text = "Streaming sends tokens incrementally as they are generated, improving perceived latency for users."
    print("Streaming output: ", end="", flush=True)
    for word in text.split(" "):
        print(word + " ", end="", flush=True)
        time.sleep(0.08)
    print("\n[Stream finished]\n")


def demo_temperature_comparison():
    print("--- 3. Temperature 0 vs Temperature 1 Comparison ---")
    prompt = "Suggest a title for a sci-fi book about quantum time travel."
    
    print(f"Prompt: \"{prompt}\"")
    print("Temperature = 0.0 (Deterministic, Greedy):")
    print("  Run 1 -> 'The Quantum Paradox'")
    print("  Run 2 -> 'The Quantum Paradox'")
    
    print("Temperature = 1.0 (Varied, Exploratory):")
    print("  Run 1 -> 'Chronicles of the Entangled Horizon'")
    print("  Run 2 -> 'Echoes from the Tachyon Rift'\n")


def demo_structured_json_output():
    print("--- 4. Structured JSON Output & Safe Parsing Demo ---")
    mock_llm_response = '{"genre": "Science Fiction", "summary": "A thrilling exploration into parallel dimensions where a lone librarian discovers books detailing future timelines."}'
    
    try:
        data = json.loads(mock_llm_response)
        print("Successfully parsed structured JSON:")
        print(f"  Genre: {data.get('genre')}")
        print(f"  Summary: {data.get('summary')}")
    except json.JSONDecodeError as err:
        print(f"Failed to parse LLM response: {err}")


if __name__ == "__main__":
    print("=====================================================")
    print("    WEEK 4 — LLM API CONCEPTS & PATTERNS (Asiya)    ")
    print("=====================================================\n")
    demo_conversation_history()
    demo_streaming_simulation()
    demo_temperature_comparison()
    demo_structured_json_output()
