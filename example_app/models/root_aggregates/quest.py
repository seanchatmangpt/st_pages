import uuid
from typing import List
from pydantic import BaseModel, Field

from dspygen.lm.groq_lm import Groq
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.yaml_tools import uuid_factory, YAMLMixin
from soc.models.domain_models.exam_point import ExamPoint
from soc.models.domain_models.question import Question
from soc.models.value_objects.creator import Creator
from soc.models.value_objects.edge import Edge


class Quest(BaseModel, YAMLMixin):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the quest.")
    title: str = Field("", description="The title of the quest.")
    description: str = Field("", description="A brief description of the quest.")
    creator: Creator = Field(default_factory=Creator, description="The creator of the quest.")
    questions: List[Question] = Field([], description="A list of questions in the quest.")
    exam_points: List[ExamPoint] = Field([], description="A list of exam points.")
    edges: List[Edge] = Field([], description="A list of edges connecting exam points.")
    data_path: str = Field("", description="The path to the data file associated with the quest.")


    def add_question(self, question: Question) -> None:
        """
        Adds a new question to the quest, ensuring no duplicates.
        """
        if question.id in [q.id for q in self.questions]:
            raise ValueError("Question with this ID already exists in the quest.")
        self.questions.append(question)

    def remove_question(self, question_id: str) -> None:
        """
        Removes a question from the quest by ID.
        """
        self.questions = [q for q in self.questions if q.id != question_id]

    def validate_quest(self) -> bool:
        """
        Validates the quest's completeness and consistency.
        """
        if not self.questions:
            raise ValueError("A quest must have at least one question.")
        # Additional validation logic can be implemented as needed
        return True

    def assign_creator(self, creator: Creator) -> None:
        """
        Assigns a creator or administrator to the quest.
        """
        self.creator = creator


def main():
    from soc.repositories.repository import quest_repository
    # quest_repository.save(apple_cultivation_quest)
    print(quest_repository.get(id="1"))


def main2():
    # Initialize dspygen with Groq
    init_dspy(Groq, model="mixtral-8x7b-32768")

    # Define a creator for the quest
    creator = Creator(name="Dr. Appleseed", email="dr.appleseed@example.com")

    # Define exam points
    ep1 = ExamPoint(
        ep_number=1,
        evidence=[
            "Research data showing a 40% decrease in apple yield in Mississippi due to the pest.",
            "Farmer testimonials on pest sightings and crop damage."
        ],
        reasoning="The emergence of a new pest has significantly impacted apple cultivation in Mississippi, indicating a severe threat to crop yield.",
        assumptions=[
            "The pest's impact is primarily due to its rapid reproduction and lack of effective pesticides.",
            "Similar climate conditions across apple-growing regions might lead to widespread pest spread."
        ]
    )

    ep2 = ExamPoint(
        ep_number=2,
        evidence=[
            "Predictive models suggesting a 40% decrease in nationwide apple production in the next year.",
            "Studies on pest mobility and survival indicating potential for rapid spread."
        ],
        reasoning="Given the pest's characteristics and lack of current control measures, it's projected to spread across the United States, significantly affecting apple production.",
        assumptions=[
            "The pest will encounter similar environmental conditions in other states as in Mississippi.",
            "No effective pest control measures will be developed within the year."
        ]
    )

    ep3 = ExamPoint(
        ep_number=3,
        evidence=[
            "Early-stage research on genetically modified apple varieties showing resistance to the pest.",
            "Funding announcements for research into pest-resistant crops."
        ],
        reasoning="Scientific efforts are underway to develop apple varieties resistant to the pest, which could mitigate future crop losses.",
        assumptions=[
            "Genetic modification can effectively confer resistance to the pest.",
            "Resistant apple varieties can be developed and deployed rapidly enough to impact pest spread."
        ]
    )

    # Define edges to illustrate relationships
    edge1 = Edge(from_ep="ep1", to_ep="ep2", bridging_concept="Pests affecting apple trees")
    edge2 = Edge(from_ep="ep2", to_ep="ep3", bridging_concept="Strategies to mitigate pest impact")

    # Define questions for the quest
    question1 = Question(
        text="What state experienced a significant decrease in apple cultivation due to a new parasite in 2023?",
        options=["Mississippi", "Louisiana", "Arkansas", "Alabama"],
        correct_option=0  # Assuming the first option is correct
    )

    question2 = Question(
        text="What is the expected impact on apple cultivation across the United States by 2024?",
        options=["No change", "20% decrease", "40% decrease", "60% increase"],
        correct_option=2
    )

    question3 = Question(
        text="Which variety of apples was most affected by the parasite?",
        options=["Granny Smith", "Red Delicious", "Honeycrisp", "Fuji"],
        correct_option=0  # Assuming Granny Smith is correct based on the context provided
    )

    # Create a quest
    apple_cultivation_quest = Quest(
        id="1",
        title="Understanding Apple Cultivation and Parasite Impact",
        creator=creator
    )

    # Add exam points and edges to the quest
    for ep in [ep1, ep2, ep3]:
        apple_cultivation_quest.exam_points.append(ep)

    for edge in [edge1, edge2]:
        apple_cultivation_quest.edges.append(edge)

    # Add questions to the quest
    for question in [question1, question2, question3]:
        apple_cultivation_quest.add_question(question)

    # Validate the quest
    if apple_cultivation_quest.validate_quest():
        print(f"Quest '{apple_cultivation_quest.title}' is valid and ready to be published.")
    else:
        print(f"Quest '{apple_cultivation_quest.title}' is not valid.")


    from dspygen.rm.data_retriever import DataRetriever
    data_retriever = DataRetriever(file_path="/Users/candacechatman/dev/soc/data/data.csv", return_columns=["year","state","crop"])

    apple_cultivation_quest.to_yaml("apple_cultivation_quest.yaml")

    from soc.repositories.repository import quest_repository
    # quest_repository.save(apple_cultivation_quest)
    print(quest_repository.get(id="1"))


