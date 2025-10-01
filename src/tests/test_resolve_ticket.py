import pytest
from src.api import resolve_ticket, initialize_data

@pytest.fixture(autouse=True)
def setup_vector_store():
    initialize_data()

@pytest.mark.parametrize("request_text, expected_action", [
    (
        "My domain was suspended and I didn't get any notice. How can I reactivate it?",
        "escalate_to_abuse_team"
    ),
    (
        "I was charged for a domain renewal I didn't authorize. I want a refund.",
        "escalate_to_billing_team"
    ),
    (
        "I represent the trademark holder for BrandX. One of your customers is infringing on our trademark with their domain name.",
        "escalate_to_legal_team"
    ),
    (
        "All of my customers are reporting that our website is down. DNS lookups are failing intermittently.",
        "escalate_to_operations_team"
    ),
    (
        "My site was down earlier but now it's back online. No action required.",
        "resolved"
    )
])

def test_resolve_ticket(request_text, expected_action):
    response = resolve_ticket({"ticket_text": request_text})
    assert "action_required" in response, f"Missing action_required in response: {response}"
    assert response["action_required"] == expected_action, f"Unexpected action: {response}"
