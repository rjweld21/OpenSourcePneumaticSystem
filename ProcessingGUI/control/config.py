import json, os

def setup(filename, config_params, help=[], defaults=[]):
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
    default_counter = 0
    
    output_help = False
    if len(config_params) == len(help):
        output_help = True
        
    config = {}
    
    for i, p in enumerate(config_params):
        out_str = p
        
        if help[i] == 'default':
            config[p] = defaults[default_counter]
            default_counter += 1
            continue
            
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
    
def configSafetyCheck(config_data):
    checkFields = {'MaxDAC': 255}
    nonZeros = ['MaxDAC', 'PeriodMax']
    
    for f in list(checkFields):
        if config_data[f] > checkFields[f]:
            print('%s too large for field %s... Resetting to %s' % (
                    config_data[f], f, checkFields[f]))
            config_data[f] = checkFields[f]
            
    for f in nonZeros:
        if config_data[f] <= 0:
            print('%s too low for field %s... Resetting to 1' % (
                    config_data[f], f))
            config_data[f] = 1
            
    return config_data
    
def load_config(filename, test=0):
    # Function for loading previously created config file
    
    if not os.path.exists(filename):
        raise FileNotFoundError('%s FILE NOT FOUND. MUST RUN config.py TO SETUP THIS FILE' % filename)
    _f = open(filename, 'r')
    out = json.loads(_f.read())
    
    out = configSafetyCheck(out)
    
    if test:
        print('\n\nLoading config file tested and successful...\nContents: %s' % out)
        
    return out
