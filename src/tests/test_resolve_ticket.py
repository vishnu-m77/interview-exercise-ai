import subprocess
import json
import pytest

def resolve_ticket(request_text: str):
    cmd = [
        "curl", "-s", "-X", "POST", "http://localhost:8000/resolve-ticket",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(request_text)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

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
    response = resolve_ticket(request_text)
    assert "action_required" in response, f"Missing action_required in response: {response}"
    assert response["action_required"] == expected_action, f"Unexpected action: {response}"
