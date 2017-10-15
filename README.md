# Life game

Life game is a Python 2.7 application which runs on the Unix-like systems at the moment.

## Installation

```
git clone git@github.com:jezradek/life_game.git
cd life_game

virtualenv life_game_venv
source life_game_venv/bin/activate

pip install -r requirements.txt
```

## Run

```
python run.py <path/to/file.xml>

python run.py samples/small.xml
python run.py samples/big.xml
```

## Run tests
```
python tests/run_tests.py
```

## Contributing

Please follow PEP8 style guide with only exception to the line length, which is 100 chars in this case.

