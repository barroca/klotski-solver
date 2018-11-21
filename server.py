# -*- encoding: utf-8 -*-
from flask import Flask
from flask import request, render_template
from klotskigame import KlotskiBoard


app = Flask(__name__)


@app.route('/')
def home(board=None, error_message=None):
    return render_template('index.html', board=board,
                           error_message=error_message)


@app.route('/get_solution', methods=['GET', 'POST'])
def get_solution():
    try:
        if request.method == 'POST':
            line = request.form['board']
            line = line.strip()
            board = []
            for x in line:
                board.append(x)
            if len(board) != 20:
                raise Exception("Wrong input size")
            klotskiBoard = KlotskiBoard()
            klotskiBoard.parse_board(board)
            klotskiBoard.find_solution()
            solution = klotskiBoard.get_solution()
            result = ''
            result += "Steps are:<br>"
            for p in solution:
                result += p.stringfy()
                result += '<br>'
            result += 'SOLVED<br>'
            result += "Number of steps {}".format(len(solution))
            return result
        else:
            return home()
    except Exception as e:
        error_message = "Problem with board input and processing: {}".format(e)
        return home(line, error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
