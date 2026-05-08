from dataclasses import dataclass

from council_of_translation.localization.schemas import ReviewMode


@dataclass(frozen=True)
class ReviewerRole:
    agent_name: str
    role: str
    role_mission: str
    review_focus: str
    priority: int
    modes: tuple[ReviewMode, ...]


REVIEWER_ROLES: tuple[ReviewerRole, ...] = (
    ReviewerRole(
        agent_name="technical_safety_reviewer",
        role="技术与占位符审校员",
        role_mission="你只负责检查候选译文是否安全保留占位符、变量、命令、标签、格式和不可翻译项，并考虑长度或格式约束。",
        review_focus="占位符安全、结构保留、格式完整性、技术约束兼容性。",
        priority=10,
        modes=("lightweight", "standard", "strict"),
    ),
    ReviewerRole(
        agent_name="fidelity_reviewer",
        role="忠实度审校员",
        role_mission="你只负责检查候选译文是否准确表达原文含义，是否存在漏译、误译、过度发挥、逻辑关系错误、否定或条件处理错误。",
        review_focus="语义准确性、信息完整性、逻辑关系、义务等级、限制条件。",
        priority=20,
        modes=("lightweight", "standard", "strict"),
    ),
    ReviewerRole(
        agent_name="terminology_reviewer",
        role="术语与一致性管理员",
        role_mission="你只负责检查候选译文与术语表、历史译法和同类文案是否一致，避免同一概念多种译法或专有名词错误翻译。",
        review_focus="术语一致性、命名稳定性、风格规则一致性。",
        priority=30,
        modes=("lightweight", "standard", "strict"),
    ),
    ReviewerRole(
        agent_name="product_context_reviewer",
        role="产品语境审校员",
        role_mission="你只负责检查候选译文是否适合真实产品场景，包括组件类型、交互阶段、界面长度和上下文语义。",
        review_focus="场景适配、组件匹配、交互语义、长度与界面可用性。",
        priority=40,
        modes=("standard", "strict"),
    ),
    ReviewerRole(
        agent_name="ux_copy_reviewer",
        role="用户体验文案审校员",
        role_mission="你只负责检查候选译文是否便于用户理解和行动，是否清楚表达发生了什么、为什么以及用户下一步该做什么。",
        review_focus="易懂性、可操作性、认知负担、错误提示可执行性。",
        priority=50,
        modes=("standard", "strict"),
    ),
    ReviewerRole(
        agent_name="brand_voice_reviewer",
        role="品牌语气守门员",
        role_mission="你只负责检查候选译文是否符合品牌语气和沟通风格，不负责判断技术正确性或术语规范性，除非它们直接影响语气一致性。",
        review_focus="品牌语气、正式程度、情感温度、统一表达风格。",
        priority=60,
        modes=("strict",),
    ),
    ReviewerRole(
        agent_name="risk_ambiguity_reviewer",
        role="风险与歧义审校员",
        role_mission="你只负责检查候选译文是否存在歧义、误导、过度承诺、文化敏感或潜在风险表达。",
        review_focus="歧义、误解风险、合规敏感性、文化风险、措辞稳妥性。",
        priority=70,
        modes=("strict",),
    ),
    ReviewerRole(
        agent_name="fluency_reviewer",
        role="自然度润色员",
        role_mission="你只负责检查候选译文是否符合目标语言习惯，是否流畅自然、简洁清楚，避免翻译腔和生硬表达。",
        review_focus="自然度、可读性、语序、搭配、简洁度。",
        priority=80,
        modes=("lightweight", "standard", "strict"),
    ),
)


ROLE_PRIORITY_RULES = """裁决优先级：
1. 显式项目规则、TB、SG、known_exceptions
2. 技术约束
3. 语义忠实
4. 风险控制
5. 产品语境
6. 术语一致
7. 用户理解效率
8. 品牌语气
9. 自然度润色
10. reviewer 风格偏好

若项目规则与通用本地化经验冲突，优先遵循项目规则；若传入规则互相冲突，应标记人工复核。"""


def normalize_mode(mode: str | None) -> ReviewMode:
    if mode in {"lightweight", "standard", "strict"}:
        return mode  # type: ignore[return-value]
    return "standard"


def get_reviewers_for_mode(mode: ReviewMode) -> list[ReviewerRole]:
    return sorted(
        [role for role in REVIEWER_ROLES if mode in role.modes],
        key=lambda role: role.priority,
    )

