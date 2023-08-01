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
