"""
Tests for vote routes and CRUD operations.
Uses shared fixtures from conftest.py for database and client setup.
"""

import pytest


@pytest.mark.unit
def test_create_upvote(client, test_user, another_user, test_feedback):
    """Test upvote creation"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["feedback_id"] == test_feedback['id']
    assert data["user_id"] == another_user['id']
    assert data["vote_type"] == "upvote"


@pytest.mark.unit
def test_create_downvote(client, test_user, another_user, test_feedback):
    """Test downvote creation"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "downvote"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["vote_type"] == "downvote"


@pytest.mark.unit
def test_cannot_vote_on_own_feedback(client, test_user, test_feedback):
    """Test that user cannot vote on their own feedback"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": test_user['id'],
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 400
    assert "Cannot vote on your own feedback" in response.json()["detail"]


@pytest.mark.unit
def test_cannot_vote_nonexistent_feedback(client, another_user):
    """Test voting on non-existent feedback"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 9999,
            "user_id": another_user['id'],
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 404
    assert "Feedback not found" in response.json()["detail"]


@pytest.mark.unit
def test_cannot_vote_nonexistent_user(client, test_feedback):
    """Test voting as non-existent user"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": 9999,
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


@pytest.mark.unit
def test_update_vote_type(client, test_user, another_user, test_feedback):
    """Test changing vote type (upvote to downvote)"""
    # Create upvote
    response1 = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "upvote"
        }
    )
    assert response1.status_code == 201
    
    # Change to downvote (should update instead of creating duplicate)
    response2 = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "downvote"
        }
    )
    assert response2.status_code == 201
    data = response2.json()
    assert data["vote_type"] == "downvote"


@pytest.mark.unit
def test_get_top_ideas(client, test_user, another_user, test_feedback):
    """Test getting top voted ideas"""
    # Vote on feedback
    client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "upvote"
        }
    )
    
    response = client.get("/vote/top/?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.unit
def test_get_top_ideas_with_limit(client):
    """Test getting top ideas with custom limit"""
    response = client.get("/vote/top/?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.unit
def test_get_top_ideas_invalid_limit(client):
    """Test getting top ideas with invalid limit"""
    response = client.get("/vote/top/?limit=101")
    assert response.status_code == 400
    
    response = client.get("/vote/top/?limit=0")
    assert response.status_code == 400


@pytest.mark.unit
def test_invalid_vote_type(client, test_user, another_user, test_feedback):
    """Test voting with invalid vote type"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "invalid"
        }
    )
    assert response.status_code == 422


@pytest.mark.integration
def test_vote_count_accuracy(client, test_user, another_user, test_feedback):
    """Test that vote counts are accurate"""
    # Create multiple votes
    client.post(
        "/vote/",
        json={
            "feedback_id": test_feedback['id'],
            "user_id": another_user['id'],
            "vote_type": "upvote"
        }
    )
    
    # Get top ideas to verify count
    response = client.get("/vote/top/?limit=10")
    assert response.status_code == 200
    ideas = response.json()
    
    # Find our test feedback in the list
    test_feedback_in_list = next((idea for idea in ideas if idea['id'] == test_feedback['id']), None)
    if test_feedback_in_list:
        assert test_feedback_in_list['upvotes'] >= 1
