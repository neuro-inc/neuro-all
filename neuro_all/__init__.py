from neuro_sdk import PluginManager


NEURO_ALL_UPGRADE = """\
You are using Neuro-All {old_ver}, however {new_ver} is available.
You should consider upgrading via the following command:
    pipx upgrade neuro-all
"""


def get_neuro_all_txt(old: str, new: str) -> str:
    return NEURO_ALL_UPGRADE.format(old_ver=old, new_ver=new)


def setup(manager: PluginManager) -> None:
    manager.version_checker.register("neuro-all", get_neuro_all_txt, exclusive=True)
