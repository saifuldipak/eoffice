import pytest

def test_create_role(client, auth_headers):
    """Test successfully creating a new role."""
    role_data = {
        "name": "test_role",
        "description": "A test role for testing"
    }
    
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == role_data["name"]
    assert data["description"] == role_data["description"]
    assert "id" in data

def test_create_duplicate_role(client, auth_headers):
    """Test that creating a duplicate role returns an error."""
    role_data = {
        "name": "duplicate_role",
        "description": "This role should only be created once"
    }
    
    # Create the role first time
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 200
    
    # Attempt to create the same role again
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Role with this name already exists"

def test_create_role_missing_name(client, auth_headers):
    """Test that creating a role without a name returns a validation error."""
    role_data = {
        "description": "A role without a name"
    }
    
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"][-1] == "name"

def test_create_role_empty_description(client, auth_headers):
    """Test that creating a role with empty description is allowed."""
    role_data = {
        "name": "no_description_role",
        "description": None
    }
    
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == role_data["name"]
    assert data["description"] is None

def test_create_role_without_description_field(client, auth_headers):
    """Test that creating a role without including the description field succeeds."""
    role_data = {
        "name": "minimal_role"
        # description field is completely omitted
    }
    
    response = client.post("/users/roles/", json=role_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == role_data["name"]
    # Check that the API assigns a default value (likely null/None) when field is omitted
    assert "description" in data