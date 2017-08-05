# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Informations
bl_info = { "name": "Your Palette Color",
    "description": "",
    "author": "Almisuifre (aidé par Pistiwique, Wazou, Stilobique et Iscream",
    "version": (1,0,0),
    "blender": (2,78,0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View", }

# Importer des libraries
import os
import bpy
from bl_operators.presets import AddPresetBase
from bpy.types import Panel, PropertyGroup, Menu, Operator
from bpy.props import FloatVectorProperty, PointerProperty

# Presets par défaut
def get_default_palette_presets():
    presets = {
        # Maya like pour le Blender Loundge
        'maya-like': [
            (0.3840000033378601, 0.3840000033378601, 0.3840000033378601),
            (0.23330000042915344, 0.23330000042915344, 0.23330000042915344),
            (0.11900000274181366, 0.11900000274181366, 0.11900000274181366),
            (0.07000000029802322, 0.07000000029802322, 0.07000000029802322),
            (0.19599999487400055, 0.19599999487400055, 0.19599999487400055),
            (0.10700000077486038, 0.10700000077486038, 0.10700000077486038),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ],
        
        # Gold
        'gold': [
            (0.17144113779067993, 0.06847818195819855, 0.006048833951354027),
            (0.3185468018054962, 0.13013650476932526, 0.007499032653868198),
            (0.3049873411655426, 0.16513220965862274, 0.008568125776946545),
            (0.23455063998699188, 0.17788845300674438, 0.07618538290262222),
            (0.33245155215263367, 0.2015562802553177, 0.0009105807403102517),
            (0.4793201982975006, 0.23839758336544037, 0.00334653677418828),
            (0.4910208284854889, 0.18782080709934235, 0.020288560539484024),
            (0.6038274168968201, 0.18447501957416534, 0.01599629409611225),
            (0.8148468732833862, 0.17464742064476013, 0.08228271454572678),
            (0.47353148460388184, 0.15592648088932037, 0.19120171666145325),
        ],
        
        # Red dégradé @Almisuifre
        'red-degrade': [
            (1.0, 0.004053084179759026, 0.0),
            (0.6266627311706543, 0.0032313596457242966, 0.0),
            (0.4479791224002838, 0.002778549212962389, 0.0),
            (0.3423837125301361, 0.002461397321894765, 0.0),
            (0.23301564157009125, 0.0020640576258301735, 0.0),
            (0.1679489016532898, 0.0017729197861626744, 0.0),
            (0.1106889396905899, 0.0014554420486092567, 0.0),
            (0.06997819989919662, 0.0011639943113550544, 0.0),
            (0.04445476084947586, 0.0009259051876142621, 0.0),
            (0.018848737701773643, 0.0005820458172820508, 0.0),
        ],
        
        # Copper @Almisuifre
        'copper': [
            (0.4178850054740906, 0.14702700078487396, 0.07618500292301178),
            (0.760524570941925, 0.2622506618499756, 0.11953846365213394),
            (1.0, 0.6938719749450684, 0.42326799035072327),
            (1.0, 0.5209956169128418, 0.29613834619522095),
            (0.32314300537109375, 0.03310500085353851, 0.017642000690102577),
            (0.6104956269264221, 0.13286834955215454, 0.09530746936798096),
            (0.799102783203125, 0.215860515832901, 0.16513220965862274),
            (1.0, 0.44520121812820435, 0.3662526309490204),
            (1.0, 1.0, 1.0),
            (0.0, 0.0, 0.0),
        ],
        
        # Blank @Almisuifre
        'blank': [
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ],
        
        # Primaire et secondaire @Almisuifre
        'blank': [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, 0.0),
            (0.0, 1.0, 1.0),
            (1.0, 0.0, 1.0),
            (1.0, 1.0, 1.0),
            (0.0, 0.0, 0.0),
        ],
    }
    return presets

# Fonctionqui est appeler au démarrage du script
def setup():
    # Vérifier la présence du répertoire des presets
    preset_subdir = "your_palette_colour_presets"
    preset_directory = os.path.join(bpy.utils.user_resource('SCRIPTS'), "presets", preset_subdir)
    preset_paths = bpy.utils.preset_paths(preset_subdir)
    
    # Si le répertoire n'hexiste pas, le créer
    if(preset_directory not in preset_paths):
        # Si pe chemin n'est pas préset dans le système, le créer
        if(not os.path.exists(preset_directory)):
            os.makedirs(preset_directory) # Créer le répertoire
    
    # Cherche des presets existants
    def walk(p):
        r = {'files': [], 'dirs': [], }
        for(root, dirs, files) in os.walk(p):
            r['files'].extend(files)
            r['dirs'].extend(dirs)
            break
        return r
    
    found = []
    for p in preset_paths:
        c = walk(p)
        for f in c['files']:
            if(f.endswith(".py")):
                found.append(f[:-10])
    
    # Si le répertoire est vide
    if(len(found) == 0):
        # Crée des fichiers présets par défaut
        default_presets = get_default_palette_presets()
        
        """ !!! Mise en garde :
                le code qui suit met en forme le contenu des fichiers créés.
                Modifier cette section avec parcimonie.
            !!! """
            
        e = "\n"
        for n, p in default_presets.items():
            s = ""
            s += "import bpy" + e
            
            for i in range(10):
                s += "C"+format(i)+" = bpy.context.window_manager.myPropertyGroup"+e
            s += e
            for i in range(10):
                d = i + 1   # Petit décallage du à la façont d'ont c'est codé
                s += "C"+format(i)+".create_color"+format(d)+" = "
                s += "("+format(p[i][0])+", "+format(p[i][1])+", "+format(p[i][2])+") "+e
                
            # Ecrire le fichier 
            with open(os.path.join(preset_directory, "{}.py".format(n)), mode = 'w',
            encoding = 'utf-8') as f: # Forçage à UTF-8
                f.write(s)
          
    # Debug
    #print(i)
    #print(s) #Debug
    #print(preset_directory) # Path
    #print("Finish !")

# Classe d'édition de la couleur
class ColorEditGroup(PropertyGroup):
    # Edition de la couleur 1 de base
    create_color1 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 1', )
    
    # Edition de la couleur 2 de base
    create_color2 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 2', )
    
    # Edition de la couleur 3 de base
    create_color3 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 3', )
    
    # Edition de la couleur 4 de base
    create_color4 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 4', )
    
    # Edition de la couleur 5 de base
    create_color5 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 5', )
    
    # Edition de la couleur 6 de base
    create_color6 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 6', )
    
    # Edition de la couleur 7 de base
    create_color7 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 7', )
    
    # Edition de la couleur 8 de base
    create_color8 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 8', )
        
    # Edition de la couleur 9 de base
    create_color9 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 9', )
        
    # Edition de la couleur 10 de base
    create_color10 = FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = 'Your create color 10', )

