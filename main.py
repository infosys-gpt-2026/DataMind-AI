from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from chains.router import route_question


load_dotenv()


def main():

    print("\n" + "=" * 60)
    print("🤖 Welcome to DataMind AI")
    print("📊 Your AI-Powered Data Analyst")
    print("=" * 60)

    chat_history = []

    while True:

        question = input("\n💬 Ask a question (or type 'exit'): ").strip()

        if question.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Thank you for using DataMind AI!")
            break

        if not question:
            print("⚠️ Please enter a valid question.")
            continue

        print("\n🔍 DataMind AI is analyzing...")

        try:
            intent, response = route_question(question, chat_history=chat_history)

            print(f"🧠 Detected Intent: {intent.upper()}")
            print("\n🤖 DataMind AI Response:\n")
            print(response)

            # Only the analyst path uses/benefits from history, but tracking
            # every turn keeps things simple and consistent.
            chat_history.append(HumanMessage(content=question))
            chat_history.append(AIMessage(content=response))

        except Exception as error:
            print("\n❌ An error occurred:")
            print(error)


if __name__ == "__main__":
    main()