import json, os

def setup(filename, config_params, help=[]):
    """
        Function to setup config file and save to specified
            filename and include user input params from list
            config_params
            
        INPUTS
        :filename: - String to save config file to
        :config_params: - List of strings for JSON configuration file.
                            User will be asked to input content for
                            each config params
        :help: - List that must be same length of config_params. This
                    is a list of strings where each string is extra
                    information to be output to user when asking
                    for config inputs.
    """
    output_help = False
    if len(config_params) == len(help):
        output_help = True
        
    config = {}
    
    for i, p in enumerate(config_params):
        out_str = p
        
        if output_help:
            out_str += '\nNOTE: %s' % help[i] if len(help[i]) else ''
            
        ui = input('Enter input for %s\n:' % out_str)
        config[p] = ui
        
    save_config(filename, config)
        
def save_config(filename, config_dict):
    # Function to save dictionary of config data
    
    _f = open(filename, 'w')
    json.dump(config_dict, _f)
    _f.close()
    
    print('Config file saved!')
    
def load_config(filename, test=0):
    # Function for loading previously created config file
    
    if not os.path.exists(filename):
        raise FileNotFoundError('%s FILE NOT FOUND. MUST RUN config.py TO SETUP THIS FILE' % filename)
    _f = open(filename, 'r')
    out = json.loads(_f.read())
    
    if test:
        print('\n\nLoading config file tested and successful...\nContents: %s' % out)
        
    return out
