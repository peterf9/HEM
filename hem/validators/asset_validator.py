from hem.contracts.asset import Asset


class AssetValidator:

    def validate(self, assets: list[Asset]) -> None:

        ids = set()

        for asset in assets:

            if asset.id in ids:
                raise ValueError(
                    f"Duplicate Asset ID: {asset.id}"
                )

            ids.add(asset.id)
