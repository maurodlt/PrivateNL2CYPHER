# Ask Safely – Experimental Code

This repository contains the experimental implementation and materials used in the article **Ask Safely: Privacy-Aware LLM Query Generation for Knowledge Graphs**.
For the production-ready version of Ask Safely, please refer to:

👉 https://github.com/BESSER-PEARL/BESSER-Ask-Safely

To reproduce the experiments, simply install the dependencies from requirements.txt, apply the simple_ner.patch, and run the notebook [`MetaQA-GPT.ipynb`](MetaQA-GPT.ipynb).

The privacy analysis can be visualized in the following notebooks:
- [`Leakage_Test.ipynb`](Leakage_Test.ipynb)
- [`Mutual_Information.ipynb`](Mutual_Information.ipynb)
- [`Token_exposure.ipynb`](Token_exposure.ipynb)

Finally, the manual count of the errors was performed in
[`VisualizeErrors.ipynb`](VisualizeErrors.ipynb).

## Citation

If you use this code, please cite the article:

Tosi, M. D. L., & Cabot, J. (2025). Ask Safely: Privacy-Aware LLM Query Generation for Knowledge Graphs. arXiv preprint arXiv:2512.04852. https://arxiv.org/abs/2512.04852
