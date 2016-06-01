import json
from pprint import pprint

class SettingsLocal:


    # Define critical settings and/or override defaults specified in
    # settings.py. Copy this file to settings_local.py in the same
    # directory as settings.py and edit. Any settings defined here
    # will override those defined in settings.py

    def __init__(self,settings=None):

        data = None

        if settings is None:
            with open('settings.json') as data_file:
                data = json.load(data_file)
        else:
            data = settings

        print("DATA:")
        print(data)
        
        # Set this to point to your compiled checkout of caffe
        self.caffevis_caffe_root      = data['caffevis_caffe_root']


        # '/root/Documents/caffes/caffe-dlt'

        # Load model: caffenet-yos
        # Path to caffe deploy prototxt file. Minibatch size should be 1.
        self.caffevis_deploy_prototxt = str(data['caffevis_deploy_prototxt'])
        # caffevis_deploy_prototxt = '%DVT_ROOT%/models/caffenet-yos/caffenet-yos-deploy.prototxt'

        # Path to network weights to load.
        self.caffevis_network_weights = str(data['caffevis_network_weights'])
        # caffevis_network_weights = '%DVT_ROOT%/models/caffenet-yos/caffenet-yos-weights'

        # Other optional settings; see complete documentation for each in settings.py.
        self.caffevis_data_mean       = str(data['caffevis_data_mean'])
        # caffevis_data_mean      =  '%DVT_ROOT%/models/caffenet-yos/ilsvrc_2012_mean.npy'

        self.caffevis_labels       = str(data['caffevis_labels'])
        # caffevis_labels         ='%DVT_ROOT%/models/caffenet-yos/ilsvrc_2012_labels.txt'

        self.caffevis_label_layers    = tuple(str(data['caffevis_label_layers']).replace(" ", "").split(","))
        # caffevis_label_layers    = ('fc8', 'prob')


        self.caffevis_prob_layer     = str(data['caffevis_prob_layer'])
        # caffevis_prob_layer      = 'prob'


        self.caffevis_unit_jpg_dir  = str(data['caffevis_unit_jpg_dir'])
        # caffevis_unit_jpg_dir    = '%DVT_ROOT%/models/caffenet-yos/unit_jpg_vis'

        self.caffevis_jpgvis_layers   = str(data['caffevis_jpgvis_layers']).replace(" ", "").split(",")
        # caffevis_jpgvis_layers   = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5', 'fc6', 'fc7', 'fc8', 'prob']

        self.caffevis_jpgvis_remap    = json.loads('{"'+ str(data['caffevis_jpgvis_remap'].replace(" ","").replace(':','":"').replace(',','","'))+ '"}')
        # pprint(caffevis_jpgvis_remap)
        # caffevis_jpgvis_remap = {'pool1': 'conv1', 'pool2': 'conv2', 'pool5': 'conv5'}


        # Use GPU? Default is True.
        #caffevis_mode_gpu = True
        # Display tweaks.
        # Scale all window panes in UI by this factor
        self.global_scale = 0.9
        # Scale all fonts by this factor
        self.global_font_size = 0.8
        print("GLOBAL SCALE SET")
        print(self.global_scale)

    def caffevis_layer_pretty_name_fn(self,name):
        return name.replace('pool','p').replace('norm','n')