# Classe qui fera apparaître le menu flotant de sélection du nom de preset
class VIEW3D_OT_colours_preset_add(AddPresetBase, bpy.types.Operator):
    bl_idname = 'scene.colours_preset_add'
    bl_label = 'Add colours palette preset'
    bl_options = {'REGISTER', 'UNDO'}
    preset_menu = 'VIEW3D_MT_your_palette_presets'
    preset_subdir = 'your_palette_colour_presets'
    
    preset_defines = [
        "C0 = bpy.context.window_manager.myPropertyGroup",
        "C1 = bpy.context.window_manager.myPropertyGroup",
        "C2 = bpy.context.window_manager.myPropertyGroup",
        "C3 = bpy.context.window_manager.myPropertyGroup",
        "C4 = bpy.context.window_manager.myPropertyGroup",
        "C5 = bpy.context.window_manager.myPropertyGroup",
        "C6 = bpy.context.window_manager.myPropertyGroup",
        "C7 = bpy.context.window_manager.myPropertyGroup",
        "C8 = bpy.context.window_manager.myPropertyGroup",
        "C9 = bpy.context.window_manager.myPropertyGroup",
    ]
    
    preset_values = [
        "C0.create_color1",
        "C1.create_color2",
        "C2.create_color3",
        "C3.create_color4",
        "C4.create_color5",
        "C5.create_color6",
        "C6.create_color7",
        "C7.create_color8",
        "C8.create_color9",
        "C9.create_color10",
    ]

