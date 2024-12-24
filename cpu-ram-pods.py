
from kubernetes import client, config
from prettytable import PrettyTable
import os

def main():
    # Carga la configuración desde el archivo kubeconfig. Asegúrate de que la ruta sea correcta. 
    kubeconfig_path = os.path.join(os.path.expanduser("~"), ".kube", "kubeconfig")
    try:
        config.load_kube_config(kubeconfig_path)
    except config.ConfigException:
        print(f"Error al cargar la configuración desde {kubeconfig_path}. Asegúrate de que el archivo existe y es válido.")
        return

    v1 = client.CoreV1Api()

    namespaces = v1.list_namespace()

    for namespace in namespaces.items:
        print(f"\nNamespace: {namespace.metadata.name}")
        pods = v1.list_namespaced_pod(namespace.metadata.name)

        table = PrettyTable()
        table.field_names = ["Pod Name", "CPU Request", "CPU Limit", "Memory Request", "Memory Limit"]

        for pod in pods.items:
            pod_name = pod.metadata.name
            for container in pod.spec.containers:
                cpu_request = container.resources.requests.get('cpu') if container.resources.requests else "N/A"
                cpu_limit = container.resources.limits.get('cpu') if container.resources.limits else "N/A"
                memory_request = container.resources.requests.get('memory') if container.resources.requests else "N/A"
                memory_limit = container.resources.limits.get('memory') if container.resources.limits else "N/A"

                table.add_row([pod_name, cpu_request, cpu_limit, memory_request, memory_limit])

        print(table)
if __name__ == "__main__":
    main()
