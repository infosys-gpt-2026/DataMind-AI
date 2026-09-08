def handle_ai_error(error):

    error_message = str(error)

    if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:

        return """
⚠️ Gemini API quota has been exceeded.

Please wait for the quota to reset or change the Gemini model/API plan.

Your DataMind AI application is working correctly — this is an API quota limitation.
"""

    return f"""
❌ An error occurred:

{error_message}
"""