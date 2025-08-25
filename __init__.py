bl_info = {
	"name": "Localize texture images",
	"blender": (2, 8, 0),
	"category": "Material",
	"author": "Renzo Gerritzen",
	"description": "Copy all used image textures into a \"material_textures\" folder in the project file root dir and relink all image textures to the localized files them.",
	"location": "View3D > Sidebar > Tool",
	"category": "3D View"
}



import bpy
import os
import shutil



def start_file_localization(context, subdir_name):
	blend_dir = os.path.dirname(bpy.data.filepath)
	if not blend_dir:
		raise Exception("Please save your .blend file first!")

	textures_dir = os.path.join(blend_dir, subdir_name)
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



class OBJECT_OT_start_localize(bpy.types.Operator):
	bl_idname = "object.start_localize"
	bl_label = "Localize texture files"
	bl_description = "Executes my custom function"

	def execute(self, context):
		subdir_name = context.scene.localization_subdir_name
		start_file_localization(context, subdir_name)
		self.report({'INFO'}, f"Copied all texture files to: ./{subdir_name}")
		return {'FINISHED'}



class VIEW3D_PT_localization_panel(bpy.types.Panel):
	bl_label = "Localization"
	bl_idname = "VIEW3D_PT_localization_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Tool"

	def draw(self, context):
		layout = self.layout
		layout.prop(context.scene, "localization_subdir_name", text="Subdir name")
		layout.operator("object.start_localize")



classes = (OBJECT_OT_start_localize, VIEW3D_PT_localization_panel)



def register():
	bpy.types.Scene.localization_subdir_name = bpy.props.StringProperty(name="Subdir name", description="The sub-directory to which the image-texture files will be copied", default="texture_images")
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.localization_subdir_name



if __name__ == "__main__":
	register()
