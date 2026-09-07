from dotenv import load_dotenv

from chains.router import (
    detect_intent,
    get_chain,
)

from agents.analyst_agent import (
    run_analyst_agent,
)


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


        # Exit condition
        if question.lower() in [
            "exit",
            "quit",
            "bye",
        ]:

            print(
                "\n👋 Thank you for using DataMind AI!"
            )

            break


        # Empty input
        if not question.strip():

            print(
                "⚠️ Please enter a valid question."
            )

            continue


        print(
            "\n🔍 DataMind AI is analyzing..."
        )


        try:

            # Detect intent
            intent = detect_intent(question)

            print(
                f"🧠 Detected Intent: {intent.upper()}"
            )

            print(
                "\n🤖 DataMind AI Response:\n"
            )


            # ==========================
            # ANALYST AGENT
            # ==========================

            if intent == "analyst":

                response = run_analyst_agent(
                    question
                )


            # ==========================
            # OTHER CHAINS
            # ==========================

            else:

                chain = get_chain(intent)

                response = chain.invoke( # pyright: ignore[reportOptionalMemberAccess]
                    {
                        "question": question
                    }
                )


            print(response)


        except Exception as error:

            print(
                "\n❌ An error occurred:"
            )

            print(error)


if __name__ == "__main__":

    main()