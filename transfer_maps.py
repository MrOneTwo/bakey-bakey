import sys
import os
import xNormal


xNormal.path = r"C:\Program Files\xNormal\3.19.3\x64\xNormal.exe"

if len(sys.argv) < 4:
    print("You have to run this script with two arguments:\n"
          "\n"
          "    python source_folder_meshes source_folder_maps destination_folder    "
          "\n")
    exit()
else:
    source_meshes = []
    source_maps = []
    destination_meshes = []
    destination_maps = []
    source_folder_meshes = sys.argv[1]
    source_folder_maps = sys.argv[2]
    destination_folder = sys.argv[3]
    base_texture_is_normalmap = False

    print(" >> Is the base texture a TS normal map? (y/n)")
    if input() == 'y':
        base_texture_is_normalmap = True


    source_folder_meshes_exists = False
    source_folder_maps_exists = False
    destination_folder_exists = False

    print(" >> The following data was collected...")

    # this is recursive
    for (dirpath, dirnames, filenames) in os.walk('.'):
        #print("Where: {}, directories: {}, files: {}".format(dirpath, dirnames, filenames))
        if dirpath[2:] == destination_folder:
            print(" >> Got the destination folder: {}".format(dirpath))
            destination_meshes = [x for x in filenames if 'obj' in x]
            print("      meshes: {}".format(destination_meshes))
            destination_folder_exists = True
        if dirpath[2:] == source_folder_meshes:
            print(" >> Got the meshes source folder: {}".format(dirpath))
            source_meshes = [x for x in filenames if 'obj' in x]
            print("      meshes: {}".format(source_meshes))
            source_folder_meshes_exists = True
        if dirpath[2:] == source_folder_maps:
            print(" >> Got the maps source folder: {}".format(dirpath))
            source_maps = [x for x in filenames if 'png' in x]
            print("      maps  : {}".format(source_maps))
            source_folder_maps_exists = True

    print(" >> Should we continue? (y/n)")
    if input() == 'y':
        pass
    else:
        exit()

    if source_folder_meshes_exists == False:
        print(" >> Source folder with meshes doesn't exist...")
        exit()
    if source_folder_maps_exists == False:
        print(" >> Source folder with maps doesn't exist...")
        exit()
    if destination_folder_exists == False:
        print(" >> Destination folder doesn't exist...")
        exit()

    source_configs = []
    destination_configs = []

    for mesh in source_meshes:
        mesh_name = mesh.split('.')[0]
        for m in source_maps:
            if mesh_name in m:
                corresponding_map = m
        source_configs.append(
            xNormal.high_mesh_options(
                source_folder_meshes + "/" + mesh,
                base_tex_path=source_folder_maps + "/" + corresponding_map,
                scale=1.0,
                texture_is_normalmap=base_texture_is_normalmap
            )
        )
    for mesh in destination_meshes:
        destination_configs.append(
            xNormal.low_mesh_options(
                destination_folder + "/" + mesh,
                scale=1.0,
                forward_ray_dist=0.1,
                backward_ray_dist=0.1,
            )
        )
        
    """
    print('-------------------------')
    print(source_configs)
    print('-------------------------')
    print(destination_configs)
    """

    generation_config = xNormal.generation_options(
        "out.png",
        width=2048,
        height=2048,
        edge_padding=16,
        normals_high_texture=True
    )

    config = xNormal.config(source_configs, destination_configs, generation_config)
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
