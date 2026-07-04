# Lesson Review Map

Source of truth for **which concept appears in which lesson**, so warm-ups,
review questions, troubleshooting, and `spaced_hooks` are planned — not
random.

Read this before writing or editing lessons. Update it when you add or move
a concept.

## Legend

- **First taught in** — the lesson that introduces the concept.
- **Recall in** — later lessons whose `warm_up` should reach back for it.
- **Deep reuse in** — later lessons where the concept is used inside the
  main task (spiral learning: same concept, harder scenario).
- **Common failure mode** — the classic mistake we test in
  `troubleshooting` or `common_mistakes`.

## Concept table

| Concept              | First taught in                   | Recall in (warm-up)                                  | Deep reuse in                                        | Common failure mode                                    |
|----------------------|-----------------------------------|------------------------------------------------------|------------------------------------------------------|--------------------------------------------------------|
| Container            | 02-01                             | 02-03, 03-03, 04-01                                  | every workload lesson                                | wrong image tag, image pull error                      |
| Container vs VM      | 02-02                             | 02-03                                                | (concept only)                                       | thinking Pods are VMs                                  |
| Docker basics        | 02-03                             | 03-01, 03-03                                         | 13-01 (CI/CD builds an image)                        | forgetting to push image before cluster tries to pull  |
| Kind local cluster   | 03-01                             | 03-02, 03-03                                         | 06-04 (LoadBalancer stays pending on Kind)           | port-mapping needed, cloud LB not available            |
| kubectl basics       | 03-02                             | 03-03, 04-01, 04-02                                  | every hands-on lesson                                | wrong namespace, wrong context                         |
| YAML apply           | 03-03                             | 04-01, 04-02, 05-01                                  | every workload / config / networking lesson          | wrong `apiVersion`, wrong indent                       |
| Pod                  | 04-01                             | 04-02, 04-03, 05-01, 06-01, 09-01, 10-01             | 07-03 (podSecurity), 11-01 (scheduling), 09-04       | forgetting labels, wrong `restartPolicy`               |
| Labels / selectors   | 04-01 (labels), 04-02 (selectors) | 04-03, 06-01, 07-02, 11-03                           | 06-* (Service selector), 07-02 (NP podSelector)      | selector does not match labels → 0 endpoints           |
| ReplicaSet           | 04-02                             | 04-03                                                | 13-06 (rolling updates)                              | direct edits reverted by owning Deployment             |
| Deployment           | 04-03                             | 04-04, 05-01, 06-01, 09-04, 12-01                    | 07-03, 08-01, 09-*, 11-*, 12-*, 13-*                 | forgetting `spec.selector.matchLabels`                 |
| StatefulSet          | 04-04                             | 10-03                                                | 10-03 (with PVC), 11-04 (priorities)                 | mixing StatefulSet with Deployment volume patterns     |
| Job / CronJob        | 04-05                             | 08-03, 13-01                                         | 12-03 (scale-to-zero patterns)                       | forgetting `restartPolicy: OnFailure` or `Never`       |
| ConfigMap            | 05-01                             | 05-02, 06-01, 08-01, 09-04, 13-02                    | 07-01 (RBAC to read), 13-03 (Helm values)            | env var name vs key name confusion                     |
| Secret               | 05-02                             | 06-01, 07-01, 07-03, 13-02                           | 07-03 (avoid mounting as env), 13-02 (sealed)        | mistaking base64 for encryption                        |
| Service (ClusterIP)  | 06-01                             | 06-02, 06-05, 07-02, 09-04, 12-01                    | 06-04, 10-03, 13-04                                  | selector mismatch, port vs targetPort                  |
| NodePort             | 06-02                             | 06-04                                                | 06-04 (comparison to Ingress)                        | high port range, security concerns                     |
| Helm                 | 06-03                             | 06-04, 13-03                                         | 13-02 (GitOps deploys Helm), 07-01 (helm + RBAC)     | forgetting `helm repo update`                          |
| LoadBalancer/Ingress | 06-04                             | 06-05, 13-04, 13-05                                  | 13-*, 09-04 (health under Ingress)                   | wrong `ingressClassName`, host header mismatch         |
| Pod-to-Pod DNS       | 06-05                             | 07-02, 10-03                                         | 09-03 (traces), 13-02 (services in envs)             | using pod IP instead of Service DNS name               |
| RBAC                 | 07-01                             | 07-03, 13-02, 14-02                                  | 14-* (controllers need Roles)                        | cluster-wide `*` verbs, wrong subject                  |
| NetworkPolicy        | 07-02                             | 07-03, 10-03                                         | 13-04 (canary + policies)                            | default-deny too early breaks Pods                     |
| Pod security         | 07-03                             | 08-01, 10-03, 11-05                                  | 13-* (image scanning), 14-*                          | running as root, missing seccomp                       |
| Requests / limits    | 08-01                             | 08-02, 08-03, 09-02, 11-01, 12-01, 12-02             | 11-04 (priorities), 12-* (HPA/VPA need requests)     | missing requests → bad scheduling, no HPA              |
| Namespaces           | 08-02                             | 08-03, 09-*, 11-*                                    | 07-01 (RBAC scope), 13-02                            | forgetting `-n` on kubectl → default namespace         |
| Resource quotas      | 08-02                             | 08-03                                                | 12-03 (autoscaling under quota)                      | quota blocks Pod creation silently                     |
| Optimize usage       | 08-03                             | 12-*                                                 | 12-* (VPA), 09-02                                    | over-requesting causing waste                          |
| Logs                 | 09-01                             | 09-05, 13-01                                         | 07-03 (audit), 09-04 (probes fail)                   | logs disappear when pod restarts                       |
| Metrics              | 09-02                             | 09-04, 09-05, 12-01, 12-02                           | 12-* (HPA reads metrics)                             | Metrics Server not installed                           |
| Traces               | 09-03                             | 09-05                                                | 13-* (canary uses traces)                            | thinking traces = logs                                 |
| Probes (liveness/readiness) | 09-04                      | 09-05, 12-01, 13-04, 13-06                           | 13-06 (rollout waits on readiness)                   | liveness too aggressive → restart loop                 |
| Volumes / PV / PVC   | 10-01                             | 10-02, 10-03                                         | 04-04 revisit                                         | forgetting `accessModes` matching StorageClass         |
| CSI drivers          | 10-02                             | 10-03                                                | 14-* (CRDs from CSI)                                 | choosing wrong access mode                             |
| Stateful apps        | 10-03                             | 11-04                                                | 13-05 (blue/green + stateful)                        | draining a StatefulSet pod without care                |
| Scheduling basics    | 11-01                             | 11-02, 11-03, 11-04, 11-05                           | 12-* (Cluster autoscaler)                            | thinking node with most CPU wins                       |
| Taints / tolerations | 11-02                             | 11-03, 11-04, 11-05                                  | 12-03 (autoscaler adds tainted nodes)                | taint blocks system Pods                               |
| Topology spread      | 11-03                             | 11-04                                                | 13-04 (canary needs spread)                          | `whenUnsatisfiable: DoNotSchedule` too strict          |
| Priorities           | 11-04                             | 11-05                                                | 12-* (preemption during autoscale)                   | preemption of critical Pods                            |
| Evictions            | 11-05                             | 12-*                                                 | 13-* (rolling updates + PDB)                         | missing PodDisruptionBudget                            |
| HPA                  | 12-01                             | 12-02, 12-03, 13-04                                  | 13-* (canary + HPA)                                  | HPA without requests defined                           |
| VPA                  | 12-02                             | 12-03                                                | 08-* revisit                                         | VPA + HPA on same metric conflict                      |
| Cluster autoscaling  | 12-03                             | 13-* (rollouts)                                      | 14-04 (multi-cluster)                                | wrong instance type, cold start                        |
| CI/CD                | 13-01                             | 13-02                                                | 13-04, 13-05, 13-06                                  | secrets in git, no image scanning                      |
| GitOps               | 13-02                             | 13-03, 13-04                                         | 14-01 (CRDs behind GitOps)                           | drift not detected                                     |
| Canary               | 13-04                             | 13-05                                                | 14-02 (controller for canary)                        | traffic split not respected                            |
| Blue-green           | 13-05                             | 13-06                                                | (concept only)                                       | forgetting DB migration compatibility                  |
| Rolling updates      | 13-06                             | 14-04                                                | 04-03 revisit                                        | `maxUnavailable` too high                              |
| CRDs                 | 14-01                             | 14-02                                                | 14-03, 14-04                                         | schema breaking change                                 |
| Custom controllers   | 14-02                             | 14-03                                                | 14-04                                                | reconcile loop without back-off                        |
| Custom schedulers    | 14-03                             | 14-04                                                | (concept only)                                       | scheduler conflict with default                        |
| Multi-cluster        | 14-04                             | (capstone)                                           | (capstone)                                           | network partition assumptions                          |

## How to use this table when writing a lesson

For each new lesson `L`:

1. Find its row in **First taught in**. That is L's *new concept*.
2. Scan for rows where L appears in **Recall in** — those concepts belong
   in L's `warm_up` block (2–3 questions from earlier lessons).
3. Scan for rows where L appears in **Deep reuse in** — those concepts
   must be *used inside* L's `task` (not just mentioned). This is
   interleaving.
4. The row's **Common failure mode** feeds `troubleshooting` and
   `common_mistakes`.
5. For `spaced_hooks`, look forward: which later lesson does the new
   concept appear in as **Recall in** or **Deep reuse in**? Pick 2–3 and
   set the `when` field accordingly (`next`, `2-3`, `5-7`, `capstone`).

## Reading the columns of L

- `warm_up` — pulled from **Recall in** rows pointing at L.
- `task` interleaving — pulled from **Deep reuse in** rows pointing at L.
- `troubleshooting` — from **Common failure mode** of the *new* concept.
- `common_mistakes` — same row.
- `spaced_hooks` — L's own concept pointed forward.
