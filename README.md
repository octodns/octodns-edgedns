## Akamai Edge DNS provider for octoDNS

An [octoDNS](https://github.com/octodns/octodns/) provider that targets [Akamai Edge DNS](https://www.akamai.com/products/edge-dns).

### Installation

#### Command line

```
pip install octodns-edgedns
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.14
octodns-edgedns==0.0.1
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@9da19749e28f68407a1c246dfdf65663cdc1c422#egg=octodns
-e git+https://git@github.com/octodns/octodns-edgedns.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg=octodns_edgedns
```

### Configuration

```yaml
providers:
  edgedns:
    class: octodns_edgedns.AkamaiProvider
    client_secret: env/AKAMAI_CLIENT_SECRET
    host: env/AKAMAI_HOST
    access_token: env/AKAMAI_ACCESS_TOKEN
    client_token: env/AKAMAI_CLIENT_TOKEN
    #contract_id: env/AKAMAI_CONTRACT_ID (optional)
```

The first four variables above can be hidden in environment variables and octoDNS will automatically search for them in the shell. It is possible to also hard-code into the config file: eg, contract_id.

The first four values can be found by generating credentials: https://control.akamai.com/

Configure > Organization > Manage APIs > New API Client for me

Select appropriate group, and fill relevant fields.  For API Service Name, select DNS-Zone Record Management and then set appropriate Access level (Read-Write to make changes).  Then select the "New Credential" button to generate values for above

The contract_id paramater is optional, and only required for creating a new zone. If the zone being managed already exists in Akamai for the user in question, then this paramater is not needed.

### Support Information

#### Records

AkamaiProvider supports A, AAAA, CAA, CNAME, MX, NAPTR, NS, PTR, SPF, SRV, SSHFP, and TXT.

#### Dynamic

AkamaiProvider does not support dynamic records.

### Development

See the [/script/](/script/) directory for some tools to help with the development process. They generally follow the [Script to rule them all](https://github.com/github/scripts-to-rule-them-all) pattern. Most useful is `./script/bootstrap` which will create a venv and install both the runtime and development related requirements. It will also hook up a pre-commit hook that covers most of what's run by CI.
