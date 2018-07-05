# Rubix

### What is Rubix?
Python library that makes it easy to perform common DevOps operations inside Jupyter Notebooks. Some examples of common operations include plot Cloudwatch metrics, rollback your app on ECS/kubernetes cluster.

### When to use it?
It's useful for writing incident runbooks/playbooks. Steps that on-call needs to perform are written as instructions accompanied with executable code.

### Why Jupyter Notebook?
  - Jupyter allows interleaving instructions and code. Ideal for quick incident response.
  - Rich HTML output makes it easy to plot graphs, show deployment status etc.
  - Low friction edit/view/execute notebooks in a browser.

# Live In Action
Checkout this 1-minute debugging session to see how Rubix helped root cause API latency.
[![Demo Video](https://uploads-ssl.webflow.com/5adf07174a787c7249ade79f/5b0cfeb0db589c364b44ee72_Video_Thumbnail_2.png)](https://www.youtube.com/watch?v=vvLXSAHCGF8&rel=0&autoplay=0 "API Latency Demo")

# Documentation
* [Rubix](http://docs.nurtch.com/en/latest/rubix-library/index.html)
  * [Cloudwatch](http://docs.nurtch.com/en/latest/rubix-library/aws/cloudwatch.html)
  * [Elastic Container Service (ECS)](http://docs.nurtch.com/en/latest/rubix-library/aws/ecs.html)
  * [Kubernetes](http://docs.nurtch.com/en/latest/rubix-library/kubernetes.html#api-usage)

# Installation
```
pip install rubix
```
For your Jupyter/JupyterHub setup, just execute the following at the top of any notebook. Rubix also comes pre-installed with [nurtch](http://nurtch.com) multi-user Jupyter setup.

# Usage
Complete documentation is linked above. These are a few example usage of the library.

### Plot Cloudwatch Metrics
![Cloudwatch Metrics Example](http://docs.nurtch.com/en/latest/_images/plot_metric_example.png)

### Rollback Service in ECS
![ECS Rollback Example](http://docs.nurtch.com/en/latest/_images/ecs_rollback.png)

# Contribute
If you see any problem, open an issue or send a pull request. You can write to me at [amit@nurtch.com](mailto:amit@nurtch.com) or DM me on [twitter](https://twitter.com/amittrathi).
