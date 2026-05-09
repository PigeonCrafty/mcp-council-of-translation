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
    detect_conflicts,
    effective_output_mode,
    enforce_output_mode_on_review,
    extract_first_json_object,
    extract_text_from_sampling_repr,
    normalize_chief_editor_decision,
    normalize_conflict_review,
    normalize_conflict_review_mode,
    normalize_output_mode,
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
        "output_mode": "review_only",
        "max_examples": 3,
        "term_glossary": "selected = 已选",
        "style_guide": "保留占位符。",
        "technical_constraints": "placeholders={count}",
    }

    prompt = build_reviewer_prompt(role, task)

    assert "=== REVIEW TASK START ===" in prompt
    assert "selected = 已选" in prompt
    assert "placeholders={count}" in prompt
    assert ROLE_PRIORITY_RULES in prompt
    assert "role_feedback" in prompt
    assert "findings" in prompt
    assert "不要输出 recommended_translation 字段" in prompt
    assert "只输出 JSON" in prompt


def test_chief_editor_prompt_is_recommendation_only():
    task = {
        "source_text": "Save",
        "candidate_translation": "保存",
        "target_language": "zh-CN",
        "output_mode": "review_only",
    }
    prompt = build_chief_editor_prompt(task, [])

    assert "你不直接修改文件" in prompt
    assert "must_fix" in prompt
    assert "should_fix" in prompt
    assert "full_rewrite 才允许 suggested_translation" in prompt
    assert "只输出 JSON" in prompt


def test_parse_json_object_from_fenced_output():
    parsed = parse_json_object(
        """```json
        {"verdict": "通过", "issues": [], "suggestions": []}
        ```"""
    )
    assert parsed["verdict"] == "通过"


def test_extract_text_from_goose_sampling_result_repr():
    response = (
        "SamplingResult(text='{\"agent_name\":\"fidelity_reviewer\","
        "\"verdict\":\"有保留通过\",\"issues\":[\"ok\"]}', result='{...}')"
    )

    extracted = extract_text_from_sampling_repr(response)
    parsed = parse_json_object(extracted)

    assert parsed["agent_name"] == "fidelity_reviewer"
    assert parsed["issues"] == ["ok"]


def test_parse_first_json_object_ignores_sampling_result_tail():
    text = "SamplingResult(text='prefix {\"a\": {\"b\": 1}}', result='{...}')"
    fragment = extract_first_json_object(text)

    assert fragment == '{"a": {"b": 1}}'


def test_normalize_review_result_defaults_invalid_values():
    result = normalize_review_result(
        {
            "verdict": "maybe",
            "issues": "缺少占位符",
            "confidence": "certain",
            "findings": [
                {
                    "span": "{count}",
                    "issue_type": "technical",
                    "severity": "critical",
                    "problem": "占位符缺失",
                    "evidence": "项目要求保留占位符。",
                    "action": "补回 {count}。",
                }
            ],
        },
        "technical_safety_reviewer",
        "技术与占位符审校员",
    )

    assert result["verdict"] == "有保留通过"
    assert result["confidence"] == "低"
    assert result["issues"] == ["缺少占位符"]
    assert result["findings"][0]["issue_type"] == "technical"
    assert result["findings"][0]["severity"] == "critical"


def test_normalize_chief_editor_decision_defaults_to_candidate():
    task = {"candidate_translation": "保存"}
    decision = normalize_chief_editor_decision({"publishability": "bad"}, task)

    assert decision["publishability"] == "需人工复核"
    assert "suggested_translation" not in decision
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
    assert result["findings"][0]["issue_type"] == "other"


def test_fallback_chief_editor_uses_reviewer_text():
    task = {"candidate_translation": "The original translation", "output_mode": "full_rewrite"}
    reviews = [
        {
            "agent_name": "fluency_reviewer",
            "role": "自然度润色员",
            "verdict": "有保留通过",
            "role_feedback": "The phrase sounds like a first-person statement.",
            "findings": [
                {
                    "span": "what I need",
                    "issue_type": "fluency",
                    "severity": "minor",
                    "role_perspective": "自然度润色员",
                    "problem": "格言式建议中第一人称略别扭。",
                    "evidence": "目标读者会期待第二人称建议。",
                    "action": "改为 what you need 或 your own needs。",
                }
            ],
            "issues": ["'what I need' is slightly awkward in aphoristic advice."],
            "suggestions": ["Prefer 'what you need' or 'your own needs'."],
            "example_revisions": [],
            "confidence": "低",
            "rationale": "Natural-language fallback.",
        }
    ]

    decision = build_fallback_chief_editor_decision(task, reviews, "bad json")

    assert decision["publishability"] == "修改后可发布"
    assert decision["suggested_translation"] == "The original translation"
    assert "what I need" in decision["optional_improvements"][0]
    assert decision["review_needed"] == "是"


