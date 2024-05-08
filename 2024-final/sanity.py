from challtools.utils import discover_challenges, load_config

paths = discover_challenges()

configs = [load_config(path.parent, search=False, cd=False) for path in paths]

print("challs:", len(set(paths)))
print("ids:", len(set([config["challenge_id"] for config in configs])))
