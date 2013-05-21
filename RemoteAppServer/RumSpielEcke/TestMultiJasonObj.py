__author__ = 'MrLapTop'
import json



stringi = '{"r":{"y":1,"x":0},"e":0,"m":{"b":0,"a":0}};' \
          '{"r":{"y":0,"x":0},"e":0,"m":{"b":1,"a":0}};' \
          '{"r":{"y":1,"x":0},"e":0,"m":{"b":0,"a":0}};' \
          '{"r":{"y":0,"x":0},"e":0,"m":{"b":1,"a":0}};' \
          '{"r":{"y":1,"x":0},"e":0,"m":{"b":0,"a":0}};'



if __name__ == "__main__":
    stringList = stringi.split(";")[:-1]

    for string in stringList:
        jLoadOut = json.loads(string)
        print jLoadOut