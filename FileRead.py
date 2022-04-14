class FileRead:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    ## Read file and construct data string
    def read(self):
        file = open(self.file_path, 'r')

        for line in file: 
            for c in line:
                if c.isalpha():
                    self.data.append(c)

        file.close()