def create_apple_cultivation_quest():
    # Initialize dspygen with Groq
    init_dspy(Groq, model="mixtral-8x7b-32768")

    # Detailed description and educational objectives of the quest
    quest_description = """
    This quest explores the ecological and economic impacts of a new pest species on apple cultivation in Mississippi.
    Students will investigate the pest's effects, current research on mitigation strategies, and the broader implications
    for apple cultivation across the United States.
    """

    # Define a creator for the quest
    creator = Creator(name="Dr. Appleseed", email="dr.appleseed@example.com")

    # Define exam points with detailed evidence and assumptions
    ep1 = ExamPoint(
        ep_number=1,
        evidence=[
            "40% decrease in apple yield in Mississippi directly attributed to the new pest.",
            "Lack of effective pesticides against the new pest species."
        ],
        reasoning="The new pest's rapid reproduction and resistance to existing pesticides have decimated apple yields.",
        assumptions=[
            "Current pest control methods are ineffective against the new species.",
            "Similar climate conditions in other apple-growing regions could facilitate the pest's spread."
        ]
    )

    ep2 = ExamPoint(
        ep_number=2,
        evidence=[
            "Predicted nationwide decrease in apple production by 40% if the pest spreads.",
            "Genetic modification research as a potential solution to pest resistance."
        ],
        reasoning="The spread of the pest could nationally mirror the devastation seen in Mississippi without intervention.",
        assumptions=[
            "The pest's spread is unimpeded by natural barriers.",
            "Genetically modified apples could offer a timely solution to the pest problem."
        ]
    )

    # Define questions that encourage critical thinking and application of knowledge
    question1 = Question(
        text="How does the rapid reproduction rate of the new pest contribute to its threat level?",
        options=["Increases its ability to resist pesticides", "Decreases its visibility to farmers", "Limits its geographical spread", "Enhances its susceptibility to natural predators"],
        correct_option=0
    )

    question2 = Question(
        text="What are the potential risks and benefits of using genetically modified apples to combat the pest?",
        options=["Risk of cross-species gene transfer vs. potential for increased yield", "Higher cultivation costs vs. pest resistance", "Public resistance to GMO foods vs. saving the apple industry", "All of the above"],
        correct_option=3
    )

    # Define three interconnected exam points for the quest
    ep1 = ExamPoint(
        ep_number=1,
        evidence=[
            "Research data showing a 40% decrease in apple yield in Mississippi due to the pest.",
            "Farmer testimonials on pest sightings and crop damage."
        ],
        reasoning="The emergence of a new pest has significantly impacted apple cultivation in Mississippi, indicating a severe threat to crop yield.",
        assumptions=[
            "The pest's impact is primarily due to its rapid reproduction and lack of effective pesticides.",
            "Similar climate conditions across apple-growing regions might lead to widespread pest spread."
        ]
    )

    ep2 = ExamPoint(
        ep_number=2,
        evidence=[
            "Predictive models suggesting a 40% decrease in nationwide apple production in the next year.",
            "Studies on pest mobility and survival indicating potential for rapid spread."
        ],
        reasoning="Given the pest's characteristics and lack of current control measures, it's projected to spread across the United States, significantly affecting apple production.",
        assumptions=[
            "The pest will encounter similar environmental conditions in other states as in Mississippi.",
            "No effective pest control measures will be developed within the year."
        ]
    )

    ep3 = ExamPoint(
        ep_number=3,
        evidence=[
            "Early-stage research on genetically modified apple varieties showing resistance to the pest.",
            "Funding announcements for research into pest-resistant crops."
        ],
        reasoning="Scientific efforts are underway to develop apple varieties resistant to the pest, which could mitigate future crop losses.",
        assumptions=[
            "Genetic modification can effectively confer resistance to the pest.",
            "Resistant apple varieties can be developed and deployed rapidly enough to impact pest spread."
        ]
    )

    # Define edges to illustrate relationships between exam points
    edge1 = Edge(from_ep="ep1", to_ep="ep2",
                 bridging_concept="Pest's potential for widespread impact on apple cultivation in the US")
    edge2 = Edge(from_ep="ep2", to_ep="ep3",
                 bridging_concept="Research and development of pest-resistant apple varieties as a mitigation strategy")



    # Create the quest with detailed objectives and educational content
    apple_cultivation_quest = Quest(
        id=str(uuid.uuid4()),
        title="Impact of New Pest Species on Apple Cultivation",
        creator=creator,
        description=quest_description,
        exam_points=[ep1, ep2],
        edges=[edge1, edge2],
        questions=[question1, question2],
        data_path="/Users/candacechatman/dev/soc/data/data.csv"
    )

    # The following attributes are mocked for the purpose of this example
    # Add exam points and edges as per the actual implementation details
    # for edge in [edge1, edge2]:
    #     apple_cultivation_quest.edges.append(edge)

    return apple_cultivation_quest



if __name__ == '__main__':
    main()
