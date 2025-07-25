# 🧩 A Data-Centric Study on Multi-Domain Reasoning via Reinforcement Learning

Welcome! This is the official codebase for
'A Data-Centric Study on Multi-Domain Reasoning via Reinforcement Learning' 🎉

Explore how data from multiple domains influences reasoning performance, powered by reinforcement learning. Whether you’re a researcher, student, or RL enthusiast, this repo will help you dive into the world of multi-domain data and intelligent reasoning!

## 🚀 Quick Start

### 1. Environment Setup

We recommend using [Conda](https://docs.conda.io/en/latest/) for a clean, reproducible environment.  
All required packages are listed in `requirements.txt`.

Our experiments are built on [VeRL](https://github.com/volcengine/VeRL/tree/v0.2.0.post1) version `v0.2.0.post1` — a fantastic toolkit for RL research!

#### Create and activate the environment:

```bash
conda create -n data_rl python=3.10
conda activate data_rl
pip install -r requirements.txt
```
If you need to install VeRL manually, run:
```bash
git clone https://github.com/volcengine/VeRL.git
cd VeRL
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

### 4. Reward Design

The reward design for all datasets, along with output regularization logic, can be found in  
`verl/utils/reward_score/__init__.py` and the corresponding data-specific files.

## 📧 Contact

If you have any questions, suggestions, or encounter issues, feel free to:
- Open an issue or pull request on GitHub
- Contact us directly at: [liyu1@pjlab.org.cn](mailto:liyu1@pjlab.org.cn)

We're always happy to help and discuss! 😊

## 📢 Citation

If our work helps your research, please consider citing our paper and starring this repo! 🌟




```tex
@misc{li2025domainhelpothersdatacentric,
      title={Can One Domain Help Others? A Data-Centric Study on Multi-Domain Reasoning via Reinforcement Learning}, 
      author={Yu Li and Zhuoshi Pan and Honglin Lin and Mengyuan Sun and Conghui He and Lijun Wu},
      year={2025},
      eprint={2507.17512},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2507.17512}, 
}
```


## 🙏 Acknowledgements

We are extremely grateful to the VeRL team for providing such an efficient and user-friendly RL training framework. Thank you once again for making this research possible!
