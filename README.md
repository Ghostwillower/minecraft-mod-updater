# Minecraft Mod Auto-Updater

Continuous-integration workflow that:
1. Checks Modrinth and CurseForge to see if a build for the requested Minecraft version already exists.
2. If none is found, rebuilds the mod JAR, rewrites its metadata to the target version, and uploads the rebuilt JAR as a workflow artifact.

## Usage
* Manually trigger the workflow from the “Actions” tab and supply **target_version** (e.g. `1.20.4`).
* Or let the nightly cron run do its thing.
* Grab the rebuilt JAR from the workflow run’s “Artifacts” section.

### Required secrets
| Name                | Purpose                          |
| ------------------- | -------------------------------- |
| `CURSEFORGE_API_KEY`| Access to CurseForge API         |

### Required repository variables
| Name                   | Example            |
| ---------------------- | ------------------ |
| `MODRINTH_PROJECT_ID`  | `abcd1234`         |
| `CURSEFORGE_MOD_ID`    | `123456`           |

No external publishing happens here—just build and ship the JAR artifact.
