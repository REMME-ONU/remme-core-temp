***************************
Account Transaction Family
***************************

Overview
=========

The Account transaction family provides an information about agent's state mapped to his public key within the REMME blockchain and allows to perform token transfers and retrieve the list of certificates in control as of main operations to date.

The account transaction family plays a critical role during blockchain initialization and executes logic for genesis block initial token release.

Definition of Account Entries
-----------------------------

The following protocol buffers definition defines account entries:

.. code-block:: protobuf

    // Entity storing related info to a public key
    message Account {
         uint64 balance = 1;
         repeated string certificates = 2;
     }

    // Information on weather the genesis emission has occurred
    message GenesisStatus {
        bool status = 1;
    }

Addressing
----------

The address of an entity on the storage is built as follows (where ``public_key`` is a public key of a user in
hexadecimal representation and ``hash512(text)`` returns the hexadecimal representation of ``sha512(text)``):

.. code-block:: python

    address = hash512('account')[:6] + hash512(public_key)[:64]


Transaction Payload
===================

Account transaction family payloads are defined by the following protocol
buffers code:

.. code-block:: protobuf

    // Transfer Payload
    // - Contains receiver address and the amount transaffered.
    message TransferPayload {
        string address_to = 1;
        uint64 value = 2;
    }

    // Genesis Payload
    // - Total supply assigned to a transaction signer's address.
    message GenesisPayload {
        uint64 total_supply = 1;
    }


Transaction Header
==================

Inputs and Outputs
------------------

The inputs and outputs for account family transactions must include:

* Sender's account address
* Receiver's account address

Dependencies
------------

None.


Family
------

- family_name: "account"
- family_version: "0.1"

Encoding
--------

The encoding field must be set to "application/protobuf".


Execution
=========

There is a clear separation of _transfer_from_address (on chain method) and _transfer (public method) to forbid transfers from a reserved *ZERO_ADDRESS* outside of the blockchain scope and help with an addres formation from the public key.

Further, during execution of a transfer, 1) it ensures that the recipient's address is also not among reserved ones, 2) we make sure that the the transaction is not sent to oneself.

We retrieve account entry for the signer account as well as of a recipient.

If either entry doesn't exist on the blockchain yet, we initialise it.

Once we verified that the balance is sufficinet for a transfer, the state of each account gets updated.
