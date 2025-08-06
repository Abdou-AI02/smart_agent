class TaskSequencer:
    def __init__(self, agent):
        self.agent = agent

    def execute_sequence(self, tasks):
        """Executes a sequence of tasks."""
        results = []
        for i, task in enumerate(tasks):
            self.agent.add_log(f"Executing Task {i+1}: {task}")
            result = self.agent.process_command(task)
            results.append(result)
            self.agent.add_log(f"Task {i+1} Result: {result}")
        return results

    def plan_and_execute(self, objective):
        """Uses the LLM to plan tasks for a given objective and then executes them."""
        self.agent.add_log(f"Planning tasks for objective: {objective}")
        planning_prompt = f"""
        Given the objective: "{objective}", break it down into a sequence of simple, actionable steps.
        Each step should be a clear command that the agent can understand and execute.
        List each step on a new line, prefixed with a number and a period (e.g., "1. First step.").
        If the objective is simple, just return it as a single step.
        """
        plan_response = self.agent.llm_manager.generate_response(planning_prompt, self.agent.memory_manager.get_history())
        
        tasks = [line.strip() for line in plan_response.split('\n') if line.strip().startswith(tuple(str(i) + '.' for i in range(1, 10)))]
        
        if not tasks:
            self.agent.add_log("Could not generate a clear plan. Attempting to execute objective directly.")
            tasks = [objective]

        self.agent.add_log(f"Generated Plan: {tasks}")
        return self.execute_sequence(tasks)