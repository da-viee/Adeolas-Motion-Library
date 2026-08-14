# Adeola's Motion Library - User Guide

This document contains everything you need to know to install the plugin and test the motions we've built so far.

---

## 1. How to Install the Plugin via ZIP

To install this custom add-on into Blender, you need to compress the code into a `.zip` file. 

**What exactly do you ZIP?**
You need to zip the *contents* of your code folder, not the parent folder itself.

1. Open your File Explorer and go to your folder: `C:\Users\Adeola\Music\connect to blender`.
2. Inside that folder, you will see `__init__.py`, the `motions` folder, and the `utils` folder.
3. Select **all of those files and folders** at the same time.
4. Right-click them and choose **Compress to ZIP file** (or Send to > Compressed (zipped) folder).
5. Name the resulting zip file something like `adeolas_motion_library.zip`.
6. Open Blender. Go to **Edit > Preferences > Add-ons**.
7. Click the **Install...** button at the top right.
8. Find and select your new `adeolas_motion_library.zip` file.
9. Check the box next to **Animation: Adeola's Motion Library** to activate the plugin.

---

## 2. How to Test Phase 1 (Single Motions)

1. Open the 3D Viewport in Blender.
2. Add an object to the scene (e.g., a Suzanne monkey head).
3. Press **`N`** on your keyboard to open the right-side panel in the viewport.
4. Click the new tab on the right side labeled **Adeola Motions**.
5. With your monkey selected, click the **Jelly Bounce** button.
6. Press **Play (Spacebar)** on your timeline. The object will instantly start bouncing procedurally based on the scene time!

---

## 3. How to Test Phase 4 (Morph Interaction)

This tests the advanced two-object system we just built.

1. Add two different objects to your scene (e.g., a **Monkey** and a **Cube**). Move them slightly apart so you can clearly see both.
2. In the Adeola Motions panel, look under the **Phase 4: Interactions** section.
3. You will see two fields: `Source (A)` and `Target (B)`. 
4. Click the eyedropper icon (or the dropdown box) next to **Source (A)** and click on the **Monkey**.
5. Click the eyedropper next to **Target (B)** and click on the **Cube**.
6. Click the **Morph A to B** button.
7. Now, select your **Monkey**. Look at the **Modifiers Properties tab** (the blue wrench icon on the far right of the screen).
8. Under the Geometry Nodes modifier, you will see a slider named **Morph Factor**. 
9. Drag that slider from `0.0` to `1.0`. You will see the Monkey's geometry instantly melt and snap to the surface of the Cube!
