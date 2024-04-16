import asyncio
from pydantic import BaseModel, Field
from typing import Optional, List


class SocraticModeration(BaseModel):
    """
    Simplified moderation for educational Socratic dialogues.
    Ensures discussions remain focused and respectful.
    """
    level: int = Field(1, ge=1, le=5,
                       description="Moderation intensity level, with 1 being least and 5 most restrictive.")
    categories: Optional[List[str]] = Field(default=None,
                                            description="Optional categories for focused moderation.")


class SocraticResponse(BaseModel):
    """
    Represents a Socratic response to encourage deeper thinking and reflection.
    """
    question: str = Field(..., title="Question",
                          description="The Socratic question posed to the user to stimulate deeper thinking.")
    context: str = Field(..., title="Context",
                         description="Context or theme of the discussion to guide the dialogue.")
    moderation: SocraticModeration = Field(..., title="Moderation Settings",
                                           description="Settings to ensure dialogue remains productive and respectful.")
    follow_up: Optional[str] = Field(None, title="Follow-Up Question",
                                     description="An optional follow-up question to further deepen the dialogue.")


class DialogueAggregate:
    def __init__(self):
        self.state = "initial"
        self.moderation_settings = SocraticModeration(level=2, categories=["respect", "productivity"])

    async def handle_user_input(self, user_input: str) -> SocraticResponse:
        """
        Processes user input, applies moderation, and generates a Socratic response.
        """
        # Example response generation logic
        question = "What led you to ask about this topic?"
        context = "Understanding the motivation behind questions."
        follow_up = "How does this topic relate to your current learning objectives?"

        return SocraticResponse(
            question=question,
            context=context,
            moderation=self.moderation_settings,
            follow_up=follow_up
        )


async def main():
    """Main function for initiating Socratic dialogue."""
    dialogue = DialogueAggregate()
    user_input = "Can you tell me more about the Socratic method?"
    response = await dialogue.handle_user_input(user_input)
    print(response.json(indent=2))


if __name__ == '__main__':
    asyncio.run(main())
