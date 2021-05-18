# Technical Specification for CrowdNotifier

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]
[![Documentation Status][rtd-badge]][rtd-link]

This repository holds the source files for the technical specification of CrowdNotifier. This specification is technical. We refer to the [CrowdNotifier Documents repository](https://github.com/CrowdNotifier/Documents/) for a more gentle introduction.

A live version of this documentation is available at: [https://crowdnotifierspec.readthedocs.io](https://crowdnotifierspec.readthedocs.io).

We welcome feedback on the specification contained in this repository. We of course 
also welcome feedback on the high-level CrowdNotifier designs and a discussion of their security and privacy properties. However,
please use the [CrowdNotifier Documents](https://github.com/CrowdNotifier/Documents/) repository for these discussions.

## How to build

```
make html
```

or while writing

```
make autobuild-html
```

to auto-build the html files and refresh them in the browser.

To rebuild the images, run

```
cd source/figures
make
```

## Contributing

We welcome feedback on the technical specification in this document. If you have a trivial fix or improvement, go ahead and create a pull request. For large fixes, please create an issue first so we can discuss the changes. Please use the [CrowdNotifier Documents](https://github.com/CrowdNotifier/Documents/) repository for high-level discussions about CrowdNotifier.

Any contributions to this specification must be licensed under the CC BY-SA 4.0 license.

Everyone interacting on the CrowdNotifier projects codebases, issue trackers, etc. is expected to follow the [code of conduct](CODE_OF_CONDUCT.txt).


## License

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

[rtd-link]: https://crowdnotifier.readthedocs.io/en/latest/?badge=latest
[rtd-badge]: https://readthedocs.org/projects/crowdnotifier/badge/?version=latest
