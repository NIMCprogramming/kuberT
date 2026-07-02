# kuberT Roadmap

The lesson order is based on [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes).

This file is the **source of truth** for the lesson list. Each module here matches a folder in `lessons/`. Each lesson sub-item should match a YAML file in that folder.

| #  | Module (folder)            | Lessons inside                                                                    |
|----|----------------------------|-----------------------------------------------------------------------------------|
| 01 | `01-introduction`          | Overview · Why Kubernetes · Key concepts · Alternatives                           |
| 02 | `02-containers`            | What is a container · Container vs VM · Docker for K8s                            |
| 03 | `03-setting-up`            | Local cluster with Kind · First kubectl · First app                               |
| 04 | `04-running-apps`          | Pods · ReplicaSets · Deployments · StatefulSets · Jobs                            |
| 05 | `05-configuration`         | ConfigMaps · Secrets                                                              |
| 06 | `06-services-networking`   | Services basics · External access · LoadBalancer · Pod-to-Pod                     |
| 07 | `07-security`              | RBAC · Network policies · Pod security                                            |
| 08 | `08-resources`             | Requests/Limits · Namespaces & Quotas · Optimize usage                            |
| 09 | `09-observability`         | Logs · Metrics · Traces · Health · Tools                                          |
| 10 | `10-storage`               | Volumes basics · CSI drivers · Stateful apps                                      |
| 11 | `11-scheduling`            | Basics · Taints/Tolerations · Topology spread · Priorities · Evictions            |
| 12 | `12-autoscaling`           | HPA · VPA · Cluster autoscaling                                                   |
| 13 | `13-deployment-patterns`   | CI/CD · GitOps · Helm · Canary · Blue-Green · Rolling updates                     |
| 14 | `14-advanced`              | CRDs · Custom controllers · Custom schedulers · Multi-cluster                     |

## Status

All modules have lesson YAML files. Lessons follow roadmap.sh/kubernetes
sub-topics and use A2 English.

- `01-introduction/`: overview, why-kubernetes, key-concepts, alternatives
- `02-containers/`: what-is-a-container, container-vs-vm, docker-for-k8s
- `03-setting-up/`: local-cluster-with-kind, first-kubectl, first-app
- `04-running-apps/`: pods, replicasets, deployments, statefulsets, jobs
- `05-configuration/`: configmaps, secrets
- `06-services-networking/`: services-basics, external-access, helm-basics, loadbalancer, pod-to-pod
- `07-security/`: rbac, network-policies, pod-security
- `08-resources/`: requests-limits, namespaces-quotas, optimize-usage
- `09-observability/`: logs, metrics, traces, health, tools
- `10-storage/`: volumes-basics, csi-drivers, stateful-apps
- `11-scheduling/`: basics, taints-tolerations, topology-spread, priorities, evictions
- `12-autoscaling/`: hpa, vpa, cluster-autoscaling
- `13-deployment-patterns/`: ci-cd, gitops, helm, canary, blue-green, rolling-updates
- `14-advanced/`: crds, custom-controllers, custom-schedulers, multi-cluster
