#! /usr/bin/env python
import subprocess, shlex

def get_commands():
    command_dict = {
        "JECNtuple_MiniAOD"                    : "ofilename=JECNtuple_MiniAOD.root maxEvents=100000",
        "JECNtuple_MiniAOD_JESUncertaintyUp"   : "ofilename=JECNtuple_MiniAOD_JESUncertaintyUp.root JESUncertainty=up maxEvents=100000",
        "JECNtuple_MiniAOD_JESUncertaintyDown" : "ofilename=JECNtuple_MiniAOD_JESUncertaintyDown.root JESUncertainty=down maxEvents=100000",
        "JECNtuple_MiniAOD_JER"                : "ofilename=JECNtuple_MiniAOD_JER.root JERUncertainty=nominal maxEvents=100000",
        "JECNtuple_MiniAOD_JERUncertaintyUp"   : "ofilename=JECNtuple_MiniAOD_JERUncertaintyUp.root JERUncertainty=up maxEvents=100000",
        "JECNtuple_MiniAOD_JERUncertaintyDown" : "ofilename=JECNtuple_MiniAOD_JERUncertaintyDown.root JERUncertainty=down maxEvents=100000",
    }
    return command_dict

def main(debug = False):
    print "Starting to run a series of cmsRun commands ... "

    command_dict = get_commands()
    child_filenames = []
    procs = []
    for name, cmd in command_dict.iteritems():
        if cmd.find("ofilename=") or cmd.startswith("ofilename="):
            child_filenames.append(cmd.split("ofilename=")[1].split()[0])
        else:
            child_filenames.append("JECNtuple.root")

        command = "nohup cmsRun jmehats_JEC.py print " + cmd
        if debug:
            print "The current command is",command
        out=open(name+".log","w")
        procs.append(subprocess.Popen(shlex.split(command), shell=False, stdout=out, stderr=subprocess.STDOUT))

    return_code_sum = 0
    for iproc in procs:
        return_code_sum+=iproc.wait()
    out.close()

    if return_code_sum==0:
        print "All ntuples created successfully!"
        print "The ntuples created are named:"
        for n in child_filenames:
            print "\t"+n
    else:
        print "One or more of the ntuples were not created successfully :("
        exit(-1)

if __name__ == '__main__':
    main()