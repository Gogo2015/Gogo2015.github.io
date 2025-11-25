# Quantized Video Compression Autoencoder  
**Repository:** [ae_compressed_vision](https://github.com/Gogo2015/ae_compressed_vision)  
**Technical Report:** [AutoencoderPaper.pdf](https://github.com/Gogo2015/ae_compressed_vision/blob/main/AutoencoderPaper.pdf)

## Project Overview  
This project implements a quantized convolutional autoencoder for video compression. It reduces video frame sequences into discrete latent codes via a tunable codebook, enabling control over bitrate vs reconstruction quality (rate-distortion trade-off). 

## My Contributions  
- Developed encoder/decoder architecture: 3D CNN encoder + transposed convolution decoder.
- Implemented quantized latent space: discrete codebook sizes (K = {2, 4, 8, 16,32,…}) to adjust bitrate.
- Built data pipeline on Moving MNIST dataset, training scripts, and reconstruction visualizations.  
- Analysed rate-distortion curves and documented results in technical report.

## Results & Insights  
- Clear demonstration of the trade-off between codebook size (bitrate) and reconstruction quality.  
- Insight: Larger codebook sizes yield diminishing returns in reconstruction fidelity — informing future work in efficient latent representations.  
- Learned: The practical challenges of latent quantization, managing under-training for high K values, and integrating autoencoding in a video pipeline.

## Tech Stack  
- Python, PyTorch  
- 3D Convolutional Neural Networks  
- Latent quantization (codebooks)  
- Visualization scripts & rate–distortion graphs  

## Future Work  
- Extend to full video dataset (beyond Moving MNIST) for real-world scale.  
- Integrate IP-frame / P-frame structure for real-time/streaming applications.
- Explore transformer or hybrid architectures to further improve compression-reconstruction trade-off.

**Link:** [GitHub Repository](https://github.com/Gogo2015/ae_compressed_vision)  
