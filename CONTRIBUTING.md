# Contributing

Contributions are welcome, and they are greatly appreciated\! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/aluttik/kitsune/issues>.

If you are reporting a bug, please include:

  - Your operating system name and version.
  - Any details about your local setup that might be helpful in
    troubleshooting.
  - Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is
open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
"feature" is open to whoever wants to implement it.

### Write Documentation

kitsune could always use more documentation, whether as part of the
official kitsune docs, in docstrings, or even on the web in blog
posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/aluttik/kitsune/issues>.

If you are proposing a feature:

  - Explain in detail how it would work.
  - Keep the scope as narrow as possible, to make it easier to
    implement.
  - Remember that this is a volunteer-driven project, and that
    contributions are welcome :)


## Get Started

Ready to contribute? Here's how to set up kitsune for local
development.

1.  [Fork](https://github.com/aluttik/kitsune/fork) the kitsune
    repo on GitHub.

2.  Clone your fork locally:

        git clone git@github.com:your_name_here/kitsune.git

3.  Create a branch for local development:

        git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

4.  When you're done making changes, check that your changes pass style
    and unit tests, including testing other Python versions with tox:

        tox

    To get tox, just pip install it.

5.  Before commiting your changes make sure that they comply with the code
    style guidelines by running black:

        black

    To get black, just pip install it.

6.  Commit your changes and push your branch to GitHub:

        git add .
        git commit -m "Your detailed description of your changes."
        git push origin name-of-your-bugfix-or-feature

7.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  Run `black` to make sure all the code is formatted correctly.
3.  The pull request should work for CPython 2.6, 2.7, 3.3, 3.4, 3.5,
    3.6, and 3.7 and for PyPy. Check
    <https://travis-ci.org/aluttik/kitsune> under pull requests for
    active pull requests or run the `tox` command and make sure that the
    tests pass for all supported Python versions.

## Tips

To run a subset of tests:

    tox -e <env> -- tests/<file>[::test]

To run all the test environments in *parallel* (you need to `pip install
detox`):

    detox
