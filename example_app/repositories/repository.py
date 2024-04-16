from pathlib import Path
from soc.models.domain_models.conversation import Conversation
from soc.models.domain_models.user import User
from soc.models.domain_models.exam_point import ExamPoint
from soc.models.domain_models.feedback import Feedback
from soc.models.domain_models.student_progress import StudentProgress
from soc.models.domain_models.question import Question, ConstructedQuestion  # Assuming ConstructedQuestion is part of the same file
from soc.models.root_aggregates.educational_content import EducationalContent
from soc.models.root_aggregates.quest import Quest
from soc.models.root_aggregates.tutoring_session import TutoringSession
# Import the base repository class
from soc.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    pass

class ExamPointRepository(BaseRepository[ExamPoint]):
    pass

class ConversationRepository(BaseRepository[Conversation]):
    pass

class FeedbackRepository(BaseRepository[Feedback]):
    pass

class StudentProgressRepository(BaseRepository[StudentProgress]):
    pass

class QuestionRepository(BaseRepository[Question]):
    pass

class ConstructedQuestionRepository(BaseRepository[ConstructedQuestion]):
    pass

class EducationalContentRepository(BaseRepository[EducationalContent]):
    pass

class QuestRepository(BaseRepository[Quest]):
    pass

class TutoringSessionRepository(BaseRepository[TutoringSession]):
    pass

from pathlib import Path

# Define the base directory for storage files
BASE_DIR = Path(__file__).resolve().parent / "data_storage"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Instantiate repositories with specific storage file paths
user_repository = UserRepository(model=User, storage_file=BASE_DIR / "users.json")
exam_point_repository = ExamPointRepository(model=ExamPoint, storage_file=BASE_DIR / "exam_points.json")
conversation_repository = ConversationRepository(model=Conversation, storage_file=BASE_DIR / "conversations.json")
feedback_repository = FeedbackRepository(model=Feedback, storage_file=BASE_DIR / "feedback.json")
student_progress_repository = StudentProgressRepository(model=StudentProgress, storage_file=BASE_DIR / "student_progress.json")
question_repository = QuestionRepository(model=Question, storage_file=BASE_DIR / "questions.json")
constructed_question_repository = ConstructedQuestionRepository(model=ConstructedQuestion, storage_file=BASE_DIR / "constructed_questions.json")
educational_content_repository = EducationalContentRepository(model=EducationalContent, storage_file=BASE_DIR / "educational_content.json")
quest_repository = QuestRepository(model=Quest, storage_file=BASE_DIR / "quests.json")
tutoring_session_repository = TutoringSessionRepository(model=TutoringSession, storage_file=BASE_DIR / "tutoring_sessions.json")

# Example usage to demonstrate adding a new user
def add_sample_user():
    new_user = User(user_id="1", name="Sample User")
    user_repository.add(new_user)
    print(f"User {new_user.name} added.")

if __name__ == '__main__':
    add_sample_user()
