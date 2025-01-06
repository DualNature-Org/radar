# File: chatgpt_api.py
import openai

class ChatGPTAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def evaluate_objective(self, content, objective):
        """
        Evaluate if the objective is met in the given content.

        Parameters:
        - content (str): The textual content to evaluate.
        - objective (str): The objective to check against the content.

        Returns:
        - tuple (bool, float): A tuple containing:
            - A boolean indicating if the objective is met.
            - A prediction score (percentage) of relevance.
        """
        try:
            prompt = (
                "Given the following content, determine if the objective is met. "
                "Provide a clear answer (yes or no) and a prediction score as a percentage of how likely the objective is met.\n"
                "Content: {content}\n"
                "Objective: {objective}\n"
                "Response format: 'Answer: <yes/no>, Prediction Score: <percentage>'"
            ).format(content=content[:5000], objective=objective)  # Limit to 5000 characters for API input size

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )

            output = response.choices[0].text.strip()
            # Parse the response
            if "Answer: yes" in output.lower():
                answer = True
            else:
                answer = False

            # Extract prediction score
            try:
                score_str = output.split("Prediction Score:")[1].strip().replace("%", "")
                prediction_score = float(score_str) / 100
            except (IndexError, ValueError):
                prediction_score = 0.0

            return answer, prediction_score

        except Exception as e:
            print(f"Error during ChatGPT API call: {e}")
            return False, 0.0

# Example usage
if __name__ == "__main__":
    api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key
    chatgpt_api = ChatGPTAPI(api_key)

    content = "This is a sample content about data mining and its applications."
    objective = "Find if this content explains data mining techniques."

    is_met, score = chatgpt_api.evaluate_objective(content, objective)
    print(f"Objective met: {is_met}, Prediction score: {score * 100}%")
