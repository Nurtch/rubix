import time
from IPython import display
from IPython.display import HTML, Markdown
from ipywidgets import Output

from rubix.aws.base import get_client
from rubix.utils import print_markdown_table, first, printmd


def get_latest_deployment_status(service, **kwargs):
    client = get_client('ecs', **kwargs)
    cluster = kwargs.get('cluster')

    if cluster and not isinstance(cluster, str):
        raise ValueError('Cluster value should be of type str')

    response = client.describe_services(
        cluster=cluster,
        services=[service]
    )

    if not response['services']:
        raise ValueError('Service could not be found. Please check service name, cluster name, and aws region. Make sure the AWS credentials have rights to access ECS!')

    if not response['services'][0]['deployments']:
        print('No deployments found! Have you just spin up the service recently?')

    deployments = response['services'][0]['deployments']
    recent_deployment = {}

    for deployment in deployments:
        if deployment['status'] == 'PRIMARY':
            recent_deployment = deployment.copy()

    recent_deployment.pop('status', None)
    recent_deployment.pop('launchType', None)
    return recent_deployment


def rollback_deployment(service, **kwargs):
    client = get_client('ecs', **kwargs)
    cluster = kwargs.get('cluster')

    if cluster and not isinstance(cluster, str):
        raise ValueError('Cluster value should be of type str')

    if cluster:
        try:
            response = client.describe_services(
                cluster=cluster,
                services=[service]
            )
        except client.exceptions.ServiceNotFoundException:
            raise ValueError('Could not find service %s. Please check service, cluster, region and that IAM credentials has access to ECS' % service)
    else:
        try:
            # default cluster is assumed when not specified
            response = client.describe_services(
                services=[service]
            )
        except client.exceptions.ClusterNotFoundException:
            raise ValueError('Could not find service %s in default cluster. Please specify cluster.' % service)

    if not response['services']:
        raise ValueError('Service could not be found. Please check service name, cluster name, and aws region. Make sure the AWS credentials have rights to access ECS!')

    current_task_definiton = response['services'][0]['taskDefinition']
    print('Current task definition for service %s is:: %s' % (service, current_task_definiton))

    response = client.describe_task_definition(
        taskDefinition=current_task_definiton
    )

    task_definiton_family = response['taskDefinition']['family']

    response = client.list_task_definitions(
        familyPrefix=task_definiton_family,
        status='INACTIVE',
        sort='DESC',
        maxResults=5
    )

    task_definitions = response['taskDefinitionArns']

    if not task_definitions:
        raise ValueError('Could not find previous task definitions for service %s. Make sure that the previous task definiton exist and they are marked INACTIVE.' % service)

    rollback_candidates = []

    for td in task_definitions:
        response = client.describe_task_definition(
            taskDefinition=td
        )

        image = response['taskDefinition']['containerDefinitions'][0]['image']
        rollback_candidates.append([td, image])

    print_markdown_table(headers=['Task Definitions', 'Container Image'], data=rollback_candidates)
    rollback_td = input('Enter the task defintion that you want to rollback to: ')

    response = client.describe_task_definition(
        taskDefinition=rollback_td
    )

    response = response['taskDefinition']

    new_td = client.register_task_definition(
        family=response['family'],
        containerDefinitions=response['containerDefinitions']
    )

    client.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=new_td['taskDefinition']['taskDefinitionArn']
    )

    markdown_string = ''
    progress_bar_url = "http://progressed.io/bar/0"

    deployment_status_output = Output()
    display.display(deployment_status_output)

    # poll for 10 minutes for updates (120 * 5 second wait)
    for i in range(121):
        response = client.describe_services(
            cluster=cluster,
            services=[service]
        )

        deployments = response['services'][0]['deployments']
        primary_deployment = first(d for d in deployments if d['status'] == 'PRIMARY')

        desired_count = primary_deployment['desiredCount']
        running_count = primary_deployment['runningCount']

        status = int(running_count * 100 / desired_count)
        progress_bar_url = "http://progressed.io/bar/" + str(status)
        markdown_string = "# New Task Definition\n" + "* **Desired Count: " + str(desired_count) + "**\n" + "* **Running Count: " + str(running_count) + "**"
        deployment_status_output.clear_output(wait=True)

        with deployment_status_output:
            printmd(markdown_string)
            display.display(
                HTML(
                    "<table><tr><td><b>Deployment Status</b></td><td><img src=" + progress_bar_url + "></td></tr></table>"))
            display.display(HTML("<div class=\"loader\"></div>"))

        if status == 100:
            break

        time.sleep(4.5)

    deployment_status_output.clear_output(wait=True)

    with deployment_status_output:
        printmd(markdown_string)
        display.display(
            HTML(
                "<table><tr><td><b>Deployment Status</b></td><td><img src=" + progress_bar_url + "></td></tr></table>"))
        display.display(HTML("<div class=\"stoppedloader\"></div>"))
