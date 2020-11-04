.. _building-blocks:

*****************************
Cryptographic Building Blocks
*****************************

A short overview of the cryptographic primitives used by CrowdNotifier.


Basic Primitives
================

* SHA256 - The usual hash function
* HKDF - Hash-Based Key Derivation Function based on HMAC and SHA256.

.. _symmetric-encryption:

Symmetric-key Encryption
========================

CrowdNotifier uses symmetric encryption to send data that only visitors of (notified) locations can read. For this, we use a authenticated encryption scheme given by the algorithms :math:`\aeenc` and :math:`\aedec`. We construct these using XSalsa20 (as stream cipher) and Poly1305 (as MAC).

As implementation, we use the following algorithms from `libsodium <https://libsodium.gitbook.io/doc/>`_:

 * :math:`\aeenc`: `crypto_secretbox_easy <https://libsodium.gitbook.io/doc/secret-key_cryptography/secretbox#combined-mode>`_
 * :math:`\aedec`: `crypto_secretbox_open_easy <https://libsodium.gitbook.io/doc/secret-key_cryptography/secretbox#combined-mode>`_

Public-key Encryption
=====================

CrowdNotifier relies on a regular CCA2 secure public-key scheme given by the algorithms :math:`\keygen`, :math:`\enc`, and :math:`\dec` with the usual semantics:

* :math:`(\pk, \sk) \gets \keygen()`. Generates a public-private key-pair.
* :math:`\ctxt \gets \enc(\pk, m)`. Given a public key :math:`\pk` and a message :math:`m` outputs a ciphertext :math:`\ctxt`.
* :math:`m \gets \dec(\sk, \ctxt)`. Given a private key :math:`\sk` and a ciphertext :math:`\ctxt` outputs a message :math:`m` or a failure symbol :math:`\bot`.

We construct these using X25519 for key-exchange and XSalsa20-Poly1305 for the subsequent symmetric encryption.

As implementation, we use the following algorithms from `libsodium <https://libsodium.gitbook.io/doc/>`_:

  * :math:`\keygen`: `crypto_box_keypair <https://libsodium.gitbook.io/doc/public-key_cryptography/authenticated_encryption#key-pair-generation>`_
  * :math:`\enc`: `crypto_box_seal <https://libsodium.gitbook.io/doc/public-key_cryptography/sealed_boxes#usage>`_
  * :math:`\dec`: `crypto_box_seal_open <https://libsodium.gitbook.io/doc/public-key_cryptography/sealed_boxes#usage>`_

.. _ibe-intro:

Identity-Based Encryption
=========================

CrowdNotifier relies on an identity-based encryption scheme to provide its most important properties. In an identity-based encryption scheme, messages can be encrypted against identities without requiring a specific key-pair to be generated for each identity. Instead, a trusted authority -- in our case usually a location owner or organization -- generates a master public key :math:`\masterpk` and a corresponding master private key :math:`\mastersk` by running the :math:`\ibekeygen` algorithm. We emphasize that each location has its own corresponding public key :math:`\masterpk`.

To encrypt a message :math:`m` against an identity :math:`\id` under the public key :math:`\masterpk`, a party (in our case a visitor) runs :math:`\ctxt \gets \ibeenc(\masterpk, \id, m)`. To decrypt this ciphertext, the trust authority (e.g., location or organization) first computes the corresponding identity-based decryption key :math:`\skid \gets \ibekeyder(\masterpk, \mastersk, \id)`. Given the identity-based decryption key :math:`\skid` a visitor (user) can then decrypt a ciphertext :math:`\ctxt` encrypted under an identity :math:`\id` by running :math:`m \gets \ibedec(\id,\allowbreak \skid,\allowbreak \ctxt)`.

We refer to the :ref:`identity-based encryption` section for the full details. For completeness, we introduce the full syntax that we use:

* :math:`\pp \gets \ibecommonsetup(1^\secpar)`. Generates the common parameters :math:`\pp`. Typically these parameters are part of the implementation.

* :math:`(\masterpk, \mastersk) \gets \ibekeygen(\pp)`. Generates a master public-private key pair.

* :math:`\skid \gets \ibekeyder(\masterpk, \mastersk, \id)`. On input of a master public key :math:`\masterpk`, a master private key :math:`\mastersk`, and an identity :math:`\id`; outputs private decryption key :math:`\skid` corresponding to this identity.

* :math:`\ctxt \gets \ibeenc(\masterpk, \id, m)`. On input of a master public key :math:`\masterpk`, an identity :math:`\id`, and a message :math:`m`, outputs a ciphertext :math:`\ctxt`.

* :math:`m \gets \ibedec(\id, \skid, \ctxt)`. On input of an identity :math:`\id`, a private key :math:`\skid`, and a ciphertext :math:`\ctxt`, either outputs the decryption :math:`m` of :math:`\ctxt`, or :math:`\bot` if decryption fails.

We implement the concrete :ref:`identity-based encryption` scheme over the BLS12-381 curve. As instantiation we use the `mcl library <https://github.com/herumi/mcl>`_. We refer to :ref:`later sections for more information on the implementation <ibe-implementation>`.
