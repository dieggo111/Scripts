sys.path.append("C:\\Users\\Marius\\KITPlot\\")
from KITPlot import KITData

class selectData(object):

    def __init__(self):

        self.__dataList = []
        self.__searchList = []
        self.__paraList = ["Voltage","Annealing"]
        self.__default_gain = 210
        self.__annealing_norm = 1

    def collect_alibava_id(self,runNr,searchItem,*args):
        """
        runNr: str, must look like "startNr-endNr"
        searchItem: str, must look like "Para=Value"

        """
        # validate input (must be "ID-ID") and determine search parameter
        try:
            (startNr,endNr) = runNr.split("-")
            (para,val) = searchItem.split("=")
            if para not in self.__paraList or val.isdigit() is False:
                raise ValueError("Unkown parameter")
            else:
                pass
        except:
            raise ValueError("Unkown input")

        if int(startNr) > int(endNr):
            # TODO: intercept error + status message in gui
            # raise ValueError("Unexpected input. StartNr must be smaller"
            #                  " than endNr!")
            print("Unexpected input. StartNr must be smaller"
                             " than endNr!")
        else:
            pass

        # fill self.__dataList with kitdata files
        self.fill_dataList(startNr,endNr)

        if self.__dataList == []:
            raise ValueError("Can't find complete runs in between {0} and {1}".format(startNr,endNr))
        else:
            pass

        print("Search completed...")

        # check if default name was set by user
        try:
            gain = [x for x in args if "gain" in x.lower()][0]
            gain = int(gain.split("=")[1])
        except:
            gain = None

        # check if sensor name was given by user
        try:
            name = [x for x in args if "name" in x.lower()][0]
            name = name.split("=")[1]
        except:
            name = self.__dataList[0].getName()

        # fill self.__searchList
        for kData in self.__dataList:
            if name == kData.getName() and para == "Voltage":
                if int(val) in range(int(abs(round(kData.getX()[0]))-1),\
                                     int(abs(round(kData.getX()[0]))+2)):
                    try:
                        # if it's an old Alibava measurement
                        if kData.getGain() == 1.0 and gain == None:
                            gain = self.__default_gain
                            seed = self.__default_gain*kData.getSeed()
                        else:
                            # if a default gain was given by user
                            try:
                                seed = gain*kData.getSeed()
                            # use gain from measurement calibration
                            except:
                                seed = kData.getGain()*kData.getSeed()

                        if kData.getGain() == seed/kData.getSeed():
                            self.__searchList.append({"Name" :         str(kData.getName()),
                                                      "Project":       str(kData.getProject()),
                                                      "ID" :           str(kData.getID()),
                                                      "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                      "Gain" :         str(round(kData.getGain())),
                                                      "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                      "Seed" :         str(round(seed))})
                            gain = None
                        else:
                            self.__searchList.append({"Name" :         str(kData.getName()),
                                                      "Project":       str(kData.getProject()),
                                                      "ID" :           str(kData.getID()),
                                                      "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                      "Gain" :         str(round(gain)),
                                                      "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                      "Seed" :         str(round(seed))})
                    except:
                         pass
                else:
                    pass

            elif name == kData.getName() and para == "Annealing":
                if (int(val) in range(int(round(kData.getZ()[0]/self.__annealing_norm*0.8)),\
                                      int(round(kData.getZ()[0]/self.__annealing_norm*1.1))) \
                                      or int(val) == kData.getZ()[0]):
                    try:
                        # if it's an old Alibava measurement
                        if kData.getGain() == 1.0 and gain == None:
                            gain = self.__default_gain
                            seed = self.__default_gain*kData.getSeed()
                        else:
                            # if a default gain was given by user
                            try:
                                seed = gain*kData.getSeed()
                            # use gain from measurement calibration
                            except:
                                seed = kData.getGain()*kData.getSeed()
                        if kData.getGain() == seed/kData.getSeed():
                            self.__searchList.append({"Name" :         str(kData.getName()),
                                                      "Project":       str(kData.getProject()),
                                                      "ID" :           str(kData.getID()),
                                                      "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                      "Gain" :         str(round(kData.getGain())),
                                                      "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                      "Seed" :         str(round(seed))})
                            gain = None
                        else:
                            self.__searchList.append({"Name" :         str(kData.getName()),
                                                      "Project":       str(kData.getProject()),
                                                      "ID" :           str(kData.getID()),
                                                      "Voltage" :      str(abs(round(kData.getX()[0]))),
                                                      "Gain" :         str(round(gain)),
                                                      "Annealing" :    str(round(kData.getZ()[0]/24)),
                                                      "Seed" :         str(round(seed))})
                    except:
                        pass
                else:
                    pass
            else:
                pass

        if self.__searchList == []:
            # raise ValueError("Couldn't find data that met the requirements")
            print("Couldn't find data that met the requirements")

        return True