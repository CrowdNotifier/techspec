.. _managed-crowdnotifier:

*********************
Managed CrowdNotifier
*********************

In this section we introduce a managed version of CrowdNotifier where an :term:`Organization` manages many :term:`Locations<Location>` at once without having to store a tracing QR code for each.

The design in the white paper assumes that each :term:`Location Owner` manages a single location, and can thus store the single tracing QR code containing the tracing information. In reality, a single restaurant may consist of several different rooms, or locations. And a large company might want to manage many (meeting) rooms at the same time. In these cases, storing tracing QR codes for each of these locations becomes cumbersome. Instead, we show how a single tracing key can be used to manage all rooms and locations under control of the same entity.

The Idea
========
In the :ref:`basic CrowdNotifier scheme <basic-crowdnotifier>`, the :term:`Location Owner` creates one master public key and corresponding private keys per location. In this section we show how the same master key can be used for *all* :term:`Locations <Location>` managed by the same :term:`Organization`. Thereby drastically simplifying key management.

The :term:`Organization` still needs to store information to facilitate tracing. We assume the :term:`Organization` has a local database in which it keeps track of the following values:

* The master public key :math:`\masterpk` for this :term:`Organization`
* The ciphertext :math:`\ctxtha` for the :term:`Health Authority`
* For each :term:`Location`, a copy of the QR code :math:`\payload`.

To initiate notifications, the :term:`Organization` also needs the master secret key :math:`\masterskorganization`. The security of tracing information hinges on keeping the master secret :math:`\masterskorganization` secure. In the following, we describe how this key can be derived from a passphrase. As a result, no security-critical information needs to be stored in the local database. The passphrase itself can be stored in a password management system.

Given the local database, and the master secret key, the manager can recover all information needed for tracing, and compute the per location tracing keys. In the following, we describe these steps in more detail below.

Organization Setup
==================

Initializing an :term:`Organization` proceeds as follows:

1. The system generates a strong passphrase of at least 256 bits of entropy. The
   operator should store the passphrase securely, for example in a password
   management system. The passphrase is the only security-critical component and
   is only needed to initiate tracing of rooms. It is not needed to add new
   rooms to the system.

2. First, setup computes the organization's master secret key as using the passphrase:

   .. math::

      \masterskorganization \gets \hash(\code{passphrase}) \mod \grouporder,

   where :math:`\grouporder` is the group order and :math:`\masterpkorganization =
   \generator_2^{\masterskorganization}` the corresponding :term:`Organization`'s
   public key.

   Ideally, the output of :math:`\hash` should be much longer than the bit length
   of :math:`\grouporder`. For example, using SHA512 for :math:`\grouporder` of 256 bits.
   Alternatively, :math:`\masterskorganization` can be directly computed by an appropriate
   method for hashing to the field :math:`\mathbb{Z}_{\grouporder}` if provided by the
   cryptographic library.

3. Setup then proceeds as in the original QR code generation process to compute
   the health authority key-pair :math:`\masterpkhealth, \masterskhealth`; the
   encrypted master secret key :math:`\ctxtha` for the health authority; and the
   master public key :math:`\masterpk = \masterpkorganization \cdot
   \masterpkhealth`. See the :ref:`Setting-up a Location in the basic
   CrowdNotifier scheme <basic-setting-up-location>`.

4. The system then stores :math:`\masterpk` and :math:`\ctxtha` in the local
   database. It does not store any of the other generated values.
   In particular, as in the :ref:`basic CrowdNotifier scheme<basic-crowdnotifier>`,
   it is essential for abuse resistance that the setup process does not store :math:`\masterskhealth`.


In code, the setup script computes the following values:

.. code-block:: javascript

   // Input: the public key pkha of the Health Authority
   // Input: strong passphrase pp

   // Generate mskO, mpkO from passphrase pp
   const mskO = new mcl.Fr();
   mskO.setHashOf(from_string(pp));
   const mpkO = mcl.mul(baseG2(), mskO);

   // Compute IBE key-pair for health authority
   const [mpkha, mskha] = keyGen();

   // Compute resulting master public key
   const mpk = mcl.add(mpkO, mpkha);

   // Compute encrypted master secret key for health authority
   const ctxtha = crypto_box_seal(mskha.serialize(), pkh);


Setting-up a New Location
=========================

To add a new :term:`Location`, the :term:`Organization` supplies the information describing the new :term:`Location` (e.g., name, address), see also :ref:`the entry code format<entry-code-format>`. The system then proceeds :ref:`as in the basic scheme <basic-setting-up-location>`, except that it uses the master public key :math:`\masterpk` from the database:

1. Retrieve the master public key :math:`\masterpk` from the local database.
2. Pick a random 32-byte seed :math:`\seed`
3. Construct the entry QR code :ref:`as in the basic scheme<entry-code-format>` by including :math:`\masterpk`, :math:`\seed`, and the description of the location.
4. Store the resulting QR-code payload in the local database.



Initiating Presence Notification
================================

To initiate tracing, the :term:`Health Authority` contacts the :term:`Organization` and specifies the room/location for which it wants to notify the visitors. The operator uses the passphrase generated initially to recover the information that would normally be in the tracing QR code as follows:

1. The :term:`Organization` enters the :math:`\code{passphrase}` into the local system. The system recomputes the organization's master secret key :math:`\masterskorganization` from the passphrase.

2. The system retrieves the master public key :math:`\masterpk` and the encrypted master secret key :math:`\ctxtha` of the health authority from the database.

3. For the location (e.g., a room) specified by the :term:`Health Authority`, retrieve the stored payload :math:`\payload` from the database.

4. Proceed as in :ref:`initiating presence notification of the basic scheme<basic-initiate-tracing>` where :math:`\masterskvenue = \masterskorganization`.
