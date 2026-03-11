"""
Command-line interface for the Asset Service.
"""

import click
from AssetServiceController import AssetSvc

@click.group()
@click.pass_context
def cli(ctx):
    """Asset Validation & Registration Service CLI"""
    pass


@cli.command()
@click.pass_context
def build_demo_tables(ctx):
    """Builds demonstration tables"""
    _service = ctx.obj["service"]
    _service._build_tables()


@cli.command()
@click.pass_context
def drop_demo_tables(ctx):
    """Tear down demonstration tables"""
    _service = ctx.obj["service"]
    _service._drop_tables()


@cli.command()
@click.argument("file_path", type=click.Path(exists=True, resolve_path=True))
@click.pass_context
def load(ctx, file_path):
    """Load assets from a JSON file."""
    _service = ctx.obj["service"]
    _service.batch_ingest_data(dataFile=file_path)
    click.echo("Ingest complete.")


@cli.command()
@click.argument("asset_name")
@click.argument("asset_type")
@click.pass_context
def add(ctx, asset_name, asset_type):
    """Add an asset from a JSON file."""
    _service = ctx.obj["service"]
    _id = _service.add_asset(asset_name=asset_name, asset_type=asset_type)    
    added_asset = {"name": asset_name, "type": asset_type, "id": _id}
    if (_id):
        click.echo(f"added asset version: {added_asset}")    


@cli.command()
@click.argument("asset_name")
@click.argument("asset_type")
@click.pass_context
def get(ctx, asset_name, asset_type):
    """Get an asset by name and type."""
    _service = ctx.obj["service"]
    asset = _service.get_assets(asset_name=asset_name, asset_type=asset_type)
    if asset:
        click.echo(f"asset found: {asset[0]}")
    else:
        click.echo(
            f"no asset found with name '{asset_name}' and type '{asset_type}'"
        )


@cli.command(name="list")
@click.option(
    "--asset-name",
    "asset_name",
    required=False,
    default=None,
    help="Filter by asset name",
)
@click.option(
    "--asset-type",
    "asset_type",
    required=False,
    default=None,
    help="Filter by asset type",
)
@click.pass_context
def list_cmd(ctx, asset_name, asset_type):
    """
    List all assets.
    """
    _service = ctx.obj["service"]
    assets = _service.get_assets(
        asset_name=asset_name,
        asset_type=asset_type
    )
    if assets:
        click.echo("found assets --")
    else:
        click.echo(
            f"no assets found with name '{asset_name}' and type '{asset_type}'"
        )
    for asset in assets:
        click.echo(asset)


@cli.command(name="list-failed")
@click.pass_context
def list_failed(ctx):
    """List all failed asset and asset version additions"""
    _service = ctx.obj["service"]
    failed = _service.list_failed_adds()
    if failed:
        click.echo("found failed additions -- ")
    else:
        click.echo("No failed data additions could be found.")
    for record in failed:
        click.echo(record)


@cli.group()
def versions():
    """CLI group to manage asset version subcommands"""
    pass


@versions.command("add")
@click.argument("asset_name")
@click.argument("asset_type")
@click.argument("department")
@click.argument("version_num", type=int)
@click.argument("status")
@click.pass_context
def versions_add(ctx, asset_name, asset_type, department, version_num, status):
    """Add an asset version from a JSON file."""
    _service = ctx.obj["service"]

    _id = _service.add_asset_version(
        asset_name=asset_name,
        asset_type=asset_type,
        department=department,
        version_num=version_num,
        status=status
    )
    if (_id):
        click.echo(f"added asset version. id: {_id}")


@versions.command("get")
@click.argument("asset_name")
@click.argument("asset_type")
@click.argument("department")
@click.argument("version_num", type=int)
@click.pass_context
def versions_get(ctx, asset_name, asset_type, department, version_num):
    """Get a specific asset version."""
    _service = ctx.obj["service"]
    asset_version = _service.get_asset_version(
        asset_name=asset_name,
        asset_type=asset_type,
        department=department,
        version_num=version_num
    )    
    click.echo(f"found asset version: {asset_version}")

@versions.command("list")
@click.argument("asset_name")
@click.argument("asset_type")
@click.option("--department", required=False, default=None, help="Filter by department")
@click.option("--status", required=False, default=None, help="Filter by status")
@click.option(
    "--version", required=False, default=None, type=int, help="Filter by version"
)
@click.pass_context
def versions_list(ctx, asset_name, asset_type, department, status, version):
    """
    List all versions of an asset version by the given parameters.
    """
    _service = ctx.obj["service"]
    asset_versions = _service.list_asset_versions(
        asset_name=asset_name,
        asset_type=asset_type,
        department=department,
        version_num=version,
        status=status
    )
    if asset_versions:
        click.echo("found asset versions --")
    else:
        click.echo(
            f"no asset versions found with name '{asset_name}' and type '{asset_type}'"
        )
    for av in asset_versions:
        click.echo(av)


def main():
    """Entry point for the CLI."""
    svc = AssetSvc
    cli(obj={"service": svc})


if __name__ == "__main__":
    main()