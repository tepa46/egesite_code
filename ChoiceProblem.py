import random


class ChoiceProblem:
    def __init__(self, ege_data, similar_tasks):
        self.ege_data = ege_data
        self.similar_tasks = similar_tasks

    def choice_rand_question(self):
        return random.choice([*self.ege_data.keys()])

    def choice_similar_question(self, key):
        if str(key) in self.similar_tasks and len(self.similar_tasks[str(key)]):
            return random.choice([*self.similar_tasks[str(key)]])
        else:
            return 'Не удалось подобрать задачу'
