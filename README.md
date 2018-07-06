# Rubix

### What is Rubix?
Python library that makes it easy to perform common DevOps tasks inside Jupyter Notebooks. E.g. plot Cloudwatch metrics, rollback your ECS/kubernetes app etc.

### When to use it?
While Rubix can be used in other contexts, it's most useful for writing incident runbooks/playbooks. On-call can read instructions & execute steps right from the Jupyter Notebook. I wrote more about the use case [here](https://hackernoon.com/simplify-devops-with-jupyter-notebook-c700fb6b503c).

### Why Jupyter Notebook?
  - Jupyter allows interleaving instructions and executable code. Ideal for quick incident response.
  - Rich HTML output makes it easy to plot graphs, show deployment status etc.
  - Low friction way to edit/view/execute notebooks in a browser.

# Live In Action
Checkout this 1-minute debugging session to see how Rubix helped root cause API latency issue.

[![Demo Video](https://uploads-ssl.webflow.com/5adf07174a787c7249ade79f/5b0cfeb0db589c364b44ee72_Video_Thumbnail_2.png)](https://www.youtube.com/watch?v=vvLXSAHCGF8&rel=0&autoplay=0 "API Latency Demo")

# Documentation
Currently following integrations are supported in Rubix, would love to add more. Note that Jupyter Notebook supports executing [shell commands](http://docs.nurtch.com/en/latest/nurtch-platform/index.html#run-shell-commands-in-notebook) & [SQL queries](http://docs.nurtch.com/en/latest/nurtch-platform/index.html#run-sql-queries-in-notebook) out of the box.
* [Rubix](http://docs.nurtch.com/en/latest/rubix-library/index.html)
  * [Cloudwatch](http://docs.nurtch.com/en/latest/rubix-library/aws/cloudwatch.html)
  * [Elastic Container Service (ECS)](http://docs.nurtch.com/en/latest/rubix-library/aws/ecs.html)
  * [Kubernetes](http://docs.nurtch.com/en/latest/rubix-library/kubernetes.html#api-usage)

# Installation
Rubix exclusively works with Jupyter notebooks. You can [install Jupyter](http://jupyter.org/install) locally or use [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/#) multi user setup. I also built built [nurtch](http://nurtch.com) (commercial) for easy multi user Jupyter setup.
* For your Jupyter/JupyterHub setup, just execute the following at the top of any notebook. Bang operator tells Jupyter to execute this as a terminal command.
```
!pip install rubix
```
* Rubix is pre-installed with [nurtch](http://nurtch.com) multi-user Jupyter setup.

# Usage
Complete documentation is linked above. Here are some usage examples.

### Plot Cloudwatch Metrics
![Cloudwatch Metrics Example](http://docs.nurtch.com/en/latest/_images/plot_metric_example.png)

### Rollback Service in ECS
![ECS Rollback Example](http://docs.nurtch.com/en/latest/_images/ecs_rollback.png)

# Contribute
If you see any problem, open an issue or send a pull request. For additional integrations open an issue with `Feature Request` tag & clearly describe the operations you want to perform. You can write to me at [amit@nurtch.com](mailto:amit@nurtch.com) or DM me on [twitter](https://twitter.com/amittrathi).
