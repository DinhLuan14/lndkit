# LNDKIT

Inspired by [speedy](https://github.com/anhvth/speedy), this repo improves coding speed with smart caching. It saves results in disks to cut down on repeat work.

## Features

- **Fast Caching**: Saves function results to speed up.
- **Coding Tools**: Tools for quicker coding.

## Quick Start

```bash
pip install git+https://github.com/DinhLuan14/lndkit
```

```python
from lndkit import cachef

@cachef(keys=['arg1', 'arg2'])
def some_function(arg1, arg2):
    # Function logic here
    return result
```

Apply `cachef` to cache results of `some_function` based on `arg1` and `arg2`.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for suggestions.
