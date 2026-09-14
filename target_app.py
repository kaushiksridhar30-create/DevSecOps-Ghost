# target_app.py
"""User Data Processing Module"""


def process_user_data(payload):
    """
    Processes user payload and returns uppercase user name.
    Gracefully handles missing 'user' dictionary or 'name' keys.
    """
    if not isinstance(payload, dict):
        return "GUEST"

    user_data = payload.get("user")
    if not isinstance(user_data, dict):
        return "GUEST"

    user_name = user_data.get("name", "Guest")
    if not isinstance(user_name, str):
        return "GUEST"

    return user_name.upper()


def run_test():
    """Run test cases."""
    normal_payload = {"user": {"name": "alice"}}
    result1 = process_user_data(normal_payload)
    assert result1 == "ALICE"

    edge_case_payload = {}
    result2 = process_user_data(edge_case_payload)
    assert result2 == "GUEST"

    edge_case_payload_2 = {"user": None}
    result3 = process_user_data(edge_case_payload_2)
    assert result3 == "GUEST"

    edge_case_payload_3 = {"user": {}}
    result4 = process_user_data(edge_case_payload_3)
    assert result4 == "GUEST"


if __name__ == "__main__":
    run_test()
