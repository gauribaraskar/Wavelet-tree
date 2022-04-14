class FileRead:

    """ Constructor for FASTA file, it takes file path as only argument """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.sequence_name = ''

    """ Method used to actually read and parse file """
    def read(self):
        file = open(self.file_path, 'r')

        for line in file: 
            for c in line:
                if c.isalpha():
                    self.data.append(c)

        file.close()