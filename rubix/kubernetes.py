from kubernetes import config, client


def get_latest_deployment_status(service_name, namespace='default', context=None):

    try:
        config.load_kube_config(context=context)
    except FileNotFoundError:
        raise RuntimeError("Could not find Kubernetes config. "
                           "Have you uploaded the config file from Nurtch admin UI? "
                           "If recently uploaded please wait couple of minutes for the file to propagate to every node.")

    core_client = client.CoreV1Api()
    response = core_client.read_namespaced_service(name=service_name, namespace=namespace)
    selector = response.spec.selector

    if not selector:
        raise RuntimeError('This service has no label selector. '
                           'Services without label selector are not handled in Rubix. Use kubectl instead.')

    selector_string = ''

    for k, v in selector.items():
        selector_string += (k + '=' + v + ',')

    selector_string = selector_string[:-1]  # remove trailing comma

    apps_client = client.AppsV1Api()
    response = apps_client.list_replica_set_for_all_namespaces(label_selector=selector_string)

    if response and response.items:
        replica_sets = response.items
        latest_rs = replica_sets[0]
        latest_rs_created_at = replica_sets[0].metadata.creation_timestamp

        for current_rs in replica_sets:
            current_rs_created_at = current_rs.metadata.creation_timestamp

            if current_rs_created_at > latest_rs_created_at:
                latest_rs = current_rs
                latest_rs_created_at = current_rs_created_at

        result = {}
        result['desiredCount'] = latest_rs.spec.replicas
        result['availableCount'] = latest_rs.status.available_replicas
        result['currentCount'] = latest_rs.status.replicas
        result['containerImage'] = latest_rs.spec.template.spec.containers[0].image
        result['createdAt'] = latest_rs.metadata.creation_timestamp

        return result
    else:
        raise RuntimeError('Did not find any recent deployment history of the requested service!')