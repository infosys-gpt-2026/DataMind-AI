from agents.analyst_agent import analyst_agent_executor # pyright: ignore[reportMissingImports]

print("\n" + "=" * 60)
print("🤖 Welcome to DataMind AI")
print("📊 Your AI-Powered Data Analyst (now with real data access)")
print("=" * 60)
print("💡 Tip: ask it to load a CSV first, e.g.")
print("   'Load data/sample_sales.csv and summarize it'")

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
        response = analyst_agent_executor.invoke({"question": question})
        print(response["output"])
    except Exception as error:
        print("\n❌ An error occurred:")
        print(error)

    print("\n" + "=" * 60)