# Klotski Solver
The problem is known as Klotski, a puzzle that have been originated in the early 20th century. https://en.wikipedia.org/wiki/Klotski

Among several information available on the internet, there are some Computer Science research involving the algorithm used to solve the problem. http://www.pvv.ntnu.no/~spaans/spec-cs.pdf

This solution uses BFS to look at the first available solution with less steps.

## Requirements
You should have Docker and docker-compose installed on your system, with these installed you should be able to build the image and run it.

Check https://docs.docker.com/compose/install/#install-compose to see how to install docker-compose on your OS

## Build Docker image
```
$make build
```

## Run program
The default way to run the command is with:
```
$make run-script
```
which uses sample-board.txt with the proposed board
```
$make run-script FILE=file-name.txt
```
Changing the default file to run

If you prefer, you can use python virtualenv with this package, just run (you have to have python3 installed to use venv):
```
$make venv
$source venv/bin/activate
$pip install -r requirements.txt
```

Now to run just run the script:
```
python klotski-solver.py file-name.txt
```
Check sample-board.txt to verify file format.
## Run tests
```
$make test
```
Or on virtualenv:
```
py.test tests/
```


## Run sample flask server
```
$make run
```

Open browser on address http:0.0.0.0:5000 and there you can submit a string with the inital board to be parsed, for instance add: abbcabbcdeefdghfi00j



## how to use in other projects
Just import the package:
```
from klotskigame import KlotskiBoard

board = ['a', 'b', 'b', 'c',
         'a', 'b', 'b', 'c',
         'd', 'e', 'e', 'f',
         'd', 'g', 'h', 'f',
         'i', ' ', ' ', 'j']
klotskiBoard = KlotskiBoard()
klotskiBoard.parse_board(board)
klotskiBoard.find_solution()
solution = klotskiBoard.get_solution()
```

the solution will be a list of boards with all the steps.
```
solution = klotskiBoard.get_solution()
```
gives the steps like these:
```
dgbb
dabb
jaee
f0hc
f0ic
```
and
```
solution = klotskiBoard.get_solution(stringfy=True)
```
gives the solution like these:
```
aheeabbcdbbcd00figjf
```
which is a compact version of steps allowing us to use it to return on an API.

## proposed architecture for web api
The idea is to serve this solver into an api, the user will be able to create a version of the board placing pieces and it will be submitted to the api to show the path. An example of fronted will use something like this: https://codepen.io/ggorlen/pen/MOgKxx
https://shopify.github.io/draggable/examples/unique-dropzone.html
https://github.com/WolfgangKurz/grabbable

Since the board has a fixed number of pieces and we know that the size of the boards is the same, we can create a precomputed graph of all possible boards with the transition between them with a variation of this library. With this graph we can load into a application and instead of doing the computation of steps every time a new board is submitted, the algorithm can find the smallest path from the initial board to the solution very fast.
