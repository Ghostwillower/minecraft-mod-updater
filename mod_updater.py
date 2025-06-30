import json
import os
import tempfile
import zipfile
import requests


def version_exists(modrinth_id, curse_id, version, curse_key):
    """Return True if a build for the given version exists on Modrinth or CurseForge."""
    api = f"https://api.modrinth.com/v2/project/{modrinth_id}/version?loaders=fabric&game_versions={version}"
    try:
        r = requests.get(api, timeout=10)
        if r.ok and r.json() != []:
            return True
    except Exception:
        pass

    api = f"https://api.curseforge.com/v1/mods/{curse_id}/files?gameVersion={version}"
    headers = {"x-api-key": curse_key}
    try:
        r = requests.get(api, headers=headers, timeout=10)
        if r.ok and r.json().get('data'):
            return True
    except Exception:
        pass
    return False


def update_jar(jar_path, version):
    """Retarget the given JAR to the specified Minecraft version and return the path to the new file."""
    mod_name = os.path.splitext(os.path.basename(jar_path))[0]
    out_name = mod_name + '}{' + version + '.jar'
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            jar.extractall(tmp)

        mods_toml = os.path.join(tmp, 'META-INF', 'mods.toml')
        if os.path.isfile(mods_toml):
            data = []
            with open(mods_toml, 'r') as f:
                for line in f:
                    if line.strip().startswith('mcversion'):
                        data.append(f'    mcversion = "{version}"\n')
                    else:
                        data.append(line)
            with open(mods_toml, 'w') as f:
                f.writelines(data)

        fabric_json = os.path.join(tmp, 'fabric.mod.json')
        if os.path.isfile(fabric_json):
            with open(fabric_json, 'r') as f:
                j = json.load(f)
            j.setdefault('depends', {})['minecraft'] = version
            with open(fabric_json, 'w') as f:
                json.dump(j, f, indent=2)

        out_path = os.path.join(os.path.dirname(jar_path), out_name)
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as out:
            for root, _, files in os.walk(tmp):
                for fn in files:
                    fp = os.path.join(root, fn)
                    out.write(fp, os.path.relpath(fp, tmp))
    return out_path
