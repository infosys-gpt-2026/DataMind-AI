from dotenv import load_dotenv

from chains.router import route_question


load_dotenv()


def main():

    print("\n" + "=" * 60)
    print("🤖 Welcome to DataMind AI")
    print("📊 Your AI-Powered Data Analyst")
    print("=" * 60)

    while True:

        question = input(
            "\n💬 Ask a question (or type 'exit'): "
        )

        if question.lower() in [
            "exit",
            "quit",
            "bye",
        ]:

            print("\n👋 Thank you for using DataMind AI!")
            break

        if not question.strip():

            print("⚠️ Please enter a valid question.")
            continue

        print("\n🔍 DataMind AI is analyzing...")

        try:

            intent, response = route_question(question)

            print(
                f"🧠 Detected Intent: {intent.upper()}"
            )

            print("\n🤖 DataMind AI Response:\n")

            print(response)

        except Exception as error:

            print("\n❌ An error occurred:")
            print(error)


if __name__ == "__main__":

    main()