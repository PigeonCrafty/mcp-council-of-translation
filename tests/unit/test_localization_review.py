from council_of_translation.localization.prompt_builders import (
    build_chief_editor_prompt,
    build_reviewer_prompt,
)
from council_of_translation.localization.roles import (
    ROLE_PRIORITY_RULES,
    get_reviewers_for_mode,
    normalize_mode,
)
from council_of_translation.localization.workflow import (
    build_fallback_chief_editor_decision,
    build_unstructured_review_result,
    normalize_chief_editor_decision,
    normalize_review_result,
    parse_json_object,
)


def test_mode_selection():
    assert normalize_mode("unknown") == "standard"

    lightweight = [role.agent_name for role in get_reviewers_for_mode("lightweight")]
    assert lightweight == [
        "technical_safety_reviewer",
        "fidelity_reviewer",
        "terminology_reviewer",
        "fluency_reviewer",
    ]

    strict = [role.agent_name for role in get_reviewers_for_mode("strict")]
    assert "brand_voice_reviewer" in strict
    assert "risk_ambiguity_reviewer" in strict


def test_reviewer_prompt_contains_rule_packet_and_priority():
    role = get_reviewers_for_mode("lightweight")[0]
    task = {
        "source_text": "Delete {count} selected files?",
        "candidate_translation": "删除选中的文件吗？",
        "target_language": "zh-CN",
        "term_glossary": "selected = 已选",
        "style_guide": "保留占位符。",
        "technical_constraints": "placeholders={count}",
    }

    prompt = build_reviewer_prompt(role, task)

    assert "=== REVIEW TASK START ===" in prompt
    assert "selected = 已选" in prompt
    assert "placeholders={count}" in prompt
    assert ROLE_PRIORITY_RULES in prompt
    assert "只输出 JSON" in prompt


def test_chief_editor_prompt_is_recommendation_only():
    task = {
        "source_text": "Save",
        "candidate_translation": "保存",
        "target_language": "zh-CN",
    }
    prompt = build_chief_editor_prompt(task, [])

    assert "你不直接修改文件" in prompt
    assert "recommended_translation" in prompt
    assert "只输出 JSON" in prompt


def test_parse_json_object_from_fenced_output():
    parsed = parse_json_object(
        """```json
        {"verdict": "通过", "issues": [], "suggestions": []}
        ```"""
    )
    assert parsed["verdict"] == "通过"


def test_normalize_review_result_defaults_invalid_values():
    result = normalize_review_result(
        {
            "verdict": "maybe",
            "issues": "缺少占位符",
            "confidence": "certain",
        },
        "technical_safety_reviewer",
        "技术与占位符审校员",
    )

    assert result["verdict"] == "有保留通过"
    assert result["confidence"] == "低"
    assert result["issues"] == ["缺少占位符"]


def test_normalize_chief_editor_decision_defaults_to_candidate():
    task = {"candidate_translation": "保存"}
    decision = normalize_chief_editor_decision({"publishability": "bad"}, task)

    assert decision["publishability"] == "需人工复核"
    assert decision["recommended_translation"] == "保存"
    assert decision["review_needed"] == "是"


def test_unstructured_reviewer_output_is_preserved():
    result = build_unstructured_review_result(
        "The translation is accurate, but 'what I need' sounds too literal.",
        "fluency_reviewer",
        "自然度润色员",
    )

    assert result["verdict"] == "有保留通过"
    assert "what I need" in result["rationale"]
    assert "what I need" in result["suggestions"][0]


def test_fallback_chief_editor_uses_reviewer_text():
    task = {"candidate_translation": "The original translation"}
    reviews = [
        {
            "agent_name": "fluency_reviewer",
            "role": "自然度润色员",
            "verdict": "有保留通过",
            "issues": ["'what I need' is slightly awkward in aphoristic advice."],
            "suggestions": ["Prefer 'what you need' or 'your own needs'."],
            "recommended_translation": "",
            "confidence": "低",
            "rationale": "Natural-language fallback.",
        }
    ]

    decision = build_fallback_chief_editor_decision(task, reviews, "bad json")

    assert decision["publishability"] == "修改后可发布"
    assert decision["recommended_translation"] == "The original translation"
    assert "what I need" in decision["optional_improvements"][0]
    assert decision["review_needed"] == "是"
