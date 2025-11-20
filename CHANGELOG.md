## v1.1.0 - TBD - New DNS Record Types

Changes:

* Added support for DS (DNSSEC Delegation Signer) records
* Added support for HTTPS (HTTPS Service Binding) records
* Added support for LOC (Location) records
* Added support for SVCB (Service Binding) records
* DS record digests are now normalized to lowercase when reading from and writing
  to Akamai EdgeDNS, ensuring case-insensitive comparison regardless of the case
  used in configuration files
* SSHFP record fingerprints are now normalized to lowercase when reading from and
  writing to Akamai Edge DNS, ensuring case-insensitive comparison regardless of
  the case used in configuration files

## v1.0.0 - 2024-04-29 - Long overdue 1.0

Noteworthy Changes:

* Complete removal of SPF record support, records should be transitioned to TXT
  values before updating to this version.

Changes:

* Address pending octoDNS 2.x deprecations, require minimum of 1.5.x

## v0.0.4 - 2024-01-27 - Primary Zone Creation

* Support for creation of primary zones.
  Includes automatic creation of NS record set,
  and SOA record for zones that do not exist.
* Support for comments, i.e. zone descriptions.

## v0.0.3 - 2023-03-16 - CAA has arrived

* Support for CAA records has been added
* Set a user-agent on outgoing http requests

## v0.0.2 - 2023-02-03 - Now with more PTR values

* Support for multi-value PTRs

## v0.0.1 - 2022-01-07 - Moving

#### Nothworthy Changes

* Initial extraction of AkamaiProvider from octoDNS core

#### Stuff

Nothing
