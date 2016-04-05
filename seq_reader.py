class sequence():

    def __init__(self):
        self.loops = {}
        self.dataTxt = open("Emerging_Paradigm.txt")
        self.sequence = {}
        self.getSequence(self.dataTxt)
        self.length = len(self.sequence)


    def getStep(self, stepNumber):
        self.dataTxt.seek(self.sequence[stepNumber])
        return self.dataTxt.readline()

    def getSequence(self, sequenceFile):

        def strIsInt(string):
            try:
              int(string)
              return True
            except:
              return False

        sequence = {}
        seqStep = 1
        lastLine = 0
        loop_index = -1
        # Index the seqence so that a line can be recalled very fast
        for line in sequenceFile:
            if strIsInt(line[0]) or line[:3] == "seq" or line[:4] == "loop": # If first charachter is an int it means it is a step
                #print(line)
                self.sequence[seqStep] = lastLine
                lastLine = self.dataTxt.tell()
                seqStep += 1
            else: # caputre line before first line
                lastLine = self.dataTxt.tell()
