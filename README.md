## Installation

Make sure to have Python > 3.9 installed. Run:

```
pip install -e .
```

## Running

Simply run the `main.py` file with an URL:

```
python main.py https://example.com
```

If you're on a Mac and get an SSL related error, follow the answer in this [post](https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate)

## Tests

Install `pytest`:

```
pip install pytest
```

or

```
conda install pytest
```

To run tests locally you might have to install an auxiliary tool on OSX:

```
brew install python-tk
```

## Submitting a pull request

* Make sure to run the tests locally and the linter. For the linter we're using black:

```
pip install black
```

or

```
conda install black
```

You can run the linter by going to the root directory and typing the command:

```
black .
```

* Update the main branch

```
git checkout main
git pull upstream main
```

* Create a new branch for your contributions

```
git checkout -b branch_name
```

* Submit your changes
