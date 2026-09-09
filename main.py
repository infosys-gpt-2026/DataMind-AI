from dotenv import load_dotenv

from chains.router import route_question

from memory.conversation_memory import (
    add_user_message,
    add_ai_message,
    get_chat_history,
    clear_chat_history,
)


load_dotenv()


def main():

    print("\n" + "=" * 60)
    print("🤖 Welcome to DataMind AI")
    print("📊 Your AI-Powered Data Analyst")
    print("=" * 60)

    while True:

        question = input(
            "\n💬 Ask a question "
            "(or type 'exit', 'clear'): "
        )

        # Exit
        if question.lower() in ["exit", "quit", "bye"]:
            print("\n👋 Thank you for using DataMind AI!")
            break

        # Clear conversation
        if question.lower() == "clear":
            clear_chat_history()
            print("\n🧹 Conversation memory cleared.")
            continue

        # Empty question
        if not question.strip():
            print("⚠️ Please enter a valid question.")
            continue

        print("\n🔍 DataMind AI is analyzing...")

        try:

            # Get previous conversation
            chat_history = get_chat_history()

            # Route question
            intent, response = route_question(
                question,
                chat_history=chat_history
            )

            print(
                f"🧠 Detected Intent: {intent.upper()}"
            )

            print("\n🤖 DataMind AI Response:\n")
            print(response)

            # Save conversation only after success
            add_user_message(question)
            add_ai_message(response)

        except Exception as error:

            print("\n❌ An error occurred:")
            print(error)


if __name__ == "__main__":
    main()