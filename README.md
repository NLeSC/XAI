# XAI
Resources and Prototyping about eXplainable Artificial Inteligence (XAI)

## Resources

A [github repository](https://github.com/dais-ita/interpretability-papers) collecting Interpretability papers as issues.

Own collection of papers in the [State-of-the-art folder](https://github.com/NLeSC/XAI/tree/master/State-of-the-art)

The data we use in the experiments are available in this [Dropbox folder](https://www.dropbox.com/home/XAI/Data).

### LIME - Local Interpretable Model-Agnostic Explanations
[Paper](https://github.com/NLeSC/XAI/tree/master/State-of-the-art/LIME) in State-of-the-art folder

[Introduciton to LIME](https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime) blog

Open-source Python (BSD-2) [LIME software](https://github.com/marcotcr/lime)

### LRP - Layer-wise Relevance Propagation
[Papers](https://github.com/NLeSC/XAI/tree/master/State-of-the-art/LRP) in State-of-the-art folder

[Interactive LRP demos](http://www.heatmapping.org/) (public page)

[Interactive LRP demos](https://lrpserver.hhi.fraunhofer.de/Demos) (research group page)

[LRP Toolbox](https://github.com/sebastian-lapuschkin/lrp_toolbox) (BSD-2), MATLAB, Python and Caffe

New one keras-oriented is coming up!

[LRP tutorial](http://www.heatmapping.org/tutorial/) (orginial)

[LRP tutorial](https://github.com/NLeSC/XAI/tree/master/Software/Python/LRP%20Tutorial) (redone by me)

### iNNvestigate (the latest LRP & more Toolbox)
[Paper](https://github.com/NLeSC/XAI/blob/master/State-of-the-art/iNNvestigate/iNNvestigatePaper.pdf)

[git repo](https://github.com/albermax/innvestigate)

### SpRAy - Spectral Relevance Analysis (connected to LRP)
[Paper](https://github.com/NLeSC/XAI/blob/master/State-of-the-art/SpRAy/UnmaskingCleverHansPaper.pdf) in State-of-the-art-folder
and especially the [supplementary material](https://github.com/NLeSC/XAI/blob/master/State-of-the-art/SpRAy/UnmaskingCleverHansSuppMaterial.pdf) (much longer than the paper)

### CLEAR - CLass-Enhanced Attentive Response (CLEAR) maps
[Paper](https://github.com/NLeSC/XAI/tree/master/State-of-the-art/CLEAR) in State-of-the-art-folder

### DeepLIFT
[Paper](https://github.com/NLeSC/XAI/tree/master/State-of-the-art/DeepLIFT) in State-of-the-art-folder

### SHAP
[Paper](https://github.com/NLeSC/XAI/tree/master/State-of-the-art/SHAP) in State-of-the-art-folder

### Other
[Building blocks for interpretability](https://distill.pub/2018/building-blocks/) Distill article

## Prototyping 
March, April 2018: [simple experiment](https://github.com/NLeSC/XAI/tree/master/Software/MATLAB/SimpleLRPExperiment) to find out the informativeness of LRP heatmaps on a squares vs triangles classification via CNN task

Later in 2018: Testing model 'adaptor' idea, pilot- [MATLAB NNToolbox <-> LRP Toolbox](https://github.com/NLeSC/XAI/tree/master/Software/MATLAB/NN2LRPToolboxMNISTDemo) ?

May, June 2018: Simple LRP experiemtn with Triangles and Squares dataset.

October 2018: Code  and small experiemtns for the IEEE poster.
