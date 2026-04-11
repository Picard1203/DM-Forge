"""Tests for authentication endpoints: register, login, and /me."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient) -> None:
    """Registering with a unique email and username returns 201 + token."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@dmforge.com",
            "username": "NewUser",
            "password": "Str0ngPass!",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, mock_user) -> None:
    """Registering with an already-used email returns 409 Conflict."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "hero@dmforge.com",
            "username": "AnotherUser",
            "password": "Str0ngPass!",
        },
    )
    assert response.status_code == 409
    assert "email" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, mock_user) -> None:
    """Registering with an already-taken username returns 409 Conflict."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "different@dmforge.com",
            "username": "HeroUser",
            "password": "Str0ngPass!",
        },
    )
    assert response.status_code == 409
    assert "username" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, mock_user) -> None:
    """Login with correct credentials returns 200 + token."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "hero@dmforge.com", "password": "Str0ngPass!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, mock_user) -> None:
    """Login with incorrect password returns 401 Unauthorized."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "hero@dmforge.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient) -> None:
    """Login with an unregistered email returns 401 Unauthorized."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "ghost@dmforge.com", "password": "Str0ngPass!"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_valid_token(client: AsyncClient, auth_token: str) -> None:
    """/me with a valid Bearer token returns the authenticated user's profile."""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "hero@dmforge.com"
    assert body["username"] == "HeroUser"


@pytest.mark.asyncio
async def test_me_with_invalid_token(client: AsyncClient) -> None:
    """/me with a forged Bearer token returns 401 Unauthorized."""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer this.is.not.valid"},
    )
    assert response.status_code == 401
