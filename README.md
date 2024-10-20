# Habiticalib

<p align="center">
    <em>Modern asynchronous Python client library for the Habitica API</em>
</p>

[![build](https://github.com/tr4nt0r/habiticalib/workflows/Build/badge.svg)](https://github.com/tr4nt0r/habiticalib/actions)
[![codecov](https://codecov.io/gh/tr4nt0r/habiticalib/graph/badge.svg?token=iEsZ1Ktj7d)](https://codecov.io/gh/tr4nt0r/habiticalib)
[![PyPI version](https://badge.fury.io/py/habiticalib.svg)](https://badge.fury.io/py/habiticalib)

---

**Documentation**: <a href="https://tr4nt0r.github.io/habiticalib/" target="_blank">https://tr4nt0r.github.io/habiticalib/</a>

**Source Code**: <a href="https://github.com/tr4nt0r/habiticalib" target="_blank">https://github.com/tr4nt0r/habiticalib</a>

---

## Development

### Setup environment

We use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it's installed on your system.

### Run unit tests

You can run all the tests with:

```bash
hatch run test
```

### Format the code

Execute the following command to apply linting and check typing:

```bash
hatch run lint
```

### Publish a new version

You can bump the version, create a commit and associated tag with one command:

```bash
hatch version patch
```

```bash
hatch version minor
```

```bash
hatch version major
```

Your default Git text editor will open so you can add information about the release.

When you push the tag on GitHub, the workflow will automatically publish it on PyPi and a GitHub release will be created as draft.

## Serve the documentation

You can serve the Mkdocs documentation with:

```bash
hatch run docs-serve
```

It'll automatically watch for changes in your code.

## License

This project is licensed under the terms of the MIT license.