# Classe qui fait apparaître le menu de sélection des presets
class VIEW3D_MT_your_palette_presets(bpy.types.Menu):
    bl_label = "Your palette presets"
    bl_idname = "VIEW3D_MT_your_palette_presets"
    preset_subdir = "your_palette_colour_presets"
    preset_operator = "script.execute_preset"
    
    draw = bpy.types.Menu.draw_preset

# Classe dérivée du Panel
class SimpleToolPanel_3D_VIEW(bpy.types.Panel):
    bl_idname = 'Palette_Color_3DV'
    bl_label = 'Palette'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = 'objectmode' # !!! Laisser cocher si @classmethod est utilisé plus bas !!!
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}
    
    # Permet d'afficher la palette en mode Edit et en mode Objet
    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH'}
    
    # Contenu de la fenêtre
    def draw(self, context):
        myPG = context.window_manager.myPropertyGroup
        layout = self.layout
        
        # Le pannel
        row = layout.row()
        row.label("Your colours", icon = 'COLOR')
        
        col = layout.column(align = True)
        
        box = col.box().split(align = True)
        box.prop(myPG, 'create_color1')
        box.prop(myPG, 'create_color2')
        box.prop(myPG, 'create_color3')
        box.prop(myPG, 'create_color4')
        box.prop(myPG, 'create_color5')
        
        box = col.box().split(align = True)
        box.prop(myPG, 'create_color6')
        box.prop(myPG, 'create_color7')
        box.prop(myPG, 'create_color8')
        box.prop(myPG, 'create_color9')
        box.prop(myPG, 'create_color10')
        
        row = layout.row()
        row.label("Options", icon = 'RNA_ADD')
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.menu("VIEW3D_MT_your_palette_presets", text = bpy.types.VIEW3D_MT_your_palette_presets.bl_label)
        row.operator("scene.colours_preset_add", text = "", icon = 'ZOOMIN')
        row.operator("scene.colours_preset_add", text = "", icon = 'ZOOMOUT').remove_active = True

# Classe dérivée du Panel
class SimpleToolPanel_NODE_EDITOR(bpy.types.Panel):
    bl_idname = 'Palette_Color_NE'
    bl_label = 'Palette'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}
    
    # Contenu de la fenêtre
    def draw(self, context):
        myPG = context.window_manager.myPropertyGroup
        layout = self.layout
        
        # Le pannel
        row = layout.row()
        row.label("Your colours", icon = 'COLOR')
        
        col = layout.column(align = True)
        
        box = col.box().split(align = True)
        box.prop(myPG, 'create_color1')
        box.prop(myPG, 'create_color2')
        box.prop(myPG, 'create_color3')
        box.prop(myPG, 'create_color4')
        box.prop(myPG, 'create_color5')
        
        box = col.box().split(align = True)
        box.prop(myPG, 'create_color6')
        box.prop(myPG, 'create_color7')
        box.prop(myPG, 'create_color8')
        box.prop(myPG, 'create_color9')
        box.prop(myPG, 'create_color10')
        
        row = layout.row()
        row.label("Options", icon = 'RNA_ADD')
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.menu("VIEW3D_MT_your_palette_presets", text = bpy.types.VIEW3D_MT_your_palette_presets.bl_label)
        row.operator("scene.colours_preset_add", text = "", icon = 'ZOOMIN')
        row.operator("scene.colours_preset_add", text = "", icon = 'ZOOMOUT').remove_active = True

"""
# Gère cls
class ColoursPresetsProperties(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.colours_preset_properties = bpy.props.PointerProperty(type = cls)
        cls.edit = bpy.props.BoolProperty(name = "Edit", description = "", default = False, )
    
    @classmethod
    def unregistrer(cls):
        del bpy.types.Scene.colours_preset_properties
"""

# Enregistrement
def register():
    setup()
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.myPropertyGroup = bpy.props.PointerProperty(type = ColorEditGroup)


# Désenregistrement
def unregister():
    del bpy.types.WindowManager.myPropertyGroup
    bpy.utils.unregister_module(__name__)
    
# Permet le fonctionnement du module
if __name__ == "__main__":
    register()