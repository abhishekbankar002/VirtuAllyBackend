import os

from .base_options import BaseOptions

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'myNewApp\\PFAFNModel\\')

class TestOptions(BaseOptions):
    def initialize(self):
        BaseOptions.initialize(self)

        self.parser.add_argument('--warp_checkpoint', type=str, default=os.path.join(UPLOAD_FOLDER,'checkpoints/PFAFN/warp_model_final.pth'), help='load the pretrained model from the specified location')
        self.parser.add_argument('--gen_checkpoint', type=str, default=os.path.join(UPLOAD_FOLDER,'checkpoints/PFAFN/gen_model_final.pth'), help='load the pretrained model from the specified location')
        self.parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc')
        self.parser.add_argument('runserver')
        # self.parser.add_argument('runserver')
        # self.parser.add_argument('--name', default='demo')
        # self.parser.add_argument('--resize_or_crop', default=None)
        # self.parser.add_argument('--batchSize', default=1)
        # self.parser.add_argument('--gpu_ids', default=0)
        # self.parser.add_argument('--nThread', default=0)

        self.isTrain = False
