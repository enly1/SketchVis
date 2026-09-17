# SketchVis

**SketchVis** is an Autodesk Fusion 360 add-in that adds a one-click toolbar button to quickly toggle the global visibility of sketches (`Display Settings` > `Object Visibility` > `Sketches`).

---

## Features

- **One-Click Toggle**: Instantly show or hide all sketches in your design without navigating through the bottom display settings menu.
- **Toolbar Integration**: Adds a button to the **Solid** workspace under the **Scripts and Add-Ins** panel (promoted to the main toolbar by default).
- **Customizable**: Can be pinned to your favorite tools or assigned a custom keyboard shortcut within Fusion 360.
- **Robust & Dynamic Detection**: Dynamically locates the sketch visibility control at runtime rather than relying on brittle hardcoded list offsets.
- **Multi-Language Support (i18n)**: Includes localized keyword matching for multiple languages supported by Fusion 360.

---

## How It Works

1. **Toolbar Button**: When installed and started, SketchVis registers a command button (`SketchVis`) and places it on the toolbar in the Solid environment.
2. **Accessing Fusion's Internal Controls**: When clicked, the add-in accesses Fusion 360's built-in `VisibilityOverrideCommand` control definition.
3. **Dynamic Menu Search**:
   - Rather than assuming a fixed index (which can easily break between Fusion 360 updates when menu items are added or rearranged), SketchVis inspects the items in `listItems`.
   - It performs a two-pass check (exact match first, followed by substring match) against both item `name` and `id` properties.
4. **State Toggle**: Once the "Sketches" visibility item is located, it toggles `sub.isSelected`, immediately turning sketch visibility on or off in the viewport.

---

## Internationalisation (i18n)

Fusion 360 localizes menu item names and IDs depending on the active user interface language. To support users across different regions, SketchVis matches against known translations for "Sketches" / "Sketch", including:

- **English**: `sketches`, `sketch`
- **German**: `skizzen`, `skizze`
- **French**: `esquisses`, `esquisse`
- **Spanish**: `bocetos`, `boceto`
- **Italian**: `schizzi`, `schizzo`
- **Japanese**: `スケッチ`
- **Chinese (Simplified & Traditional)**: `草图`, `草圖`
- **Korean**: `스케치`
- **Portuguese**: `esboços`, `esboço`
- **Russian**: `эскизы`, `эскиз`
- **Polish**: `szkice`, `szkic`
- **Turkish**: `çizimler`, `çizim`
- **Czech**: `náčrty`, `náčrt`

> [!WARNING]
> **Tested Only in English**
> While the internationalisation logic and translation dictionaries are implemented, SketchVis has currently **only been tested in English**.
> If you are using Fusion 360 in another language and encounter issues, check the Text Commands / Application log for available item names and please report any missing or mismatched terms.

---

## Installation & Setup

1. **Locate Add-Ins Directory**:
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
   - **Windows**: `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns\`
2. **Copy the Add-In**:
   - Place the `SketchVis` folder into the `AddIns` directory.
3. **Run in Fusion 360**:
   - In Fusion 360, navigate to the **Utilities** tab and click **Scripts and Add-Ins** (`Shift + S`).
   - Switch to the **Add-Ins** tab.
   - Select **SketchVis** and click **Run**.
   - *(Optional)* Check **Run on Startup** to automatically launch SketchVis whenever Fusion 360 starts.

---

## Icon Attribution

The toolbar icons are sourced from [Flaticon](https://www.flaticon.com/free-icon/change_125860?term=switch&page=1&position=42&origin=search&related_id=125860) created by **Gregor Cresnar**.
