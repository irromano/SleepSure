import pywt
import pandas
class DWT:
  
    def __init__(self):
        print("Running Discrete Wavelet Transform")
    #runs the DWT on specific waveset
    def getCoeffecients(self, setName):
        coefSet=[[]]
        for signals in setName:
            coeffs=pywt.wavedec(signals, 'db2', level=2)
            coefSet.append(coeffs)
            
        coefSet.pop(0)
        return coefSet
    def getCoeffecientsBand(self, signals):
        coeffs=pywt.wavedec(signals, 'db2', level=2)
        return coeffs
