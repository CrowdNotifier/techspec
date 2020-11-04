This document provides the technical specification for CrowdNotifier. Its goal is to help implementers implement a presence tracing system based on CrowdNotifier or its variants. This document repeats some of the concepts presented in the `CrowdNotifier White Paper <https://github.com/CrowdNotifier/documents/blob/main/CrowdNotifier%20-%20White%20Paper.pdf>`_ :cite:p:`whitepaper` but should be seen as a companion rather than as a replacement.

This document describes in technical detail three variants of CrowdNotifier:

* :ref:`The basic CrowdNotifier scheme <basic-crowdnotifier>` is the same scheme as described in the `CrowdNotifier White Paper <https://github.com/CrowdNotifier/documents/blob/main/CrowdNotifier%20-%20White%20Paper.pdf>`_ :cite:p:`whitepaper`. The version provides strong abuse resistance by requiring cooperation of both the :term:`Location Owner` and :term:`Health Authority` to trigger tracing. Records stored on the phone are private: they can only be decrypted if and only if these parties trigger tracing. 

* :ref:`A managed version of CrowdNotifier <managed-crowdnotifier>` that enables an organization to manage many locations (for example, meeting rooms) at the same time without the overhead of storing different tracing QR codes for each of them. This scheme has the same properties as the basic CrowdNotifier scheme.

* :ref:`A server-based version of CrowdNotifier <server-based-crowdnotifier>` that doesn't require cooperation of the :term:`Location Owner` to trigger notifications, and can instead send notifications based on records uploaded by index cases. As a result, abuse resistance is weaker -- the health authority can trigger locations on its own. However, it is fully compatible with the basic CrowdNotifier scheme so that clients, if they want, can still enjoy full privacy protection of records on the phone.

None of these schemes reveal which :term:`Locations<Location>` are notified to
adversaries that didn't visit these locations (nor colluded with somebody that
did). We refer to the academic paper for a thorough analysis of requirements and security proofs :cite:p:`crowdnotifier-paper`.


Authors and Contributors
------------------------

This technical specification was written by:

* Wouter Lueks, `SPRING Lab <spring.epfl.ch>`_, EPFL
* Linus Gasser, `C4DT <https://c4dt.org>`_, EPFL
* Carmela Troncoso, `SPRING Lab <spring.epfl.ch>`_, EPFL

This document benefited from feedback by:

* Fabian Aggeler, Ubique
* Johannes Gallmann, Ubique
* Matthias Felix, Ubique
* Simon Roesch, Ubique

This document also benefited from earlier feedback on the white paper `CrowdNotifier White Paper <https://github.com/CrowdNotifier/documents/>`__ :cite:p:`whitepaper`.

License
-------

This work is licensed under a `Creative Commons Attribution-ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>`_.
