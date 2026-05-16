from agents.src.models.skill_model import Skill


code_review_skill = Skill(
        name="Secure Code Review",
        short_description="Provides strict security validation rules for Python source code.",
        full_content=(
            "When evaluating code for security:\n"
            "1. Check for hardcoded credentials or API keys.\n"
            "2. Flag any use of 'exec()' or 'eval()'."
        )
)