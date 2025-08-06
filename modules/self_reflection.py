class SelfReflection:
    def __init__(self, llm_manager, memory_manager):
        self.llm_manager = llm_manager
        self.memory_manager = memory_manager

    def reflect_on_performance(self, last_interaction, overall_feedback=""):
        """
        Prompts the LLM to reflect on its recent performance or overall interaction.
        """
        history = self.memory_manager.get_history()
        reflection_prompt = f"""
        Analyze the following last interaction: "{last_interaction}".
        Consider the overall conversation history.
        Identify any potential misunderstandings, errors, or areas for improvement in your response.
        Suggest how you could have responded better or what information you might need in the future.
        Also, consider this overall feedback if provided: "{overall_feedback}".
        Provide a concise self-reflection and actionable insights.
        """
        reflection_response = self.llm_manager.generate_response(reflection_prompt, history)
        return reflection_response

    def analyze_error(self, error_message, context=""):
        """Asks the LLM to analyze a specific error message."""
        history = self.memory_manager.get_history()
        error_analysis_prompt = f"""
        An error occurred: "{error_message}".
        Context: "{context}".
        Based on the current conversation and this error, can you explain what might have gone wrong?
        Suggest possible reasons and potential steps to resolve it or avoid it in the future.
        """
        error_analysis_response = self.llm_manager.generate_response(error_analysis_prompt, history)
        return error_analysis_response