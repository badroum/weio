# configuration file
import json
import sys

def getConfiguration(path):
    inputFile = open(path, 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)

def saveConfiguration(path, conf):
    inputFile = open(path, 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()

config = getConfiguration(sys.argv[1])
config['port'] = 80
config['debug_mode'] = "False"
config['extern_projects_path_flash'] = "/weioUser/flash"
config['absolut_root_path']= "/weio"
saveConfiguration(sys.argv[1], config)
