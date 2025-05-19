# 🧠 Code for paper "Neuromorphic optoelectronic computing system based on semiconducting metal oxide nanocrystallites"

This project presents a minimal, interpretable spiking neural network (SNN) model that utilizes Spike-Timing Dependent Plasticity (STDP) combined with a Winner-Takes-All (WTA) mechanism. The goal is to demonstrate biologically inspired unsupervised learning for a simple pattern recognition task: distinguishing between left and right diagonals in a binary image.

The implementation is ideal for use in neuroscience education, research prototypes, or demonstrations of self-organizing learning mechanisms.

---

## 📂 Project Structure

```
.
├── encoding.py        # Converts binary inputs into spike trains
├── neuron.py          # Implements LIF neurons with STDP and WTA
├── learning.py        # Defines synaptic update rules and learning dynamics
├── parameters.py      # Configures simulation parameters
├── test_stdp.py       # Entry point for running training and evaluation
```

---

## 🧬 Biological Inspiration

- **STDP (Spike-Timing Dependent Plasticity)**  
  This synaptic update rule strengthens or weakens connections based on the precise timing between pre- and post-synaptic spikes. It emulates Hebbian learning and enables the network to adapt autonomously to repeated input patterns.

- **Winner-Takes-All (WTA)**  
  A competitive mechanism ensuring that only the neuron with the strongest response is allowed to spike. This forces output neurons to specialize and reduces redundancy.

Together, these components create a minimal yet powerful model of unsupervised representation learning.

---

## 🖼️ Task Overview

The model learns to classify $5 \times 5$ binary matrices containing either a left (`\`) or right (`/`) diagonal. These matrices are encoded into spike trains, and the neurons adapt their synaptic weights to specialize in detecting a specific orientation. The WTA mechanism guarantees that only one output neuron responds per stimulus.

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- `numpy`
- `matplotlib` (for visualization, optional)

### Installation

```bash
pip install numpy matplotlib
```

### Running the Model

```bash
python test_stdp.py
```

This script initializes the neural network, generates training data, encodes the input, and performs STDP-based learning with WTA competition. Progress can be logged or visualized, depending on configuration.

---

## ⚙️ Core Concepts

- **Spike Encoding**: Active pixels are assigned earlier spike times, while inactive ones do not emit spikes.
- **LIF Neurons**: Leaky integrate-and-fire model approximates biological membrane potential dynamics.
- **Plasticity**: STDP modifies synaptic strengths based on temporal correlations between spikes.
- **Inhibition**: Lateral competition ensures that only the most responsive neuron fires per input sample.

---

## 📊 Suggested Visualizations

To explore the network's behavior, consider plotting:
- **Spike rasters** for observing spiking activity across neurons
- **Membrane potential curves** to track the competition dynamics
- **Synaptic weight matrices** to visualize learning convergence and specialization

These visual tools can provide insight into the self-organizing properties of the system.

---

## 🧪 Usage Scenarios

- Interactive classroom demonstrations of STDP learning
- Benchmarking biologically plausible algorithms
- Visual neuroscience projects
- Research in neuromorphic computing and unsupervised learning

---

## 🧾 License

This project is open-sourced under the MIT License.  
You are free to use, modify, and distribute the code with proper attribution and without warranty.

---

## 👤 Author

Developed to serve as a concise and clear demonstration of unsupervised learning through STDP and competitive dynamics. Suitable for anyone exploring neural coding, plasticity, or neuromorphic model design.


