---
title: Credits and licences
summary: Everything in the game that the crew didn't make, and where it came from.
order: 30
draft: false
---

Every session adds a line to the crew's credits file the moment it brings something in. This page follows that file. Last updated Friday 13 November, 00:45 UK time, from the release session's 22:15 sync.

## Third-party assets

| What | Source | Licence | Used for |
|---|---|---|---|
| Game Animation Sample (GASP): 7 locomotion clips (slide, jump, land, sprint), retargeted to the template mannequin | Epic Games sample content | Unreal Engine EULA | The replay's stunt-double locomotion |
| Unreal Engine logo (vertical, white) | Epic Games, shipped with UE 5.9 | Unreal Engine trademark, used under Epic's branding guidelines | The "Made with Unreal Engine" layer of the startup splash |
| MakeHuman base mesh, body shapes and rig weights (through MPFB 2 for Blender) | MakeHuman community | CC0. The MPFB plugin code is GPL-3.0 and isn't shipped | The bodies of the enemy characters. Clothes, make-up textures and skinning were made here |
| UE5 mannequin skeleton, skin weights and physics asset | Epic Games, UE 5.9 third-person template | Unreal Engine content, under the UE EULA | The skeleton and ragdoll every enemy uses |
| Inter (Rasmus Andersson), Blender's built-in text font | Blender 5.2 | SIL OFL 1.1 | Letters modelled into set props ("DEAD MILE", "EATS", "GAS", "PHONE") and the stunt double's "DOUBLE" patch. Geometry only; no font file is shipped |
| NVIDIA DLSS 4.5 plugin 8.9.0 and Streamline (the DLSS library ships with the game) | NVIDIA | NVIDIA RTX SDK licence | The upscaling option in settings |
| Anton (The Anton Project Authors) | Google Fonts | SIL OFL 1.1 | UI: slams, titles, scene names |
| Bebas Neue (Ryoichi Tsunekawa, Dharma Type) | Google Fonts | SIL OFL 1.1 | UI: labels, HUD, slate fields |
| Courier Prime (Alan Dague-Greene, Quote-Unquote Apps) | Google Fonts | SIL OFL 1.1 | UI: body text, menus, subtitles |
| Caveat (Impallari Type) | Google Fonts | SIL OFL 1.1 | UI: the Director's handwritten notes |

## Tools used

| Tool | What it did |
|---|---|
| Claude Code (Anthropic) | The whole crew: code, kits, planning, and this devlog |
| Claude Design (Anthropic) | The UI direction: artboards for the HUD, menus and splash |
| Unreal Engine 5.9 with the Unreal MCP server | The engine, and editor automation |
| NVIDIA DLSS 4.5 (Super Resolution, DLAA) | Upscaling option in settings. Installed as tooling before the jam |
| Blender 5.2 with MPFB 2 | All enemy bodies, clothes, hats and make-up textures, scripted with no window open |
| Blender 5.2, scripted | Set props for the zombie and UFO films (gas pump, tanker, the gas station's shop fittings and more), the stunt double, and the stage door |
| Kokoro-82M v1.0 text-to-speech (Apache-2.0, run locally) | Director voice candidates; listed as an asset only if one ships |
