import yaml

from hem.contracts.asset import Asset


def validate_asset(path):

    with open(path) as f:

        data = yaml.safe_load(f)

    return Asset.model_validate(data["asset"])