def test_output_mode_defaults_and_long_text_protection():
    assert normalize_output_mode("bad") == "review_only"
    assert normalize_conflict_review_mode("bad") == "auto"
    assert effective_output_mode({"output_mode": "full_rewrite", "source_text": "a" * 3000, "candidate_translation": "b" * 2000}) == "review_only"


def test_review_only_removes_recommended_translation_and_examples():
    review = {
        "agent_name": "fluency_reviewer",
        "role": "自然度润色员",
        "verdict": "有保留通过",
        "role_feedback": "",
        "findings": [],
        "issues": [],
        "suggestions": [],
        "recommended_translation": "full rewrite",
        "example_revisions": [{"span": "a", "current": "a", "suggested": "b", "reason": "r"}],
        "confidence": "高",
        "rationale": "",
    }
    cleaned = enforce_output_mode_on_review(review, {"output_mode": "review_only"})

    assert "recommended_translation" not in cleaned
    assert cleaned["example_revisions"] == []


def test_detects_targeted_conflicts():
    reviews = [
        {
            "agent_name": "fidelity_reviewer",
            "role": "忠实度审校员",
            "verdict": "有保留通过",
            "role_feedback": "",
            "findings": [],
            "issues": ["permissions 不应加入同意。"],
            "suggestions": ["保留授权/许可。"],
            "example_revisions": [],
            "confidence": "高",
            "rationale": "",
        },
        {
            "agent_name": "risk_ambiguity_reviewer",
            "role": "风险与歧义审校员",
            "verdict": "有保留通过",
            "role_feedback": "",
            "findings": [],
            "issues": ["合规语境下授权与同意更稳妥。"],
            "suggestions": [],
            "example_revisions": [],
            "confidence": "高",
            "rationale": "",
        },
    ]

    conflicts = detect_conflicts({"enable_conflict_review": "auto", "max_conflicts": 2}, reviews)

    assert conflicts
    assert conflicts[0]["conflict_id"] == "conflict_1"


def test_detects_finding_based_conflicts():
    reviews = [
        {
            "agent_name": "terminology_reviewer",
            "role": "术语一致性审校员",
            "verdict": "有保留通过",
            "role_feedback": "术语应稳定。",
            "findings": [
                {
                    "span": "speaker preservation",
                    "issue_type": "terminology",
                    "severity": "major",
                    "role_perspective": "术语一致性审校员",
                    "problem": "需要固定术语。",
                    "evidence": "TB 要求。",
                    "action": "使用“说话人特征保留”。",
                }
            ],
            "issues": [],
            "suggestions": [],
            "example_revisions": [],
            "confidence": "高",
            "rationale": "",
        },
        {
            "agent_name": "fluency_reviewer",
            "role": "自然度润色员",
            "verdict": "有保留通过",
            "role_feedback": "读者更容易理解声音风格。",
            "findings": [
                {
                    "span": "speaker preservation",
                    "issue_type": "fluency",
                    "severity": "preference",
                    "role_perspective": "自然度润色员",
                    "problem": "固定术语略生硬。",
                    "evidence": "面向普通读者。",
                    "action": "改为“声音风格保留”。",
                }
            ],
            "issues": [],
            "suggestions": [],
            "example_revisions": [],
            "confidence": "中",
            "rationale": "",
        },
    ]

    conflicts = detect_conflicts({"enable_conflict_review": "auto", "max_conflicts": 2}, reviews)

    assert conflicts[0]["topic"].startswith("同一片段")


def test_normalize_conflict_review_defaults_to_detected_conflict():
    conflict = {
        "conflict_id": "conflict_1",
        "topic": "topic",
        "involved_agents": ["a"],
        "positions": ["p"],
        "resolution": "",
        "rationale": "",
    }
    normalized = normalize_conflict_review({"resolution": "use A"}, conflict)

    assert normalized["conflict_id"] == "conflict_1"
    assert normalized["resolution"] == "use A"
