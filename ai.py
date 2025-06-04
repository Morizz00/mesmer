class AI:
    def __init__(self):
        # Define simple rule-based responses
        self.responses = {
            "hello": "Hi there! How can I help you today?",
            "how are you": "I’m doing great, thanks for asking! How about you?",
            "what is your name": "I’m your AI voice companion, here to assist you.",
            "bye": "Goodbye! Have a great day!"
        }

    def generate_response(self, text: str) -> str:
        """
        Generate a response based on the input text.
        For now, use a simple keyword-based approach.
        """
        text = text.lower().strip()
        for keyword, response in self.responses.items():
            if keyword in text:
                return response
        return "I’m not sure how to respond to that. Can you say something else?"

ai_service = AI()