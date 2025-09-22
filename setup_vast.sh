#!/bin/bash

set -e  # Exit on any error

echo "🚀 Starting FaceFusion setup on vast.ai..."

# System updates and dependencies
echo "📦 Installing system dependencies..."
apt-get -y update && \
apt-get -y upgrade && \
apt -y install git-all && \
apt -y install curl && \
apt -y install ffmpeg && \
apt-get -y install mesa-va-drivers

# Install Miniconda
echo "🐍 Installing Miniconda..."
curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3

# Add conda to PATH and initialize
export PATH="/root/miniconda3/bin:$PATH"
echo 'export PATH="/root/miniconda3/bin:$PATH"' >> ~/.bashrc

# Initialize conda for all shells
/root/miniconda3/bin/conda init --all

# Force reload shell configuration to apply conda init changes
echo "🔄 Applying conda initialization..."
source ~/.bashrc

# Create conda environment using full path to avoid issues
echo "🏗️ Creating facefusion environment..."
/root/miniconda3/bin/conda create --name facefusion python=3.12 pip=25.0 -y

# Activate environment using source (more reliable in scripts)
echo "⚡ Activating environment and installing CUDA components..."
source /root/miniconda3/etc/profile.d/conda.sh
conda activate facefusion

# Install CUDA and cuDNN
conda install nvidia/label/cuda-12.9.1::cuda-runtime nvidia/label/cudnn-9.10.0::cudnn -y

# Install TensorRT
pip install tensorrt==10.12.0.36 --extra-index-url https://pypi.nvidia.com

# Install FFmpeg with specific versions
conda install conda-forge::ffmpeg=7.0.2 conda-forge::libvorbis=1.3.7 --yes

# Clone and install FaceFusion
echo "📥 Cloning and installing FaceFusion..."
cd /workspace
mkdir -p ddd
git clone https://github.com/dinhanhthi/facefusion-3.4.1.git
cd facefusion-3.4.1
git checkout vast
python install.py --onnxruntime cuda

echo "✅ Setup complete! FaceFusion is ready to use."
echo "🎯 To use it, run: conda activate facefusion"
echo "🔄 PLEASE RESTART YOUR TERMINAL"
echo "Then run following commands:"
echo "conda activate facefusion"
echo "cd /workspace/facefusion-3.4.1"
echo "python facefusion.py run --share-gradio"
echo "🎉 Done!"