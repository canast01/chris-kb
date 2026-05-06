# EKS

> Part of the AWS CLI Reference.

---

```bash
# Clusters
aws eks list-clusters
aws eks describe-cluster --name <cluster>

# Update kubeconfig
aws eks update-kubeconfig --name <cluster> --region <region>

# Node groups
aws eks list-nodegroups --cluster-name <cluster>
aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <ng>
```
