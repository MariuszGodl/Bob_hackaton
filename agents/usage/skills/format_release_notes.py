from agents.src.models.skill_model import Skill

format_release_notes = Skill(
        name="Format Release Notes",
        short_description="Formats raw commit summaries into standard Markdown release notes.",
        full_content=(
            "When formatting release notes:\n"
            "1. Group changes into ## 🚀 Features, ## 🐛 Bug Fixes, and ## 🧰 Maintenance.\n"
            "2. Ensure each line begins with a concise action verb."
        )
    )