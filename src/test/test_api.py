import re


def test_check_health(client):

    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_create_api_key(logged_in_client):
    response = logged_in_client.post("/dashboard/keys", 
    data={
        "name": "test key"
    })

    assert response.status_code == 302

# test a non routes function but needs existing user
def test_get_all_api_keys(app, registered_user):
    from app.services.api_key_service import create_api_key, get_all_api_keys

    with app.app_context():
        create_api_key(
            user_id=registered_user,
            name="testapi"
        )

        keys = get_all_api_keys(registered_user)
        assert len(keys) == 1