from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.abstract_message import AbstractMessage


class QuestionAsked(AbstractMessage):
    question_text: str
    topic: str


class ResponseSubmitted(AbstractMessage):
    response_text: str
    question_id: int


class FeedbackProvided(AbstractMessage):
    feedback_text: str
    response_id: int


class ContentUpdated(AbstractMessage):
    content_id: int
    update_notes: str


class StudentActor(AbstractActor):
    async def handle_question(self, question: QuestionAsked):
        # Evaluate question and provide response
        response = "The significance is..."
        await self.publish(ResponseSubmitted(response_text=response, question_id=question.message_id))


class TutorActor(AbstractActor):
    async def handle_response(self, response: ResponseSubmitted):
        # Evaluate response and provide feedback
        feedback = "Great insight, but consider..."
        await self.publish(FeedbackProvided(feedback_text=feedback, response_id=response.question_id))


class ContentManagerActor(AbstractActor):
    async def update_content(self, content_update: ContentUpdated):
        # Update content based on received update
        print(f"Content ID {content_update.content_id} updated with notes: {content_update.update_notes}")


class ModerationActor(AbstractActor):
    """Checks for inappropriate content and moderates as needed."""
    async def handle_message(self, message: AbstractMessage):
        # Placeholder logic for moderation
        if "inappropriate" in message.text:
            print("Inappropriate content detected. Moderating message...")
            await self.publish(ContentUpdated(content_id=message.message_id,
                                              update_notes="Inappropriate content removed."))
# The TutorActor would then receive the ResponseSubmitted message, evaluate the response, and issue a FeedbackProvided message.

async def main():
    from dspygen.rdddy.actor_system import ActorSystem
    actor_system = ActorSystem()
    # Example usage within the system
    student_actor = await actor_system.actor_of(StudentActor)
    tutor_actor = await actor_system.actor_of(TutorActor)
    content_manager_actor = await actor_system.actor_of(ContentManagerActor)

    # Tutor asking a question
    await actor_system.publish(QuestionAsked(question_text="What is the significance of...", topic="Physics"))

    await actor_system.publish(ResponseSubmitted(response_text="The significance is...", question_id=1))

    # Student submitting a response


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
