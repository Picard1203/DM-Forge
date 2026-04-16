"""Seeder: load quiz YAML files and upsert Quiz documents."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.models.curriculum import Module
from src.models.quiz import Quiz, QuizQuestion


async def seed_quizzes() -> None:
    """Read every YAML under curriculum/quizzes/ and upsert by slug.

    Resolves module_slug to a module_id before inserting. Skips any quiz
    whose module cannot be found.

    Returns:
        None
    """
    quiz_dir = Path(__file__).resolve().parents[3] / "curriculum" / "quizzes"
    if not quiz_dir.exists():
        return
    yaml_files = sorted(quiz_dir.glob("*.yaml"))
    for yaml_path in yaml_files:
        await _seed_file(yaml_path)


async def _seed_file(yaml_path: Path) -> None:
    """Load one YAML file and upsert each quiz entry.

    Args:
        yaml_path (Path): Absolute path to the YAML file.

    Returns:
        None
    """
    with open(yaml_path, "r", encoding="utf-8") as file_handle:
        data: Dict[str, Any] = yaml.safe_load(file_handle)
    quiz_entries: List[Dict[str, Any]] = data.get("quizzes", [])
    for entry in quiz_entries:
        await _upsert_quiz(entry)


async def _upsert_quiz(entry: Dict[str, Any]) -> None:
    """Insert or update a single Quiz document from a YAML entry.

    Args:
        entry (Dict[str, Any]): Parsed YAML dictionary for one quiz.

    Returns:
        None
    """
    module_slug: str = entry.get("module_slug", "")
    module: Optional[Module] = await Module.find_one(Module.slug == module_slug)
    if module is None:
        return
    slug: str = entry.get("slug", "")
    existing: Optional[Quiz] = await Quiz.find_one(Quiz.slug == slug)
    questions: List[QuizQuestion] = _parse_questions(entry.get("questions", []))
    if existing is not None:
        existing.module_id = str(module.id)
        existing.title = entry.get("title", existing.title)
        existing.description = entry.get("description", existing.description)
        existing.passing_score = float(entry.get("passing_score", existing.passing_score))
        existing.xp_reward = int(entry.get("xp_reward", existing.xp_reward))
        existing.questions = questions
        await existing.save()
    else:
        quiz = Quiz(
            slug=slug,
            module_id=str(module.id),
            title=entry.get("title", ""),
            description=entry.get("description", ""),
            passing_score=float(entry.get("passing_score", 0.7)),
            xp_reward=int(entry.get("xp_reward", 50)),
            questions=questions,
        )
        await quiz.insert()


def _parse_questions(raw_questions: List[Dict[str, Any]]) -> List[QuizQuestion]:
    """Convert a list of raw YAML question dicts to QuizQuestion instances.

    Args:
        raw_questions (List[Dict[str, Any]]): List of question dicts from YAML.

    Returns:
        List[QuizQuestion]: Parsed QuizQuestion embedded model instances.
    """
    questions: List[QuizQuestion] = []
    for raw in raw_questions:
        questions.append(
            QuizQuestion(
                question_text=raw.get("question_text", ""),
                question_type=raw.get("question_type", "multiple_choice"),
                options=raw.get("options", []),
                correct_answer_index=int(raw.get("correct_answer_index", 0)),
                explanation=raw.get("explanation", ""),
                scenario_context=raw.get("scenario_context"),
            )
        )
    return questions
