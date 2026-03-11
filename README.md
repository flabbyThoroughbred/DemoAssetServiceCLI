# DemoAssetServiceCLI

A Click command line interface for interacting with the AssetServiceValidation
module.

How to use:
    install requirements:
        - python -m pip install -r requirements.txt
    This will install the ASV module and its dependencies.

    run CLI:
        - python cli.py

    For demonstration purposes, the local database must be initialized. Run:
        - python cli.py build-demo-tables
    
    Remove database tables:
        - python cli.py drop-demo-tables


    * All attributes are assumed string type unless otherwise noted.
    The following attributes are type validated and will match the following:
        - type ["character", "dressing", "environment", "fx", "prop", "set", "vehicle"]
        - department ["modeling", "texturing", "rigging", "animation", "cfx", "fx"]
        - status ["active", "inactive"]


    Ingest from a json file:
        - python cli.py load <your path>
    
    Add an Asset
        - python cli.py add <name> <type>
        ie python.cli.py add guy character
    
    Retrieve an Asset:
        - python cli.py get <name> <type>
        ie python.cli.py get guy character

    List Assets:
        - python cli.py list --asset-name <name> --asset-type <type>
        # note - both asset-name and asset-type can be left blank and
        will return all assets

    Add Asset Version:
        - python cli.py versions add <name> <type> <department> <version_num> <status>
        ie python cli.py versions add guy character modeling 1 status

    Get Asset Version:
        - python cli.py versions get <name> <type> <department> <version_num> <status>

    List Asset Version(s):
        - python cli.py versions add <name> <type> --department <department> --version <version_num> --status <status>
        # note - department, version and status are considered optional here.
