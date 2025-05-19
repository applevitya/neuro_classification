# 🧠 Code for paper "Neuromorphic optoelectronic computing system based on semiconducting metal oxide nanocrystallites"

This project implements a biologically inspired spiking neural network (SNN) trained using Spike-Timing Dependent Plasticity (STDP) with a Winner-Takes-All (WTA) competition mechanism. The network learns to distinguish between left and right diagonals in simple binary input patterns.

---

## 📂 Project Structure
.
├── encoding.py        # Encodes 2D binary input into spike trains
├── neuron.py          # Spiking neuron model with STDP and WTA logic
├── learning.py        # STDP learning rule and synaptic updates
├── parameters.py      # Configuration and model parameters
├── test_stdp.py       # Main training/testing loop
---

## 🧬 Biological Inspiration

The model integrates two key neuroscience-inspired components:

- STDP (Spike-Timing Dependent Plasticity)  
  Synaptic weights are updated based on the timing of spikes between pre- and post-synaptic neurons. If a presynaptic spike precedes a postsynaptic spike, the connection is strengthened.

- Winner-Takes-All (WTA)  
  Only one output neuron is allowed to spike per stimulus, enforcing competitive learning and promoting specialization.

---

## 🖼️ Task Overview

The network is trained to classify 5×5 binary input matrices as one of two classes:

- \ Left diagonal  
- / Right diagonal

Each matrix is converted into a temporal sequence of spikes. Neurons compete to respond to patterns, and STDP reinforces the winning neuron's connections to the correct input pattern.

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- numpy
- matplotlib (optional, for plots)

Install dependencies with:
pip install numpy matplotlib
### Run the Training Script
python test_stdp.py
The script initializes the network, encodes input patterns, and runs training with real-time updates of weights and spike activity.

---

## ⚙️ Core Concepts

- Spike Encoding: Input pixels are mapped to spike times using fixed latency coding.  
- Neuron Dynamics: Leaky Integrate-and-Fire (LIF) neurons simulate membrane potential and spiking.  
- Learning Rule: STDP updates weights based on spike time differences.  
- WTA Mechanism: Suppresses all but the first spiking output neuron.

---

## 🧾 License

This project is distributed under the MIT License.  
Feel free to use, modify, and share under the terms of the license.

---

## 👤 Author

Created as a minimal and interpretable demo of STDP + WTA mechanisms for neural coding and pattern recognition.
