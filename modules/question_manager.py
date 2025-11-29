from dataclasses import dataclass,field
from modules.all_questions import all_questions
import flet as ft
import time

class QuestionNotFound(Exception):
    pass

@dataclass
class Question:
    question: str = ""
    answers: list[str] = field(default_factory=list)
    answer_count: int = 0
    first_correct: list[str | None] = field(default_factory=list)
@dataclass
class Score:
    name: str
    score: int



questions: list[Question] = []

class QuestionManager:
    def __init__(self, round_time = 90):
        self.current_index = 0
        self.round_time = round_time
        self.previous_time = 0  #selection time of  previous question
        self.question = None
        self.scores: dict[str, Score] = {}
    def get_scores(self):
        sorted_scores = sorted(
            self.scores.items(),
            key=lambda item: item[1].score,
            reverse=True
        )
        return sorted_scores

    def get_time_remaining(self):
        return  self.round_time -   int(time.time() - self.previous_time)

    def submit_answer(self, user_id,user_name, user_answer):
        ua = user_answer.strip().lower()
        valid_answers = [a.lower() for a in self.question.answers]
        try:
            idx = valid_answers.index(ua)
        except ValueError:
            return -1  # wrong answer

        # if someone already took this answer, ignore
        if self.question.first_correct[idx] is not None:
            return -2

        # store the first user who got it
        if idx == 0:
            s = 15
        else:
            s = 10
        self.scores.setdefault(user_id, Score(name=user_name, score=0)).score += s
        self.scores[user_id].name = user_name
        self.question.first_correct[idx] = user_name
        return idx

    def new_question(self):
        self.scores: dict[str, Score] = {}
        n = len(all_questions)
        self.current_index = (self.current_index + 1) % n
        self.question = Question()
        self.question.question = all_questions[self.current_index]["question"]
        self.question.answers = all_questions[self.current_index]["answers"]
        self.question.answer_count = len(self.question.answers)
        self.question.first_correct = [None] * self.question.answer_count
        self.previous_time = time.time()
    def end_current_question(self):
        self.previous_time = 0

    def get_score(self, user_id: str) -> int:
            ps = self.scores.get(user_id)
            return ps.score if ps else 0

    def get_question(self):
        if int(time.time() - self.previous_time) >= self.round_time:
            #time to get new question
            print("Selecting new question")
            self.new_question()

        return self.question