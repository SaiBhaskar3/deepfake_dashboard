import kagglehub

# Download latest version
path = kagglehub.model_download("riceleaf12/xceptionnet/keras/default")

print("Path to model files:", path)