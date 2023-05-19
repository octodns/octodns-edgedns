#
#
#

from os.path import dirname, join
from unittest import TestCase

from requests import HTTPError
from requests_mock import ANY
from requests_mock import mock as requests_mock

from octodns.provider.yaml import YamlProvider
from octodns.record import Record
from octodns.zone import Zone

from octodns_edgedns import AkamaiProvider


class TestEdgeDnsProvider(TestCase):
    expected = Zone('unit.tests.', [])
    source = YamlProvider('test', join(dirname(__file__), 'config'))
    source.populate(expected)

    # Our test suite differs a bit, add our NS and remove the simple one
    expected.add_record(
        Record.new(
            expected,
            'under',
            {
                'ttl': 3600,
                'type': 'NS',
                'values': ['ns1.unit.tests.', 'ns2.unit.tests.'],
            },
        )
    )
    for record in list(expected.records):
        if record.name == 'sub' and record._type == 'NS':
            expected._remove_record(record)
            break

    def test_populate(self):
        provider = AkamaiProvider("test", "secret", "akam.com", "atok", "ctok")

        # Bad Auth
        with requests_mock() as mock:
            mock.get(ANY, status_code=401, text='{"message": "Unauthorized"}')

            with self.assertRaises(Exception) as ctx:
                zone = Zone('unit.tests.', [])
                provider.populate(zone)

            self.assertEqual(401, ctx.exception.response.status_code)

        # general error
        with requests_mock() as mock:
            mock.get(ANY, status_code=502, text='Things caught fire')

            with self.assertRaises(HTTPError) as ctx:
                zone = Zone('unit.tests.', [])
                provider.populate(zone)
            self.assertEqual(502, ctx.exception.response.status_code)

        # Non-existant zone doesn't populate anything
        with requests_mock() as mock:
            mock.get(
                ANY,
                status_code=404,
                text='{"message": "Domain `foo.bar` not found"}',
            )

            zone = Zone('unit.tests.', [])
            provider.populate(zone)
            self.assertEqual(set(), zone.records)

        # No diffs == no changes
        with requests_mock() as mock:
            with open('tests/fixtures/edgedns-records.json') as fh:
                mock.get(ANY, text=fh.read())

            zone = Zone('unit.tests.', [])
            provider.populate(zone)
            self.assertEqual(20, len(zone.records))
            changes = self.expected.changes(zone, provider)
            self.assertEqual(0, len(changes))

        # 2nd populate makes no network calls/all from cache
        again = Zone('unit.tests.', [])
        provider.populate(again)
        self.assertEqual(20, len(again.records))

        # bust the cache
        del provider._zone_records[zone.name]

    def test_apply(self):
        provider = AkamaiProvider(
            "test",
            "s",
            "akam.com",
            "atok",
            "ctok",
            "cid",
            "gid",
            strict_supports=False,
        )

        # tests create update delete through previous state config json
        with requests_mock() as mock:
            with open('tests/fixtures/edgedns-records-prev.json') as fh:
                mock.get(ANY, text=fh.read())

            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)

            changes = provider.apply(plan)
            self.assertEqual(34, changes)

        # Test against a zone that doesn't exist yet
        with requests_mock() as mock:
            with open('tests/fixtures/edgedns-records-prev-other.json') as fh:
                mock.get(ANY, status_code=404)

            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)

            changes = provider.apply(plan)
            self.assertEqual(18, changes)

        # Test against a zone that doesn't exist yet, but gid not provided
        with requests_mock() as mock:
            with open('tests/fixtures/edgedns-records-prev-other.json') as fh:
                mock.get(ANY, status_code=404)
            provider = AkamaiProvider(
                "test",
                "s",
                "akam.com",
                "atok",
                "ctok",
                "cid",
                strict_supports=False,
            )
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)

            changes = provider.apply(plan)
            self.assertEqual(18, changes)

        # Test against a zone that doesn't exist, but cid not provided

        with requests_mock() as mock:
            mock.get(ANY, status_code=404)

            provider = AkamaiProvider(
                "test", "s", "akam.com", "atok", "ctok", strict_supports=False
            )
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)

            try:
                changes = provider.apply(plan)
            except NameError as e:
                expected = "contractId not specified to create zone"
                self.assertEqual(str(e), expected)

    def test_long_txt_records(self):
        provider = AkamaiProvider(
            "test",
            "s",
            "akam.com",
            "atok",
            "ctok",
            "cid",
            "gid",
            strict_supports=False,
        )
        output = AkamaiProvider._params_for_TXT(
            provider,
            [
                "v=DKIM1\\;t=s\\;p=MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtGYOXk57O5ZkxKRMuh3KBfMq7CccVz0iJ57kiPcpyHNrz7XuQX6Z/eUnj5gzQOGvtAPK7ht58Ao/Pyp9dfC8VgkZTEBiiOU3938FhxD1QmjTO8YTEjAMzfsIfp5ShNqKujw8nhLIFEIQw2uO2Pl/q2+3isuJYKdlFQ1iBirR+tAac+IvWUM1FXVau7eqHUASR1kSEyaR0BztmtAGsHo0+yLF+uL1WRgyJPDqD7SYa8v3qf+QMPQ7lCrgdAdWWUbOF++jsqNJh3Cj180YThWZsMybr8zd6fqdC62MOKnRb75EKBY8hZjSRH+cpMxQukjLNEJACsNcZHfJjfDhRzJwLva1dY5UeEQKpSptYwQ78ngXYoLHNRE4HfayKu2fffL7kCRS3YcKGI4FdSurIghhKnnE79kv9l2mu0l5q/3vQWG/TP9F1in6Uz3QCvhh/Pm2RMqwPAk0csgirEdjRkxg1Mlxe9pfNupYxPdESoSrAw2m329BX2HKfdTB1p6HB+zfSq0oHRcsTRJQVPg/iQEQUYYAg/ttQS0pkKDI0ZBaHjCR8w5VXatIKRSxgRVp80sIbLoOSRvJ5IMxPR/V6P4ZaHhfmvx3CQwpHPR9LVThbwTc55WPWGhOf1iF8nx18g6CVfW69usS0F2OKdZfpBJ+WAm2hgOG8izXkJnmSA4tgcsCAwEAAQ=="
            ],
        )
        # Test that TXT record values longer than 255 characters are split
        expected = [
            "\"v=DKIM1;t=s;p=MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtGYOXk57O5ZkxKRMuh3KBfMq7CccVz0iJ57kiPcpyHNrz7XuQX6Z/eUnj5gzQOGvtAPK7ht58Ao/Pyp9dfC8VgkZTEBiiOU3938FhxD1QmjTO8YTEjAMzfsIfp5ShNqKujw8nhLIFEIQw2uO2Pl/q2+3isuJYKdlFQ1iBirR+tAac+IvWUM1FXVau7eqHUASR1kSE\" \"yaR0BztmtAGsHo0+yLF+uL1WRgyJPDqD7SYa8v3qf+QMPQ7lCrgdAdWWUbOF++jsqNJh3Cj180YThWZsMybr8zd6fqdC62MOKnRb75EKBY8hZjSRH+cpMxQukjLNEJACsNcZHfJjfDhRzJwLva1dY5UeEQKpSptYwQ78ngXYoLHNRE4HfayKu2fffL7kCRS3YcKGI4FdSurIghhKnnE79kv9l2mu0l5q/3vQWG/TP9F1in6Uz3QCvhh/Pm2RMqw\" \"PAk0csgirEdjRkxg1Mlxe9pfNupYxPdESoSrAw2m329BX2HKfdTB1p6HB+zfSq0oHRcsTRJQVPg/iQEQUYYAg/ttQS0pkKDI0ZBaHjCR8w5VXatIKRSxgRVp80sIbLoOSRvJ5IMxPR/V6P4ZaHhfmvx3CQwpHPR9LVThbwTc55WPWGhOf1iF8nx18g6CVfW69usS0F2OKdZfpBJ+WAm2hgOG8izXkJnmSA4tgcsCAwEAAQ==\""
        ]
        self.assertEqual(output, expected)
