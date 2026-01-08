from chardet.universaldetector import UniversalDetector
detector = UniversalDetector()
file = 'N_Data.xlsb'
with open(file, 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result)