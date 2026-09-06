from chains.analyst_chain import analyst_chain


print("\n" + "=" * 60)
print("🤖 Welcome to DataMind AI")
print("📊 Your AI-Powered Data Analyst")
print("=" * 60)


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

        response = analyst_chain.invoke(
            {
                "question": question
            }
        )

        print(response)

    except Exception as error:

        print("\n❌ An error occurred:")
        print(error)

    print("\n" + "=" * 60)