import os
import numpy as np
import json

if __name__ == '__main__':

    year = "2016"
    thisdir = os.getcwd()
    if "2017" in thisdir:
        year = "2017"
    elif "2018" in thisdir:
        year = "2018"

    for pt in range(0, 4):
        for rho in range(0, 4):

            print("pt = "+str(pt)+", rho = "+str(rho))

            # Make the directory and go there
            thedir = "pt"+str(pt)+"rho"+str(rho)
            if not os.path.isdir(thedir):
                os.mkdir(thedir)
            os.chdir(thedir)
            if not os.path.isdir("plots"):
                os.mkdir("plots")

            # Link what you need
            os.system("ln -s ../../../../"+year+"-prefit/signalregion.root .")
            os.system("ln -s ../../make_cards_qcd.py .")

            # Create your json files of initial values
            if not os.path.isfile("initial_vals_ggf.json"):

                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
                thedict = {}
                thedict["initial_vals"] = initial_vals

                with open("initial_vals_ggf.json", "w") as outfile:
                    json.dump(thedict,outfile)

            if not os.path.isfile("initial_vals_vbf.json"):
                with open("initial_vals_vbf.json", "w") as outfile:
                    json.dump({"initial_vals":[[1]]},outfile)

            # Create the workspace
            os.system("python make_cards_qcd.py") 

            os.chdir("output/testModel_"+year)
            os.system("chmod +rwx build.sh && ./build.sh")

            workspace_command = "text2workspace.py testModel_"+year+"_combined.txt"
            os.system(workspace_command)

            # Go back to where you started
            os.chdir("../../../")