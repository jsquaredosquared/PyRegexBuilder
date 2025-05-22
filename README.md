# PyRegexBuilder

> Build regular expressions swiftly in Python.

PyRegexBuilder allows you to build regular expressions using a DSL similar to that of [Swift RegexBuilder](https://developer.apple.com/documentation/regexbuilder).

PyRegexBuilder uses the stdlib-compatible [regex](https://github.com/mrabarnett/mrab-regex) module.

## Usage

## Installation

```shell
```

## Roadmap

PyRegex builder aims to support as many `regex` module features as possible.

### High priority

- [x] Scoped and global flags
- [x] Negation/inversion
- [x] Character classes and set operations
- [x] Unicode codepoint properties
- [x] Named characters ("\N{}")
- [x] Posix character classes
- [ ] Search anchor
- [x] Support regex literals ("/.../")?
- [x] Switch from using abc to typing.Protocol?

### Low priority

- [ ] Branch reset
- [ ] Fuzzy matching
- [ ] Named list
- [ ] Define, prune, skip, fail

## Contributing

## License

## See also

- [TS Regex Builder](https://github.com/callstack/ts-regex-builder) (also based on Swift RegexBuilder)
- [Edify](https://github.com/luciferreeves/edify) (based on [Super Expressive](https://github.com/francisrstokes/super-expressive))
- [Humre](https://github.com/asweigart/humre)
