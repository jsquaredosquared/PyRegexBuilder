# PyRegexBuilder

> Build regular expressions swiftly in Python.

## Features

- 🧩 **Simple yet powerful DSL**: PyRegexBuilder allows you to build regular expressions using a DSL similar to that of [Swift RegexBuilder](https://developer.apple.com/documentation/regexbuilder). This can make it easier to compose and maintain.
- 🔎 **Extensive regular expression support**: PyRegexBuilder is made possible thanks to the feature-rich [regex](https://github.com/mrabarnett/mrab-regex) module.

!!! danger
    - 🛠️ This is still a work in progress, and the API may change.
    - 🐛 If you find a bug or have a suggestion, please open an issue or pull request.

## Quickstart

1. Install PyRegexBuilder and the Regex library using your favourite package manager.

    === "uv"

        ``` shell
        uv add pyregexbuilder regex
        ```

    === "pip"

        ```shell
        pip install pyregexbuilder regex
        ```

    ???- warning "`regex` or `re`?"
        - PyRegexBuilder uses the `regex` module under the hood, with `regex.DEFAULT_VERSION = re.V1`. This is required if you want to use all the features.
        - You can use `regex` with `regex.DEFAULT_VERSION = re.V0` or the built-in `re` module if you really want to, but some features may not work as expected.

2. Compose regular expressions.

    ```python
    from pyregexbuilder import *
    import regex as re

    text = ... # This is the text that you want to use.

    pattern = Regex(
        # Build your pattern up here.
        # Don't forget to compile it!
    ).compile()


    # Now you can use the pattern in regex operations.
    result = re.search(pattern, text)
    ```

    !!! tip
        - Strings that begin and end with forward slashes (i.e., `r"/.../"`) will be treated as regex literals.
        - All other strings will be escaped with `re.escape()`.

## Documentation

This documentation assumes familiarity with regex features.

- To learn how to use regular expressions in Python, see the [docs](https://docs.python.org/3/library/re.html) and [how-to](https://docs.python.org/3/howto/regex.html).
- To see which additional features are provided by the `regex` module, see the [regex GitHub page](https://github.com/mrabarnett/mrab-regex).
- See the [tutorial](tutorial.md) for an example of how to use PyRegexBuilder.
- Check out the API reference to see all the features available. The API is inspired by Swift RegexBuilder and TS Regex Builder.

## Contributing

See [this page](contributing.md).

## See also

- [TS Regex Builder](https://github.com/callstack/ts-regex-builder) (also based on Swift RegexBuilder)
- [Edify](https://github.com/luciferreeves/edify) (based on [Super Expressive](https://github.com/francisrstokes/super-expressive))
- [Humre](https://github.com/asweigart/humre)
