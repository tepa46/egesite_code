from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

import json

import ChoiceProblem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/blog')
def blog():
    with open('blog.json', 'r', encoding='utf-8-sig') as f:
        blog = json.loads(f.read())
    return render_template('blog.html', blog=blog)


@app.route('/problems/<string:type>', methods=['GET', 'POST'])
def problems(type):
    return render_template('problems.html', title='Задачи', choice_problem=choice_problem, ege_data=ege_data, type=type)


def check(answer, problem_id):
    flag = False
    for line in ege_data[str(problem_id)]['answer']:
        if type(line) == str:
            if answer.lower() == line.lower():
                flag = True
        else:
            if answer == line:
                flag = True
    return flag


@app.route('/problem/<int:problem_id>', methods=['GET', 'POST'])
def problem(problem_id):
    data = {'message': ['Задача по предмету: ' + ege_data[str(problem_id)]['subject_name'],
                        ege_data[str(problem_id)]['problem_text']],
            'photo': [ege_data[str(problem_id)]['problem_image_text']]}

    if request.method == 'GET':
        return render_template('view_task.html', title=f'Задача #{problem_id}', problem_id=problem_id, data=data,
                               wrong=False, success=False)
    elif request.method == "POST":
        if check(request.form['answer'], problem_id):
            return render_template('view_task.html', title=f'Задача #{problem_id}', problem_id=problem_id,
                                   data=data, wrong=False, success=True)
        else:
            return render_template('view_task.html', title=f'Задача #{problem_id}', problem_id=problem_id,
                                   data=data, wrong=True, success=False)


@app.route('/view_answer/<int:problem_id>')
def view_answer(problem_id):
    answer = ege_data[str(problem_id)]['answer']
    solution = ege_data[str(problem_id)]['problem_solution']
    return render_template('view_answer.html', title=f'Задача #{problem_id}', solution=solution, answer=answer,
                           solution_type='list' if type(solution) == list else 'oneof',
                           answer_type='list' if type(answer) == list else 'oneof', problem_id=problem_id,
                           choice_problem=choice_problem)


if __name__ == '__main__':
    with open("load.json", 'r', encoding="utf-8-sig") as f:
        ege_data = json.loads(f.read())
        # logging.info('Have read load.json')
        print('Have read load.json')

    with open('predmet_ids.json', 'r', encoding="utf-8-sig") as f:
        predmet_ids = json.loads(f.read())
        # logging.info('Have read predmet_ids.json')
        print('Have read predmet_ids.json')

    with open('similar_tasks.json', 'r', encoding="utf-8-sig") as f:
        similar_tasks = json.loads(f.read())
        # logging.info('Have read similar_tasks.json')
        print('Have read similar_tasks.json')

    choice_problem = ChoiceProblem.ChoiceProblem(ege_data, similar_tasks)
    app.run(port=8080, host='127.0.0.1')
