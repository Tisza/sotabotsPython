class gyroFilter():

        def __init__(self, numSamples):
                self.numSamples = numSamples
                self.samples = list(range(0,numSamples))
                self.index = 0            

        def update(self, updateValue):
                self.samples[self.index] = updateValue
                self.index += 1
                
                if self.index >= self.numSamples:
                        self.index = 0

                return round(sum(self.samples)/(float(len(self.samples))))
 
                 
