class FileRead:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    ## Read file and construct data string
    def read(self):
        file = open(self.file_path, 'r')

        with file as f:
            lines = f.readlines()
            for line in lines:
                for c in line:
                    if c != '\n':
                        self.data.append(c)

        file.close()