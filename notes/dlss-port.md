# Porting NVIDIA DLSS 4.5 from UE 5.8 to UE 5.9 (pre-production, Wed 11 Nov)

Notes for the Devlog session (the human asked for this to be devlogged, "even if it doesn't work"). Facts and timings below are
from the actual run. It's tooling work before the jam (allowed by §7(h), declared in `Release/DECLARATION.md`).

## Why
The NVIDIA RTX Award (a GeForce RTX 5090) needs a Render Royalty entry that uses DLSS 4.5, an NvRTX feature or NVIDIA ACE. DLSS is
the only realistic one for us. NVIDIA's DLSS 4.5 plugin (v8.9.0, released 16 Oct 2026) supports UE 5.5-5.8. We're on a **5.9 source build**.
The human also wanted Frame Generation and Reflex as simple settings toggles.

## What happened, step by step
1. **The download:** a 1.1 GB zip with 11 plugins (DLSS, NIS, Streamline and friends), docs and a sample. We only needed DLSS Super
   Resolution, DLSS Frame Generation (StreamlineDLSSG), Reflex, and their two support plugins (StreamlineCore, StreamlineNGXCommon):
   5 plugins, 20 C++ modules. The plugin ships full source, which made a port possible: its prebuilt files are for 5.8 and won't load in 5.9.
2. **A test bench:** an empty "host" project containing just those plugins, with the 5.8 binaries set aside, compiled against our 5.9
   engine. Our real projects and the running editor were left alone.
3. **Attempt 1, failed instantly:** a quoting mistake in the build command; the build tool couldn't find the project. (Our mistake, not NVIDIA's.)
4. **Attempt 2, failed:** Windows' 260-character path limit. The scratch folder's path was so long that intermediate build files went past
   it. We moved the bench to `E:\DLSSHost`.
5. **Attempt 3, 2 minutes, mostly compiled:** most modules built against 5.9 unchanged. The failures were all one thing: **UE 5.9
   validates log-message format strings at compile time**, and NVIDIA's 5.8 code passes 64-bit numbers and enum values to `%d` and
   `%u`. Four messages were fixed with `%lld`.
6. **Attempts 4 and 5:** more of the same pattern, in seven more places across the DLSS and Streamline code. Each was fixed with an
   explicit integer cast. Then we spotted the cleaner, intended fix:
7. **The real fix:** UE 5.9 has a per-module switch for exactly this, `bValidateFormatStrings` in a module's build rules. We set it to
   `false` in all 20 NVIDIA modules (a one-line, commented change in each `.Build.cs`). **Attempt 6: "Result: Succeeded"** in 2 minutes 16 s.
   All 20 modules built for the 5.9 editor.
8. **Installing:** copied into the engine's plugin folder (`Engine/Plugins/Marketplace/NVIDIA`), so every project on this engine gets it:
   tomorrow's jam project, and every gameplay worktree, with nothing added to the game's repo.
9. **First launch, blocked by a dialog:** "'DLSS' is Incompatible". The plugin files still declared `"EngineVersion": "5.8.0"`. Since
   they're now genuinely compiled for 5.9, we updated that label to 5.9.0 in all five plugins.
10. **Second launch, crashed.** The editor loaded fully (72 s). Streamline detected the RTX 2060 on driver 617.42, correctly
    **disabled Frame Generation as unsupported on this GPU**, and loaded Reflex. Then the editor crashed on its rendering thread the
    first time it drew the screen ("EndDrawingViewport", an access violation), which is the screen-present step that Streamline
    hooks. DLSS Super Resolution doesn't hook it, so Streamline was the suspect.
11. **Isolating it:** relaunched with **DLSS only** (Frame Generation and Reflex off, so Streamline never loads). **The editor came up
    cleanly in 29 s.** NVIDIA's driver layer initialised (it found the "Unreal Engine 5" driver profile) and loaded the bundled DLSS library.
12. **Asking the plugin directly** (a Python probe sent through the editor's MCP tools):
    `supported=True`, modes **Off, Auto, DLAA, Quality, Balanced, Performance, Ultra Performance**; Ray Reconstruction supported too;
    minimum driver 470.
13. **The decision:** ship DLSS (it's what the NVIDIA award asks for); drop Frame Generation and Reflex. The 2060 can't run FG anyway,
    so it would ship untested, and a crash on a judge's RTX 40-series would be far worse than a missing toggle. The three Streamline
    plugins were moved out of the engine (parked in `E:\DLSSHost\Parked`) so no crew session can enable them by accident. Setup now
    turns DLSS on in the jam project automatically when it's installed.

**Total time:** about 75 minutes, from download to a verified DLSS on 5.9, six compiles and three editor launches included.

## Takeaways worth a line in the post
- Almost all of NVIDIA's code was source-compatible with 5.9. The only real break was 5.9's stricter compile-time log-format checking.
- Read the engine's build rules before hand-patching third-party code: there was a supported switch.
- Windows' path-length limit still bites build tools in 2026.
- **The plugin's prebuilt 5.8 files and version label were the only "hard" incompatibilities.** Everything about DLSS itself worked
  once rebuilt. The real wall was Streamline's frame-presentation hook against 5.9's renderer.
- **Isolate before you debug:** turning features off one at a time found the culprit in one extra launch.
- **The human's RTX 2060 runs DLSS Super Resolution, DLAA and Ray Reconstruction, but not Frame Generation** (RTX 40 or 50 series only).

## Changes made to NVIDIA's plugin (for the declaration and credits)
- `bValidateFormatStrings = false;` added to each module's `.Build.cs` (20 modules).
- 4 format strings changed from `%d` to `%lld`, and 8 enum arguments given explicit integer casts (DLSS and StreamlineCore sources).
- `EngineVersion` set to "5.9.0" in the five `.uplugin` files.
- Licence: NVIDIA RTX SDK EULA (in the download's Documentation folder). Credit NVIDIA DLSS in CREDITS.md and in "Tools used".
