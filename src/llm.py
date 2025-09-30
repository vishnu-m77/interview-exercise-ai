import openai
from .config import settings

class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key = settings.openai_api_key)
        self.model = settings.text_completion_model

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model= self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful Knowledge Assistant that can analyze customer support queries and return structured, relevant, and helpful responses. Always respond with valid JSON only, no additional text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"Error with OpenAI API: {str(e)}"
        except Exception as e:
            return f"Unexpected Error with OpenAI API: {str(e)}"
    
PROMPT_TEMPLATE = """Analyze the customer query and provide a response using the context documents. 

Context Documents:
{context_text}

Customer Query: {query}

You must respond with ONLY a valid JSON object in this exact format:
{{
    "answer": "Provide a detailed, helpful response based on the context.",
    "references": ["List of specific document references like 'Source: Document Title, Section X.Y'."],
    "action_required": "Choose exactly one: escalate_to_abuse_team, escalate_to_billing_team, escalate_to_legal_team, escalate_to_operations_team, or resolved"
}}

Rules:
- The answer should be comprehensive and helpful
- References should be specific and cite actual documents from the context
- action_required must be one of the five specified values:
    * escalate_to_abuse_team: polivy violations, missing WHOIS, spam, phishing, malware, or other abuse-related violations.
    * escalate_to_billing_team: failed payments, refunds, renewal disputes, or chargebacks.
    * escalate_to_legal_team: copyright claims, DMCA takedowns, subpoenas, or trademark disputes.
    * escalate_to_operations_team: infrastructure outages, DNS failures, or systemic technical issues.
    * resolved: Issue can be resolved with provided information.
- When in doubt, always escalate to the most relevant team.
- During potential policy violations and missing WHOIS, escalate to the abuse team even if issue can be resolved by the user
so that the team can keep track of such cases.
- Respond with ONLY the JSON object, no additional text"""
