from langchain_core.messages import HumanMessage, AIMessage

from agents.analyst_agent import analyst_agent_executor # pyright: ignore[reportAttributeAccessIssue]

print("\n" + "=" * 60)
print("🤖 Welcome to DataMind AI")
print("📊 Your AI-Powered Data Analyst (now with real data access)")
print("=" * 60)
print("💡 Tip: ask it to load a CSV first, e.g.")
print("   'Load data/sample_sales.csv and summarize it'")

chat_history = []

while True:
    question = input("\n💬 Ask a question (or type 'exit'): ")

    if question.lower() in ["exit", "quit", "bye"]:
        print("\n👋 Thank you for using DataMind AI!")
        break

    if not question.strip():
        print("⚠️ Please enter a question.")
        continue

    print("\n🔍 DataMind AI is analyzing...\n")

    try:
        response = analyst_agent_executor.invoke(
            {"question": question, "chat_history": chat_history}
        )
        output = response["output"]
        print(output)

        # Remember this turn so the agent has real context on the next question
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=output))

    except Exception as error:
        print("\n❌ An error occurred:")
        print(error)

    print("\n" + "=" * 60)