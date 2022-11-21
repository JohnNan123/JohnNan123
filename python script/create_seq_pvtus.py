import glob
import os
import sys

"""
Pass in the wild card version of your directory of .vtu files to convert
each directory to a set of .pvtu files representing discrete time points.
"""


def main():
    foldertype = ""
    if len(sys.argv) > 1:
        foldertype = sys.argv[1]
        print(foldertype)

    folders = glob.glob(foldertype)
    print(f"The folders: {folders}")

    for folder in folders:
        writepvtu(folder)


def writepvtu(folder):
    """
    folder: path to folder

    Prints out the .pvtu for all of the .vtus in the folder. Names the .pvtu
    to be the same as the folder.
    """
    with os.scandir(folder) as foldercontents:
        pvtuname = os.path.basename(os.path.normpath(folder)) + ".pvtu"
        print(f"Creating pvtu name: {pvtuname}")
        with open(pvtuname, "w") as pvtu_handler:
            pvtu_handler.write(
                '<VTKFile type="PUnstructuredGrid" byte_order="BigEndian">'
            )
            pvtu_handler.write("<PUnstructuredGrid>\n")
            pvtu_handler.write("<PPointData>\n")
            pvtu_handler.write("</PPointData>\n")
            pvtu_handler.write('<PCellData Scalars="Pressure" Vectors="Velocity">\n')
            pvtu_handler.write('<PDataArray Name="Pressure" type="Float32"/>\n')
            pvtu_handler.write('<PDataArray Name="WSS" type="Float32"/>\n')
            pvtu_handler.write('<PDataArray Name="ID" type="Int32"/>\n')
            pvtu_handler.write(
                '<PDataArray Name="Velocity" type="Float32" NumberOfComponents="3"/>\n'
            )
            pvtu_handler.write("</PCellData>\n")
            pvtu_handler.write("<PPoints>\n")
            pvtu_handler.write(
                '<PDataArray Name="Coordinates" type="Float32" NumberOfComponents="3"/>\n'
            )
            pvtu_handler.write("</PPoints>\n")
            pvtu_handler.write("<PCells>\n")
            pvtu_handler.write('<PDataArray Name="connectivity" type="Int32"/>\n')
            pvtu_handler.write('<PDataArray Name="offsets" type="Int32"/>\n')
            pvtu_handler.write('<PDataArray Name="types" type="Int32"/>\n')
            pvtu_handler.write("</PCells>\n")
            for dirfile in foldercontents:
                if dirfile.name.endswith(".vtu"):
                    pvtu_handler.write(
                        f'<Piece Source="{os.path.join(folder, dirfile.name)}"/>\n'
                    )
            pvtu_handler.write("</PUnstructuredGrid>\n")
            pvtu_handler.write("</VTKFile>\n")


if __name__ == "__main__":
    main()
