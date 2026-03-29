"""
Tests for feedback routes and CRUD operations.
Uses shared fixtures from conftest.py for database and client setup.
"""

import pytest


@pytest.mark.unit
def test_create_feedback(client, test_user):
    """Test feedback creation"""
    response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "Improve UI",
            "description": "Add dark mode to improve user experience"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Improve UI"
    assert data["description"] == "Add dark mode to improve user experience"
    assert data["user_id"] == test_user['id']


@pytest.mark.unit
def test_create_feedback_missing_user(client):
    """Test feedback creation fails with non-existent user"""
    response = client.post(
        "/feedback/?user_id=9999",
        json={
            "title": "Test Feedback",
            "description": "This should fail because user doesn't exist"
        }
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


@pytest.mark.unit
def test_create_feedback_empty_title(client, test_user):
    """Test feedback creation fails with empty title"""
    response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "",
            "description": "Description without title"
        }
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_create_feedback_empty_description(client, test_user):
    """Test feedback creation fails with empty description"""
    response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "Valid Title",
            "description": ""
        }
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_get_all_feedback(client, test_user, test_feedback):
    """Test getting all feedback"""
    response = client.get("/feedback/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.unit
def test_get_all_feedback_empty(client):
    """Test getting all feedback when none exist"""
    response = client.get("/feedback/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.unit
def test_get_all_feedback_with_pagination(client):
    """Test getting feedback with pagination parameters"""
    response = client.get("/feedback/?skip=0&limit=10")
    assert response.status_code == 200


@pytest.mark.unit
def test_get_all_feedback_invalid_skip(client):
    """Test getting feedback with invalid skip parameter"""
    response = client.get("/feedback/?skip=-1")
    assert response.status_code == 400


@pytest.mark.unit
def test_get_all_feedback_invalid_limit(client):
    """Test getting feedback with invalid limit parameter"""
    response = client.get("/feedback/?limit=101")
    assert response.status_code == 400


@pytest.mark.unit
def test_get_feedback_by_id(client, test_feedback):
    """Test getting feedback by ID"""
    response = client.get(f"/feedback/{test_feedback['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_feedback['id']
    assert data["title"] == test_feedback['title']


@pytest.mark.unit
def test_get_feedback_by_id_not_found(client):
    """Test getting non-existent feedback"""
    response = client.get("/feedback/9999")
    assert response.status_code == 404
    assert "Feedback not found" in response.json()["detail"]


@pytest.mark.unit
def test_get_feedback_by_id_invalid(client):
    """Test getting feedback with invalid ID"""
    response = client.get("/feedback/0")
    assert response.status_code == 400


@pytest.mark.unit
def test_invalid_feedback_creation(client, test_user):
    """Test invalid input validation"""
    # Empty title
    response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "",
            "description": "Add dark mode"
        }
    )
    # Should fail validation
    assert response.status_code in [422, 400]
    
    # Empty description
    response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "Improve UI",
            "description": ""
        }
    )
    assert response.status_code in [422, 400]


@pytest.mark.unit
def test_pagination(client):
    """Test pagination parameters"""
    # Invalid skip
    response = client.get("/feedback/?skip=-1")
    assert response.status_code == 400
    
    # Invalid limit
    response = client.get("/feedback/?limit=0")
    assert response.status_code == 400
    
    # Invalid limit (too large)
    response = client.get("/feedback/?limit=101")
    assert response.status_code == 400
    
    # Valid parameters
    response = client.get("/feedback/?skip=0&limit=10")
    assert response.status_code == 200


@pytest.mark.unit
def test_feedback_not_found(client):
    """Test getting non-existent feedback"""
    response = client.get("/feedback/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.unit
def test_invalid_feedback_id(client):
    """Test invalid feedback ID"""
    response = client.get("/feedback/-1")
    assert response.status_code == 400
    
    response = client.get("/feedback/0")
    assert response.status_code == 400
