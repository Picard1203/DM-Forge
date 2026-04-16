"""Tests for spaced repetition review endpoints."""

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient

from src.models.curriculum import Module
from src.models.review_card import ReviewCard, UserCardReview


async def _seed_cards(module: Module, count: int = 3) -> list:
    """Insert review cards for a module and return them.

    Args:
        module (Module): The module to associate cards with.
        count (int): Number of cards to create.

    Returns:
        list: List of inserted ReviewCard documents.
    """
    cards = []
    for idx in range(count):
        card = ReviewCard(
            module_id=str(module.id),
            front=f"Front of card {idx}",
            back=f"Back of card {idx}",
            tags=["test"],
        )
        await card.insert()
        cards.append(card)
    return cards


@pytest.mark.asyncio
async def test_get_due_cards_returns_overdue_only(
    client: AsyncClient,
    auth_token: str,
    mock_user,
    seeded_curriculum: dict,
) -> None:
    """GET /review/due returns overdue cards and never-reviewed cards only."""
    module = seeded_curriculum["rules-fundamentals"]
    cards = await _seed_cards(module, count=3)
    past_time = datetime.now(UTC) - timedelta(days=5)
    overdue_review = UserCardReview(
        user_id=str(mock_user.id),
        card_id=str(cards[0].id),
        next_review=past_time,
    )
    await overdue_review.insert()
    future_time = datetime.now(UTC) + timedelta(days=5)
    future_review = UserCardReview(
        user_id=str(mock_user.id),
        card_id=str(cards[1].id),
        next_review=future_time,
    )
    await future_review.insert()
    response = await client.get(
        "/api/v1/review/due",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    due_ids = [item["id"] for item in response.json()]
    assert str(cards[0].id) in due_ids
    assert str(cards[2].id) in due_ids
    assert str(cards[1].id) not in due_ids


@pytest.mark.asyncio
async def test_submit_review_updates_interval(
    client: AsyncClient,
    auth_token: str,
    mock_user,
    seeded_curriculum: dict,
) -> None:
    """POST /review/submit with quality=4 creates a review record and sets interval."""
    module = seeded_curriculum["rules-fundamentals"]
    cards = await _seed_cards(module, count=1)
    card = cards[0]
    response = await client.post(
        "/api/v1/review/submit",
        json={"card_id": str(card.id), "quality": 4},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["interval_days"] == 1
    assert data["ease_factor"] > 2.0
    assert "next_review" in data
    saved = await UserCardReview.find_one(
        UserCardReview.user_id == str(mock_user.id),
        UserCardReview.card_id == str(card.id),
    )
    assert saved is not None
    assert saved.repetitions == 1


@pytest.mark.asyncio
async def test_sm2_quality_zero_resets_interval(
    client: AsyncClient,
    auth_token: str,
    mock_user,
    seeded_curriculum: dict,
) -> None:
    """Quality=0 review resets interval to 1 day and repetitions to 0."""
    module = seeded_curriculum["rules-fundamentals"]
    cards = await _seed_cards(module, count=1)
    card = cards[0]
    existing_review = UserCardReview(
        user_id=str(mock_user.id),
        card_id=str(card.id),
        repetitions=5,
        interval_days=30,
        ease_factor=2.5,
        next_review=datetime.now(UTC) - timedelta(days=1),
    )
    await existing_review.insert()
    response = await client.post(
        "/api/v1/review/submit",
        json={"card_id": str(card.id), "quality": 0},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["interval_days"] == 1
    saved = await UserCardReview.find_one(
        UserCardReview.user_id == str(mock_user.id),
        UserCardReview.card_id == str(card.id),
    )
    assert saved is not None
    assert saved.repetitions == 0
    assert saved.interval_days == 1
