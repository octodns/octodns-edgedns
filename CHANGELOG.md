## 1.1.0 - 2026-04-03

Minor:
* Add support for TLSA, DS, HTTPS, LOC, and SVCB records. Fix CAA record parsing to properly handle quoted values. - [#63](https://github.com/octodns/octodns-edgedns/pull/63)

Patch:
* Use new [changelet](https://github.com/octodns/changelet) tooling - [#55](https://github.com/octodns/octodns-edgedns/pull/55)

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
