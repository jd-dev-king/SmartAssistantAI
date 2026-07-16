import os


def search_files(filename, start_path=None):

    if start_path is None:

        start_path = os.path.expanduser("~")


    matches = []


    for root, directories, files in os.walk(start_path):

        for file in files:

            if filename.lower() in file.lower():

                matches.append(
                    os.path.join(root, file)
                )


    if matches:

        return "\n".join(matches[:5])


    return "No files found."