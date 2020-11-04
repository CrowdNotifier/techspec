.. _server-based-crowdnotifier:

**************************
Server-Based CrowdNotifier
**************************

In the basic CrowdNotifier scheme, triggering notification requires cooperation of both the :term:`Health Authority` and the :term:`Location Owner` (or :term:`Organization`, when using :ref:`the managed version of CrowdNotifier<managed-crowdnotifier>`). The need for two parties strengthens the abuse resistance of the solution. It ensures that the :term:`Health Authority` on their own cannot trigger notifications. Additionally, it enables users to receive notifications based on encrypted data stored on the phone, providing strong privacy protection of phone records.

An alternative design choice can be to prioritize speed of notification, by choosing what venues should trigger notifications without relying on decisions by the :term:`Health Authority`. Instead, the decision to trigger can be made automatically, either at the server, e.g. :cite:p:`RocaBC21`, or on the phone, e.g., the initial proposal by the CoronaWarnApp team\ [#cwa]_. In this approach, notifications are sent without explicit approval by health authorities, and without explicit approval by venue owners.

Visitors' phones store clear text records of (possibly ephemeral) identifiers of visited :term:`Locations<Location>` together with the visit times. The :term:`Health Authority` provides index cases with an authorization to upload these identifiers and times to the backend server. Other phones download these identifiers and times and compare them against their own records. If there is an overlap, the phone notifies the user.

In this section we propose a variant of CrowdNotifier, called Server-Based CrowdNotifier. This variant facilitates automatic notifications mechanism based on uploads by index cases, while being interoperable with :ref:`the basic CrowdNotifier protocol<basic-crowdnotifier>` and its clients. The basic and server-bases approaches are interoperable in that clients are always notified regardless of scheme:

* Basic CrowdNotifier clients can operate in regions that deploy Server-Based CrowdNotifier. They scan QR codes, they store encrypted records with strong privacy protections as before, and they can determine exposure and notify their users just like Server-Based CrowdNotifier clients.

* Server-Based CrowdNotifier clients can operate in regions that deploy the basic CrowdNotifier scheme. They scan QR codes, they store records (containing identifiers) as before, and they can determine exposure and notify their users just like basic CrowdNotifier clients in these regions.

Implications of Automatic Triggering
====================================

Automating the triggering decision process brings the following differences with respect to the basic CrowdNotifier.

First, the lack of filtering by a :term:`Health Authority` is likely to result in the system triggering more notifications than if the :term:`Health Authority` was involved. Depending on how many CrowdNotifier locations users visit, there may be an increase in the number of notifications they receive. This can result in notification fatigue, and in users ignoring these notifications.   

Second, because in this approach phones need to store clear text records to enable uploads, anyone with access to the phone can learn the identifiers of the places where the user has been. To ensure privacy of the records stored on the phone, :term:`Locations<Location>` should frequently rotate their identifiers and the corresponding QR codes. If the QR codes remain static, privacy of records is limited. On the contrary, even if the QR codes are static, the basic CrowdNotifier protocol still guarantees privacy of stored records.

Third, if QR codes are not rotated, malicious actors can use identifiers they know (e.g., via crowd-sourcing collection) to trigger notifications for locations they did not visit if they also have an upload authorization.

Fourth, the upload of :term:`Locations<Location>` visited by the same user and/or the publication of :term:`Locations<Location>` visited by a small group of index cases, may enable an adversaries to learn information about user patterns and co-locations. In the basic CrowdNotifier scheme, since the :term:`Health Authority` is the one triggering notifications, neither uploads nor downloads leak any information about users.

We provide an in-depth security and privacy analysis of Server-Based CrowdNotifier at the end of this section.


Overview of Server-Based CrowdNotifier
======================================

The key idea of Server-Based CrowdNotifier is to let the central :term:`Backend Server` replace the roles of the :term:`Health Authority` and :term:`Location Owner` in the basic CrowdNotifier scheme. To this end, the :term:`Backend Server` can generate tracing keys that let basic CrowdNotifier clients decrypt their records after receiving appropriate uploaded information from the index case.

To enable this shift, we build on the :ref:`managed CrowdNotifier scheme<managed-crowdnotifier>`, and let the :term:`Backend Server` generate a single master public-private key pair. The corresponding master public key is included in all QR codes in the region managed by this server. The :term:`Backend Server` locally stores the corresponding master secret key.

Index cases upload the information they collected about the locations they visited to the :term:`Backend Server`. The backend uses this information to compute the relevant tracing identities, and uses the master secret key to compute the corresponding tracing keys. Finally, the backend transmits the tracing keys to all clients. We recall that the tracing identity is just cryptographic material. To run this process, the backend does not need to know the venue's real data. 

We next detail the steps of Server-Based CrowdNotifier.


Setting up the Backend Server
=============================

The :term:`Backend Server` generates a master public key :math:`\masterpkserver` and a corresponding master secret key :math:`\masterskserver` by running :math:`\ibekeygen` of the identity-based encryption algorithm. The server publishes :math:`\masterpkserver` and privately stores :math:`\masterskserver`.


Setting-up a Location
=====================

To set up a :term:`Location` the :term:`Location Owner` runs the setup program. This process proceeds in much the same way :ref:`as in the basic CrowdNotifier scheme<basic-setting-up-location>`, but skips the key-generation steps. The program outputs one public QR code. In Server-Based CrowdNotifier their is no corresponding private QR code. 

For security reasons, the setup program must run client-side. We propose to use client-side JavaScript to statelessly generate the PDFs containing the QR code.

The :term:`Location Owner` provides a description of the location (e.g., name, address, type). Setup then proceeds as follows. 

1. It retrieves the master public key :math:`\masterpkserver` of the server.

2. It picks a random 32-byte seed. 

Setup then generates the public QR code by encoding it into :ref:`standard QR-code format<entry-code-format>`. In particular, it inserts the location information, the seed it just generated, and the server's master public key :math:`\masterpkserver`.


Visiting a Location
===================

When visiting a location basic CrowdNotifier clients :ref:`proceed as in the basic scheme<basic-visiting-location>`. Server-Based CrowdNotifier clients proceed differently to support uploads.

As before, we assume the app gathers the arrival time ``arrival time`` and departure time ``departure time``. See :ref:`the basic scheme for more details<basic-visiting-location>`. The app then proceeds as follows.

1. Using :ref:`the process detailed for the basic CrowdNotifier scheme
   <basic-computing-identities>`
   the app derives from the QR code :math:`\payload`:
   the pre identity :math:`\preid` for the :term:`Location`,
   the notification key :math:`\notificationkey`,
   and for each interval :math:`(\intervalLength, \intervalStart)` that overlaps with the user's visit 
   the time-specific keys :math:`\timekey` and identities :math:`\id`.
   This process requires only basic cryptographic primitives.

2. The app creates a visit record containing
   ``arrival time``,
   ``departure time``,
   the pre identity :math:`\preid`,
   the notification key :math:`\notificationkey`,
   and the time specific tuples:

   .. math::

      (\intervalLength, \intervalStart, \timekey, \id).

3. The app stores the visit record. When extra privacy is required, the app can encrypt the visit record against the public key of the :term:`Health Authority` and additionally store the :ref:`basic CrowdNotifier encrypted record<basic-crowdnotifier>` to match notifications.

The pre identity :math:`\preid` and values :math:`(\timekey, \id)` are needed to enable the :term:`Backend Server` to compute the location tracing keys. The notification key :math:`\notificationkey` is needed decrypt notification messages from the backend, and to enable the Server-Based CrowdNotifier backend to send encrypted tracing data to basic CrowdNotifier clients.

When records are stored in the clear,
apps use the computed identities :math:`\id`
to recognize tracing keys published by basic CrowdNotifier systems.
Otherwise, when storing CrowdNotifier encrypted records, clients proceed as in :ref:`the basic CrowdNotifier scheme<basic-crowdnotifier>`.


Initiating Presence Notification
================================

In Server-Based CrowdNotifier, presence notification is initiated by an index case that has been tested positive for SARS-CoV-2. We assume that the user has an upload authorization and that the :term:`Backend Server` knows the corresponding contagious window.

The app and server proceed as follows:

1. The app sends its upload authorization to the :term:`Backend Server` to obtain the corresponding contagious window.

2. For each record corresponding to this contagious window, the app uploads:
   the (possibly rounded) arrival and departure times,
   the pre identity :math:`\preid`,
   the notification key :math:`\notificationkey`,
   and the tuples

   .. math::

      (\intervalLength, \intervalStart, \timekey).

3. The :term:`Backend Server` validates the uploaded data.
   In particular, it checks that:

    * All reported visits fall within the user's contagious window
      as established by the :term:`Health Authority`.

    * Individual records are not too long
      (e.g., at most the maximum duration allowed by the app)

    * Validates that the reported tuples :math:`(\intervalLength, \intervalStart)`
      are correctly formed
      and
      the corresponding interval overlaps
      the reported visit times for the corresponding record.

    * That the user does not report being in more than one place at the same time.
      To do so, the server checks that the time intervals covered by the records do not overlap.
      Or,
      in case the app reports rounded interval lengths
      do not overlap more than what would be allowed because of time grunularity.

   Optionally, if the :term:`Backend Server` applies a heuristic to determine when to trigger a :term:`Location` it can store and filter the uploaded data before proceeding to the next step.

4. The :term:`Backend Server` then proceeds as follows for each uploaded (or selected) record.

   1. It uses the pre identity :math:`\preid`, and corresponding tuples

      .. math::

         (\intervalLength, \intervalStart, \timekey)

      to recompute the corresponding time-specific identities :math:`\id`
      for this record
      following :ref:`the process laid out for the basic scheme<basic-computing-identities>`

   2. For each of these identities :math:`\id` it computes the corresponding
      identity-based decryption key

      .. math::

         \skids = \ibekeyder(\masterskserver, \id)

      using its master secret key :math:`\masterskserver`. Let :math:`\traceid =
      (\id, \skid)`.

   3. The server now proceeds as in :ref:`basic
      CrowdNotifier<basic-initiate-tracing>` steps 4, 5, and 6 to compute tuples
      :math:`(\traceid, \dayctr, \ctxtnotificationdata)` where it instead uses the
      notification key :math:`\notificationkey` provided by the client rather
      than recomputing it from scratch.

5. Regularly, the server publishes a shuffled batch of tuples :math:`(\traceid, \dayctr, \ctxtnotificationdata)`.

The information that is uploaded to the backend server -- the pre identity :math:`\preid`, the notification key :math:`\notificationkey`, and the values :math:`\timekey` -- do not reveal to non-visitors any information about the :term:`Locations<Location>` they correspond to. The :ref:`cryptographic procedure used to compute these <basic-computing-identities>` and the presence of a strong cryptographic seed in the QR codes ensures that without knowledge of the seed, these values are pseudo random.

The values :math:`\timekey` are time-slot specific. As a result, a malicious server can only compute identities :math:`\id` for the time slots reported by the app. The :ref:`basic CrowdNotifier scheme<basic-crowdnotifier>` instead relies on the :term:`Location Owner` to validate the requested time slots to protect against malicious servers.

We assume that apps use cover traffic to hide from network observers that a user has been diagnosed with COVID-19. When Server-Based CrowdNotifier is combined with a GAEN-enabled app, this dummy traffic should be aligned so as not to trivially reveal real uploads. We refer to the DP-3T best practices document :cite:p:`bestpractices` for more details on how to do this.


Presence Tracing and Notification
=================================

The records published by the server have exactly the same format as in the basic CrowdNotifier scheme. These records will enable apps to decrypt the encrypted records, as they contain the correct identity-based decryption keys corresponding to the QR codes that these clients scanned. So notification will proceed :ref:`exactly as for the basic scheme<basic-presence-notification>`.

Since Server-Based CrowdNotifier clients store more extensive records, they can avoid the trial decryption step. These apps proceed as follows.

1. The app downloads all :math:`(\traceid, \dayctr, \ctxtnotificationdata)` tuples
   that were published since the last time it checked. Let :math:`\traceid = (\id, \skid)`.

2. The app checks if any of the records it stored contain the identity :math:`\id`.
   If so, the app uses the stored :math:`\notificationkey` in that record
   to decrypt :math:`\ctxtnotificationdata` and recover:

   .. math::

      \notificationdata = (\entryplus, \exitplus, m)

   if decryption fails, it moves on to the next matching tuple.

3. The app compares the reported visit times :math:`\entryplus` and :math:`\exitplus`
   with the visit times it stored.
   If there is an overlap it notifies the user
   using the recovered message :math:`m`.


Security and Privacy Analysis
=============================

We provide an analysis of the privacy properties of Server-Based CrowdNotifier. We refer to the white paper :cite:p:`whitepaper` for a detailed description of the properties we refer below as PUX, PLX, or SX.

Privacy of Users
----------------

We first consider privacy of users. Like in the Basic CrowdNotifier, there is never any collection of personal data at a location (ensuring PU2). There is no network traffic related to notifications, and thus no adversary can learn who is notified based on network traffic (ensuring PU4). Privacy of positive status is protected from network adversaries by dummy uploads using the methods described in :cite:p:`bestpractices` (ensuring PU5).

If records are stored in the clear, as described above, PU3 is not fulfilled.
Below, we describe a modification which enables users to store records that do not directly reveal the locations' identifier stored on the phone. This ensures that the Server-Based CrowdNotifier records stored on a user's phone do not reveal a user's visits (ensuring PU3). 

Finally, regarding central collection of data (PU1), in Server-Based CrowdNotifier there is no explicit central collection of visitor data. However, some information about users' might be deduced based on the interactions of the system. These leaks are *inherent* to the fact that in Server-Based CrowdNotifier, to enable fast notifications, users upload their visited locations in a single group, and mixed batches of such groups are published without large delays.

For our analysis we separate two adversaries: the :term:`Backend Server` and other users.

Adversarial Backend Server
^^^^^^^^^^^^^^^^^^^^^^^^^^

The :term:`Backend Server` receives all uploaded information from a single positive user in a single group. The :term:`Backend Server` can derive the following information from these uploads.

1. If the :term:`Backend Server` can map identifiers (or QR codes) to real locations, the backend can learn groups of locations visited by positive users. If the system is deployed with a registration service for venues, the backend would know all identifier-location pairs.

2. From the timestamps in the records uploaded, the :term:`Backend Server` can learn temporal patterns about positive users (e.g., whether users work morning shifts or work night shifts).

3. As uploaded location identifiers are shared among users, the server can learn co-locations among positive users at a location.

Whether in the previous attacks the :term:`Backend Server` can map users to real identities depends on whether users communicate anonymously with the :term:`Backend Server`. Re-identification can also happen if the groups of locations can only be associated to one or few users. To reduce the power of this attack, we recommend that users are given the capability to redact the traces they upload to skip compromising or identifying locations.

We discuss below mechanisms to mitigate these attacks.


Adversarial Users
^^^^^^^^^^^^^^^^^

The :term:`Backend Server` regularly broadcasts batches of data uploaded by positive users. An adversarial user (or anyone else) can uses these public batches to try to learn information about the visit patterns of positive users. This adversary cannot associate records in the published batches to individual users because the :term:`Backend Server` anonymizes records before broadcasting them.

Published records consists of a time-specific location identifier and other cryptographic information. Records that the adversary cannot map to real locations, e.g., because the adversary doesn't know the corresponding QR code, provide very little information. At best, the adversary can detect the existence of high-risk events because the same identifier is reported more than once. The adversary, however, cannot associate these repeated identifiers to a location, nor to a specific time slot.

The adversary can learn more information about published batches if it can map records to real locations. To do so, it can use the information contained in that location's QR code. It can obtain these QR codes by visiting these locations either individually, or crowd-sourcing the visits to a group of collaborators.

Given these QR codes, the adversary can try to recover partial location traces.
For each batch of released identifiers, it looks up the corresponding visited locations and visit times. The adversary can then use geographic information (where locations are) and timing (when they were visited), to try to reconstruct potential location traces. And from these traces re-identify positive users. These attacks are easier to do when the location traces published in the same batch do not mix (e.g., the batch contains visits from one user that lives in Zurich, and one set of visits from a user in Lausanne).

There are several options to mitigate this attack:

1. Ensure that QR codes of :term:`Locations<Location>` are rotated frequently to make collecting QR codes much harder. We expect this to be the case for private events, where QR codes are one-use.

2. Release tracing information in larger batches, to decrease the probability of identifying the underlying location traces. This would delay the publication of traces and therefore the notifications, reducing the advantage of Server-Based CrowdNotifier over the basic protocol.

3. Apply a filter on published location data to only release the urgent (e.g., reported more than once) locations; or only those in which the risk of transmission is high (e.g., release bars, but not a seated dining with social distancing).


Privacy of Locations
--------------------

The following properties are shared between the Server-Based CrowdNotifier and basic CrowdNotifier schemes with respect to :term:`Locations<Location>`: Non-visitors (that do not collude with visitors) cannot recognize the broadcasted information, and thus cannot determine which locations where notified (ensuring PL1). To ensure location privacy with respect to non-contemporary visitors (PL2), locations must frequently rotate their QR code. Server-Based CrowdNotifier does not require a database of locations (PL3 achieved), and does not require uploads by locations (PL4 achieved).



Security
--------

We focus on abuse prevention properties: prevention of fake notification for users (S1) and prevention of notifications targeting a particular location (S2). The basic CrowdNotifier scheme requires cooperation of the :term:`Location Owner` and the :term:`Health Authority` to trigger notifications. Server-Based CrowdNotifier has less strict protections.

First, the :term:`Backend Server` can trigger notifications for any :term:`Location` for which it can obtain the QR code at that :term:`Location`.

Second, when uploaded traces by index cases are not validated, malicious users might add arbitrary visits to their uploads; either by reporting different visit times, or by reporting locations that they did not visit (using QR codes they obtained elsewhere). This opportunity can be used by malicious users (or the :term:`Backend Server`) to target visitors of particular locations.

To mitigate the second attack, we recommend to sanity check uploads and to limit both the number of reported visits as well as their duration.



Privacy enhancements
====================

Improving privacy of records in the app
---------------------------------------

As explained in the CrowdNotifier white paper :cite:p:`whitepaper`, users might need strong privacy properties of the records stored on their phone. In the variant explained above, an adversary with access to the user's phone and the location records stored therein, and who has access to the QR code of the  :term:`Location` visited by that user, can easily determine where users went. In the basic CrowdNotifier scheme this attack does not work.

The Server-Based CrowdNotifier scheme admits an easy modification that strengthens privacy of records on the phone. To do so, clients use the basic CrowdNotifier approach and store an encrypted record for their visit. Only when the server generates correct tracing keys can this record be decrypted.

To enable notification of other users, Server-Based CrowdNotifier requires clients to store other data -- the pre identity :math:`\preid`, the notification key :math:`\notificationkey` and time-slot specific keys :math:`\timekey`. To protect these, the client could encrypt them against the :term:`Backend Server`'s public key before storing them. This approach comes at the cost of clients not being able to redact these records anymore before uploading them.

We point out that that in some deployment scenarios, this protection is limited. A determined attacker can use the :term:`Backend Server` as a decryption oracle to recover, say, :math:`\preid`, and thus determine a user's location visits after all.

Therefore, we recommend that, if possible, clients store only the encrypted basic CrowdNotifier records for sensitive visits. This enables them to receive notifications at no privacy risk.


Improving privacy of users towards the Backend server
-----------------------------------------------------

For the privacy attacks on users carried out by the server to be effective, the server needs to be able to map uploads to real identities. A strong defense for users is to use anonymous communications systems when uploading information in order to hide their IP address from the :term:`Backend Server`. 

By hiding their network identity, users limit the impact of the attack to cases for which (i) the :term:`Backend Server` has knowledge of the QR codes of more that one of the locations visited by the user (which will rarely include private events whose keys are used only once) and (ii) those locations are enough information to re-identify the user.

To further reduce the re-identification capability, system deployments are encouraged to include redaction to let users remove identifying locations from their upload list. 

For co-location attacks, which would be possible even if the adversary does not know the location in which users have been present, the use of anonymous communication renders the attack useless: the :term:`Backend Server` learns that two or more users were at the same location, but not whom.

One could be tempted to use dummy check-ins to try to prevent the :term:`Backend Server` from learning the locations visited by users. However, the use of dummies does not help against an adversary that has access to pairs of real locations and their QR codes. This adversary can use her knowledge to filter out dummy check-ins (the adversary removes check-ins that do not correspond to any known QR). If the adversary cannot associate a check-in to a QR code, then there is no privacy risk to start with as the adversary cannot identify the corresponding location.





.. rubric:: Footnotes

.. [#cwa] https://github.com/corona-warn-app/cwa-documentation/blob/master/event_registration.md
