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

Built so far:
- `01-introduction/01-overview` (sample, manual check)
- `04-running-apps/01-pods` (sample, real `kubectl` check)

All other lessons: TODO. Add a YAML file in the right folder when ready.
