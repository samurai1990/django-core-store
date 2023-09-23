# Target App API Document


### Create Target
* permission: `Authenticated`

* endpoint: `/targets/`

* HTTP method: `POST`

* Content-Type: `multipart/form-data`

* request:
```json
{
    "ip": "127.0.0.1",
    "whois": "test_user",
    "prefix": "127.0.0.0/24",
    "asn": "12345",
    "aso": "aso12345",
    "port_scan": {
        "http": 80,
        "https": 443,
        "ssh": 22
    },
    "history": {
        "jan": 15,
        "dec": 20,
        "sep": 22
    },
    "type": "test_type",
    "attach_surface": "test_surface",
    "network_diagram": "<File: test.jpg>",
    "dns_records": {"kind": "dns#resourceRecordSet", "name": "example.com.", "rrdatas": ["1.2.3.4"], "ttl": 86400, "type": "A"}
}
```

* ok Response
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "target": {
      "id": "f0f7e061-29db-4ce7-a34d-0e900d3ca822",
      "ip": "127.0.0.1",
      "whois": "test_user",
      "prefix": "127.0.0.0/24",
      "asn": 12345,
      "aso": "aso12345",
      "port_scan": {
        "http": 80,
        "https": 443,
        "ssh": 22
      },
      "history": {
        "jan": 15,
        "dec": 20,
        "sep": 22
      },
      "type": "test_type",
      "attach_surface": "test_surface",
      "network_diagram": "http://minio:9000/diagram/targets/20230920_f0f7e061-29db-4ce7-a34d-0e900d3ca822_django.png?AWSAccessKeyId=minioadmin&Signature=oOdON8hk0hgZxr55jcoZoXh8I2Y%3D&Expires=1695217368",
      "dns_records": {
        "kind": "dns#resourceRecordSet",
        "name": "example.com.",
        "rrdatas": [
          "1.2.3.4"
        ],
        "ttl": 86400,
        "type": "A"
      }
    }
  }
}
```

### Update Target
* permission: `Authenticated`

* endpoint: `/targets/<id>`

* HTTP method: `PATCH`

* request:
```json
{
  "asn":111111
}
```

* ok Response
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "target": {
      "id": "21138307-5a59-4bad-8c96-56d4a6903bd2",
      "ip": "192.168.1.1",
      "whois": "test_user2",
      "prefix": "192.168.1.0/24",
      "asn": 111111,
      "aso": "aso12345",
      "port_scan": {
        "ssh": 22,
        "http": 80,
        "https": 443
      },
      "history": {
        "dec": 20,
        "jan": 15,
        "sep": 22
      },
      "type": "test_type2",
      "attach_surface": "test_surface2",
      "network_diagram": "http://minio:9000/diagram/targets/20230920_21138307-5a59-4bad-8c96-56d4a6903bd2_test.jpg?AWSAccessKeyId=minioadmin&Signature=6YxSCeaPiYrT8ewZu7uf94%2FXSY0%3D&Expires=1695218541",
      "dns_records": {
        "ttl": 86400,
        "kind": "dns#resourceRecordSet",
        "name": "example.com.",
        "type": "A",
        "rrdatas": [
          "1.2.3.4"
        ]
      }
    }
  }
}
```

### Retrieve Target
* permission: `Authenticated`

* endpoint: `/targets/<id>`

* HTTP method: `GET`

* ok Response
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "target": {
      "id": "21138307-5a59-4bad-8c96-56d4a6903bd2",
      "ip": "192.168.1.1",
      "whois": "test_user2",
      "prefix": "192.168.1.0/24",
      "asn": 12345,
      "aso": "aso12345",
      "port_scan": {
        "ssh": 22,
        "http": 80,
        "https": 443
      },
      "history": {
        "dec": 20,
        "jan": 15,
        "sep": 22
      },
      "type": "test_type2",
      "attach_surface": "test_surface2",
      "network_diagram": "http://minio:9000/diagram/targets/20230920_21138307-5a59-4bad-8c96-56d4a6903bd2_test.jpg?AWSAccessKeyId=minioadmin&Signature=b1TSw020L6mrYswfQYTe7xXt67I%3D&Expires=1695218268",
      "dns_records": {
        "ttl": 86400,
        "kind": "dns#resourceRecordSet",
        "name": "example.com.",
        "type": "A",
        "rrdatas": [
          "1.2.3.4"
        ]
      }
    }
  }
}
```
### List Target
* permission: `Authenticated`

* endpoint: `/targets/`

* HTTP method: `GET`

* ok Response
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "targets": [
      {
        "id": "21138307-5a59-4bad-8c96-56d4a6903bd2",
        "ip": "192.168.1.1",
        "whois": "test_user2",
        "prefix": "192.168.1.0/24",
        "asn": 12345,
        "aso": "aso12345",
        "port_scan": {
          "ssh": 22,
          "http": 80,
          "https": 443
        },
        "history": {
          "dec": 20,
          "jan": 15,
          "sep": 22
        },
        "type": "test_type2",
        "attach_surface": "test_surface2",
        "network_diagram": "http://minio:9000/diagram/targets/20230920_21138307-5a59-4bad-8c96-56d4a6903bd2_test.jpg?AWSAccessKeyId=minioadmin&Signature=JQMx6Q%2B4iHgUaxx2sIIfYeTWbbQ%3D&Expires=1695218227",
        "dns_records": {
          "ttl": 86400,
          "kind": "dns#resourceRecordSet",
          "name": "example.com.",
          "type": "A",
          "rrdatas": [
            "1.2.3.4"
          ]
        }
      },
      {
        "id": "f0f7e061-29db-4ce7-a34d-0e900d3ca822",
        "ip": "127.0.0.1",
        "whois": "test_user",
        "prefix": "127.0.0.0/24",
        "asn": 12345,
        "aso": "aso12345",
        "port_scan": {
          "ssh": 22,
          "http": 80,
          "https": 443
        },
        "history": {
          "dec": 20,
          "jan": 15,
          "sep": 22
        },
        "type": "test_type",
        "attach_surface": "test_surface",
        "network_diagram": "http://minio:9000/diagram/targets/20230920_f0f7e061-29db-4ce7-a34d-0e900d3ca822_django.png?AWSAccessKeyId=minioadmin&Signature=%2FB9aKtEDsq4jLY5G%2BYnJxqLjtAE%3D&Expires=1695218227",
        "dns_records": {
          "ttl": 86400,
          "kind": "dns#resourceRecordSet",
          "name": "example.com.",
          "type": "A",
          "rrdatas": [
            "1.2.3.4"
          ]
        }
      }
    ]
  }
}
```

### Delete Target
* permission: `Authenticated`

* endpoint: `/targets/<id>`

* HTTP method: `DELETE`

* http status code: `204`

---