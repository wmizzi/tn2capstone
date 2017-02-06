import subprocess
import platform

class pingClient:
    # To initiate a ping test you must include a list of sites to test with the format : sitelist=["www.youtube.com","130.56.253.198","www.theage.com.au"]
    # Additionally you may enter a parameter for the number of test you want to conduct, this will default to 4 per site
    def __init__(self,sitelist):
        self.sitelist = sitelist
        self.n = len(sitelist)
        self.pingAvgTime = [-1] * self.n
        self.pingMinTime = [-1] * self.n
        self.pingMaxTime = [-1] * self.n    
    def getResults(self):
        return self.pingTime
    # Additionally you may enter a parameter for the number of test you want to conduct, this will default to 4 per site
    def runTest(self,trials = 4):
    
        ping_str = "-n " + str(trials) if  platform.system().lower()=="windows" else "-c " + str(trials)
        
        for url in self.sitelist:
            resp = subprocess.Popen("ping " + ping_str + " " + url, stdout=subprocess.PIPE).stdout.read()
            resp = resp.split('\n')
            n = len(resp)
            
            
        
        