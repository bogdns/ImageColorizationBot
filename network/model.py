import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
from skimage.color import lab2rgb
from torchvision import transforms


class ColorizationNet(nn.Module):
    def __init__(self, input_size=128):
        super().__init__()
        MIDLEVEL_FEATURE_SIZE = 128

        # First half: ResNet
        resnet = models.resnet18(num_classes=365)
        # Change first conv layer to accept single-channel (grayscale) input
        resnet.conv1.weight = nn.Parameter(resnet.conv1.weight.sum(dim=1).unsqueeze(1))
        # Extract midlevel features from ResNet-gray
        self.midlevel_resnet = nn.Sequential(*list(resnet.children())[0:6])

        # Second half: Upsampling
        self.upsample = nn.Sequential(
            nn.Conv2d(MIDLEVEL_FEATURE_SIZE, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(64, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 2, kernel_size=3, stride=1, padding=1),
            nn.Upsample(scale_factor=2)
        )

    def forward(self, input):
        midlevel_features = self.midlevel_resnet(input)

        output = self.upsample(midlevel_features)
        return output


def to_rgb(grayscale_input, ab_input):
    C, H, W = grayscale_input.shape

    ab_input_resized = torch.nn.functional.interpolate(ab_input.unsqueeze(0), size=(H, W), mode='bilinear',
                                                       align_corners=False).squeeze(0)

    color_image = torch.cat((grayscale_input, ab_input_resized), 0).numpy()

    color_image = color_image.transpose((1, 2, 0))
    color_image[:, :, 0:1] = color_image[:, :, 0:1] * 100
    color_image[:, :, 1:3] = color_image[:, :, 1:3] * 255 - 128
    color_image = lab2rgb(color_image.astype(np.float64))
    return color_image


def colorize_single_image(image, model):
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    input_gray = transform(image).unsqueeze(0)

    with torch.no_grad():
        output_ab = model(input_gray)

    return to_rgb(input_gray[0].cpu(), ab_input=output_ab[0].detach().cpu())


colorizer = ColorizationNet()
model_path = '/app/network/colorization_md1.pth'
pretrained = torch.load(model_path, map_location=lambda storage, loc: storage)
colorizer.load_state_dict(pretrained)
colorizer.eval()
