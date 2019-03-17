# ambiverse-client

[![](https://img.shields.io/badge/project-Risklio-green.svg?style=flat-square)](https://risklio.com/)

**Note:** This client is not affiliated with Ambiverse or the Max-Planck-Institute.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [License](#license)

## Install

Install with pip:

```sh
pip install ambiverse-client
```

## Usage

### KnowledgeGraph Client

```py
from ambiverseclient.clients import KnowledgeGraph

kg = KnowledgeGraph(API_ENDPOINT_HOST, port=API_ENDPOINT_PORT)
entity_list = ["http://www.wikidata.org/entity/Q104493", "http://www.wikidata.org/entity/Q103968"]
result = kg.entities(entity_list)
```

### AmbiverseNLU Client

```py
from ambiverseclient.clients import AmbiverseNLU

ac = AmbiverseNLU(API_ENDPOINT_HOST, port=API_ENDPOINT_PORT)
request_doc = AnalyzeInput(docId="test", language="en")
request_doc.text = """Brexit: UBS to move London jobs to Europe as lack of transition deal forces 'significant changes'
                      Swiss banking giant expects to merge UK entity with its German-headquartered European ..."""
ac.analyze(inp)
```

## License

This code is distributed under the terms of the GPLv3  license.  Details can be found in the file
[LICENSE](LICENSE) in this repository.

## Package Author
Linus Kohl, <linus@riskl.io>
