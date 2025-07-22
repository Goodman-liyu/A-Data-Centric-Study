# 🧩 A Data-Centric Study on Multi-Domain Reasoning via Reinforcement Learning

Welcome! This is the official codebase for  
**A Data-Centric Study on Multi-Domain Reasoning via Reinforcement Learning** 🎉

Explore how data from multiple domains influences reasoning performance, powered by reinforcement learning. Whether you're a researcher, student, or RL enthusiast, this repo will help you dive into the world of multi-domain data and intelligent LLM!

---

## 🚀 Quick Start

### 1. Environment Setup

We recommend using [conda](https://docs.conda.io/en/latest/) for a clean, reproducible environment.  
All required packages are listed in `requirements.txt`.

Our experiments are built on [VERL](https://github.com/volcengine/verl/tree/v0.2.0.post1) version `v0.2.0.post1` — a fantastic toolkit for RL research!

#### Create and activate the environment:

```bash
conda create -n data_rl python=3.10
conda activate data_rl
pip install -r requirements.txt
```
If you need to install VERL manually, run:
```bash
git clone https://github.com/volcengine/verl.git
cd verl
git checkout v0.2.0.post1
pip install -e .
```

### 2. Experiment Data

All datasets used in our experiments are located in the **`data/`** directory.
You’ll find five R1-style datasets for each of the three domains—ready to use and easy to explore.

### 3. Run the Experiments

To reproduce our results, simply execute:
```bash
bash run.sh
```
This script takes care of data processing, training, and evaluation.
Sit back and watch your models learn! 🤖✨

To run experiments on other domain combinations, you can modify the model path, data path, and training hyperparameters accordingly.

Note:
When performing curriculum learning, we recommend setting `data.shuffle = False` to ensure the data order is preserved.
Shuffling may disrupt the intended learning progression and lead to suboptimal results.
🙏 Acknowledgements

A huge thank you to the VERL team for their amazing open-source reinforcement learning library.
We couldn’t have done this without you!

⸻

📢 Citation

If our work helps your research, please consider citing our paper (citation info will be added upon publication) and starring this repo! 🌟

⸻

Happy hacking!
If you have questions, suggestions, or want to share your results, open an issue or pull request.
Let’s push the limits of multi-domain reasoning together! 🚀
