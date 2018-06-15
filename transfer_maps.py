import sys
import os
import xNormal

"""
  Script used to rebale maps between the same geometry but with different UVs.
  It creates list of meshes in source and destination folder. For each pair it
  finds 1 corresponding maps and rebakes it.

  It should use naming convention like:
    objectName_whatever - meshes
    objectName_mapType  - for maps
"""


GEO_EXTENSION = 'fbx'
TEX_EXTENSION = 'png'


xNormal.path = r"C:\Program Files\xNormal\3.19.3\x64\xNormal.exe"

class RebakeSet():
    def __init__(self, source_mesh, source_map, target_mesh, is_map_nrm=False):
        self.s_mesh = source_mesh
        self.t_mesh = target_mesh
        self.map         = source_map
        self.is_map_nrm  = is_map_nrm

    def __str__(self):
        return ("{} {} {} {}".format(self.s_mesh, self.map, self.t_mesh, self.is_map_nrm))


if len(sys.argv) < 4:
    print("You have to run this script with three arguments:\n"
          "\n"
          "    python source_folder_meshes source_folder_maps destination_folder    "
          "\n")
    exit()
else:
    source_meshes = []
    source_maps = []
    destination_meshes = []
    source_folder_meshes = sys.argv[1]
    source_folder_maps = sys.argv[2]
    destination_folder = sys.argv[3]
    rebake_sets = []

    source_folder_meshes_exists = False
    source_folder_maps_exists   = False
    destination_folder_exists   = False

    print(" >> The following data was collected...")

    """
    First just gather all meshes and maps with proper extension.
    """

    # this is recursive
    for (dirpath, dirnames, filenames) in os.walk('.'):
        #print("Where: {}, directories: {}, files: {}".format(dirpath, dirnames, filenames))
        if dirpath[2:] == destination_folder:
            print(" >> Got the destination folder: {}".format(dirpath))
            destination_meshes = [x for x in filenames if GEO_EXTENSION in x]
            print("      meshes: {}".format(destination_meshes))
            destination_folder_exists = True
        if dirpath[2:] == source_folder_meshes:
            print(" >> Got the meshes source folder: {}".format(dirpath))
            source_meshes = [x for x in filenames if GEO_EXTENSION in x]
            print("      meshes: {}".format(source_meshes))
            source_folder_meshes_exists = True
        if dirpath[2:] == source_folder_maps:
            print(" >> Got the maps source folder: {}".format(dirpath))
            source_maps = [x for x in filenames if TEX_EXTENSION in x]
            print("      maps  : {}".format(source_maps))
            source_folder_maps_exists = True

    """
    Report if a folder doesn't exist.
    """

    if source_folder_meshes_exists == False:
        print(" >> Source folder with meshes doesn't exist...")
        exit()
    if source_folder_maps_exists == False:
        print(" >> Source folder with maps doesn't exist...")
        exit()
    if destination_folder_exists == False:
        print(" >> Destination folder doesn't exist...")
        exit()

    """
    Then build the sets for rebaking.
    """

    for single_map in source_maps:
        object_name = single_map.split('_')[0]
        s_mesh = next((m for m in source_meshes if (object_name in m)), None)
        t_mesh = next((m for m in destination_meshes if (object_name in m)), None)
        if ('nrm' in single_map) or ('normal' in single_map):
            rebake_sets.append(RebakeSet(s_mesh, single_map, t_mesh, True))
        else:
            rebake_sets.append(RebakeSet(s_mesh, single_map, t_mesh))

    print("Rebake sets:")
    for s in rebake_sets:
        print("  " + str(s))

    print(" >> Should we continue? (y/n)")
    if input() == 'y':
        pass
    else:
        exit()


    for rebake_set in rebake_sets:
        source_mesh_config = \
            xNormal.high_mesh_options(
                source_folder_meshes + "/" + rebake_set.s_mesh,
                base_tex_path=source_folder_maps + "/" + rebake_set.map,
                scale=1.0,
                texture_is_normalmap=rebake_set.is_map_nrm
            )
        target_mesh_config = \
            xNormal.low_mesh_options(
                destination_folder + "/" + rebake_set.t_mesh,
                scale=1.0,
                forward_ray_dist=0.8,
                backward_ray_dist=0.8,
            )
        bake_config = \
            xNormal.generation_options(
                destination_folder + "/" + rebake_set.map.split(".")[0] + ".png",
                width=2048,
                height=2048,
                edge_padding=16,
                normals_high_texture=True
            )
        """
        print('-------------------------')
        print(source_mesh_config)
        print('-------------------------')
        print(target_mesh_config)
        """
        config = xNormal.config( [source_mesh_config], [target_mesh_config], bake_config )
        xNormal.run_config(config)





    f = open("last_bake.xml", 'w')
    f.write(config)
    f.close()

    exit()





    # FROM
    high_config = xNormal.high_mesh_options("hat.obj", base_tex_path="guide_001_Hat_Normal.png", scale=1.0, texture_is_normalmap=True)

    # TO
    low_config = xNormal.low_mesh_options("hat_dst.obj", scale = 1.0)

    generation_config = xNormal.generation_options(
        "hat.png",
        width=512,
        height=512,
        edge_padding=64,
        aa=2,
        normals_high_texture=True
    )

    config = xNormal.config([high_config], [low_config], generation_config)
    xNormal.run_config(config)


    f = open("last_bake.xml", 'w')
    f.write(config)
    f.close()
