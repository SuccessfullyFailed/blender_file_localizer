# BlenderFileLocalizer

**BlenderFileLocalizer** is a lightweight Blender extension that helps you collect and organize all image textures used in your project. With a single button, it copies all external images into a local folder (relative to your `.blend` file) and automatically relinks them.

This makes it easy to:
- Keep your project self-contained.
- Ensure all textures are backed up along with your `.blend` file.
- Share or version-control projects (e.g. with GitHub) without missing textures.

---

## Features
- **Custom folder name**: Choose the name of the target folder via a text field.
- **One-click localize**: Copies all image textures to the folder, keeping the original images intact.
- **Auto-relink**: Updates texture paths in the project to the new local copies.
- **Non-destructive**: Original files remain untouched.

---

## Usage
1. Install the add-on in Blender (`Edit > Preferences > Add-ons > Install` and select the ZIP file).
2. Enable **BlenderFileLocalizer**.
3. In the **3D View > Tools panel**, you’ll see:
   - A text field to set your target folder name.
   - A button to localize your textures.
4. Click the button → all textures are copied into the folder next to your `.blend` file, and Blender updates to use them.

---

## Example
If your project file is:
```
/my_project/scene.blend
```
and you set the folder name to `textures_local`, after running the tool you’ll have:
```
/my_project/scene.blend
/my_project/textures_local/   <-- all image textures copied here
```

---

## Why use it?
Blender’s “Pack Resources” feature embeds everything into the `.blend` file, which can make version control messy.
**BlenderFileLocalizer** offers a clean, transparent, and Git-friendly alternative by keeping textures external but still neatly organized.

---

## License
MIT License.