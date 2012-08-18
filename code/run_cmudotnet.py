#Copyright (c) 2012, Carnegie Mellon University.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions
#are met:
#1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#3. Neither the name of the University nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.

# run_cmudotnet.py
"""Run analysis on CMU.net data from KDD'12 paper"""

import pipeline
from rescache import Cache
from preprocess import *

#Normalization of only high bound originally used when analyzing CMU.net data
class HighValNormalize(Transform):
    def __init__(self, lo, hi):
        self.hi = 5
        self.maxvpre = None
    def apply(self, v):
        self.maxvpre = max(v)
        return v/self.maxvpre*self.hi
    def unapply(self,v):
        if self.maxvpre is None:
            print "Must normalize in the forward direction before reversing!"
        return v*self.maxvpre/self.hi
    def getname(self):
        return "LinearNorm"

def get_default_pipeline(host="127.0.0.1",port="8124"):
    crawler = pipeline.OpenTSDBCrawlStage(host, port)
    resample = pipeline.ResampleStage(600)
    cypress = pipeline.CypressStage()
    spirit = pipeline.SpiritStage(ispca=False,thresh=0.01,ebounds=(0,1.1),startm=6)

    transforms["median"] = HighValNormalize(0,0.1)
    normalize = pipeline.NormalizeStage(True)
    denormalize = pipeline.NormalizeStage(False)
    pipe = pipeline.Pipeline()
    pipe.append_stage(crawler)
    pipe.append_stage(resample)
    pipe.append_stage(cypress)
    pipe.append_stage(normalize)
    pipe.append_stage(spirit)
    pipe.append_stage(denormalize)
    return pipe
    
if __name__ == "__main__":
    pipe = get_default_pipeline(host="172.19.149.159")
    input = dict()
    input["hosts"] = ["CMU-West", "LocalMachine", "NewYork", "PSU", "QatarExternal", "Qatar"]
    input["start"] = "2011/12/28-15:00:00"
    input["end"] = "2012/1/18-18:50:00"
    input["metrics"] = ["median"]
    output = pipe.run(input)
    cache = Cache("../etc/tmp/cache/cmu-dot-net")
    cache.write(output)
