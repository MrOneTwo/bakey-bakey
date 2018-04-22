import sys
import os
import xNormal


xNormal.path = r"C:\Program Files\xNormal\3.19.3\x64\xNormal.exe"

if len(sys.argv) < 3:
    print("You have to run this script with two arguments:\n"
          "\n"
          "    python source_folder_meshes destination_folder    "
          "\n")
    exit()
else:
    source_meshes = []
    source_maps = []
    destination_meshes = []
    destination_maps = []
    source_folder_meshes = sys.argv[1]
    destination_folder = sys.argv[2]
    base_texture_is_normalmap = False


    source_folder_meshes_exists = False
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
            source_meshes = [x for x in filenames if 'obj' in x.lower()]
            print("      meshes: {}".format(source_meshes))
            source_folder_meshes_exists = True

    print(" >> Should we continue? (y/n)")
    if input() == 'y':
        pass
    else:
        exit()

    if source_folder_meshes_exists == False:
        print(" >> Source folder with meshes doesn't exist...")
        exit()
    if destination_folder_exists == False:
        print(" >> Destination folder doesn't exist...")
        exit()

    source_configs = []
    destination_configs = []


    for mesh in source_meshes:
        source_configs.append(
            xNormal.high_mesh_options(
                source_folder_meshes + "/" + mesh,
                scale=1.0,
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
        "baked_maps/out.png",
        width=1024,
        height=1024,
        edge_padding=64,
        gen_normals=True,
        gen_ao=True,
    )

    config = xNormal.config(source_configs, destination_configs, generation_config)
    xNormal.run_config(config)


    f = open("last_bake.xml", 'w')
    f.write(config)
    f.close()

    exit()
