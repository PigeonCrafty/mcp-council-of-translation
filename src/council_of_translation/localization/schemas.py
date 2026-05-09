from typing import Literal, TypedDict


ReviewMode = Literal["lightweight", "standard", "strict"]
OutputMode = Literal["review_only", "with_snippets", "full_rewrite"]
ConflictReviewMode = Literal["off", "auto", "always"]
ReviewerVerdict = Literal["通过", "有保留通过", "不通过"]
Publishability = Literal["可发布", "修改后可发布", "需人工复核"]
Confidence = Literal["高", "中", "低"]


class TranslationReviewTask(TypedDict, total=False):
    task_id: str
    source_text: str
    candidate_translation: str
    source_language: str
    target_language: str
    content_type: str
    context: str
    audience: str
    mode: ReviewMode
    output_mode: OutputMode
    enable_conflict_review: ConflictReviewMode
    max_examples: int
    max_conflicts: int
    term_glossary: str
    style_guide: str
    project_rules: str
    brand_guidelines: str
    technical_constraints: str
    reference_translations: str
    known_exceptions: str
    notes: str


class ReviewResult(TypedDict):
    agent_name: str
    role: str
    verdict: ReviewerVerdict
    issues: list[str]
    suggestions: list[str]
    recommended_translation: str
    confidence: Confidence
    rationale: str


class ChiefEditorDecision(TypedDict):
    publishability: Publishability
    must_fix: list[str]
    optional_improvements: list[str]
    recommended_translation: str
    alternatives: list[str]
    decision_rationale: str
    review_needed: Literal["是", "否"]
    review_reason: str


class ConflictReview(TypedDict):
    conflict_id: str
    topic: str
    involved_agents: list[str]
    positions: list[str]
    resolution: str
    rationale: str


class ReviewRecord(TypedDict):
    review_id: str
    task: TranslationReviewTask
    mode: ReviewMode
    status: str
    reviews: list[ReviewResult]
    conflict_reviews: list[ConflictReview]
    chief_editor_decision: ChiefEditorDecision
