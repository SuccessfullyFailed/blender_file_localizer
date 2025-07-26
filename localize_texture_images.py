bl_info = {
	"name": "Localize texture images",
	"blender": (4, 4, 0),
	"category": "Material",
	"author": "Renzo Gerritzen",
	"description": "Copy all used image textures into a "material_textures" folder in the project file root dir and relink all image textures to the localized files them.",
}

import bpy
import os
import shutil


def localize_image_textures():
	blend_dir = os.path.dirname(bpy.data.filepath)
	if not blend_dir:
		raise Exception("Please save your .blend file first!")

	textures_dir = os.path.join(blend_dir, "material_textures")
	os.makedirs(textures_dir, exist_ok=True)

	copied_images = {}
	for image in bpy.data.images:
		if not image.filepath or image.packed_file:
			continue

		image_path = bpy.path.abspath(image.filepath)
		image_name = os.path.basename(image_path)
		new_path = os.path.join(textures_dir, image_name)
		if not os.path.isfile(image_path) and not os.path.isfile(new_path):
			print(f"Skipping missing image: {image_path}")
			continue
		
		if image_path not in copied_images:
			if not os.path.exists(new_path):
				shutil.copy2(image_path, new_path)
				print(f"Copied: {image_path} -> {new_path}")
			copied_images[image_path] = new_path

		image.filepath = bpy.path.relpath(new_path)
		image.reload()
		print(f"Relinked image: {image.name} -> {image.filepath}")

	return "All images copied and relinked."


class TEXTURE_OT_CopyAndRelink(bpy.types.Operator):
	bl_idname = "texture.localize_image_textures"
	bl_label = "Localize image textures"
	bl_description = "Copy all used image textures into a "material_textures" folder in the project file root dir and relink all image textures to the localized files them."
	bl_options = { 'REGISTER', 'UNDO' }

	def execute(self, context):
		try:
			result = localize_image_textures()
			self.report({ 'INFO' }, result)
		except Exception as e:
			self.report({ 'ERROR' }, str(e))
			return { 'CANCELLED' }
		return {'FINISHED'}


class TEXTURE_LOCALIZER_CopyPanel	(bpy.types.Panel):
	bl_label = "Relink texture images"
	bl_idname = "TEXTURE_PT_copy_panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Textures'

	def draw(self, context):
		layout = self.layout
		layout.operator("texture.localize_image_textures", icon="FILE_FOLDER")


classes = (TEXTURE_OT_LocalizeImageTexture, TEXTURE_LOCALIZER_CopyPanel	)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()