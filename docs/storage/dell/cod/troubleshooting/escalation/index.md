# COD — Escalation

> Part of the [COD](../../) reference.

---

## Support Portal

Open a Dell support case at [https://www.dell.com/support](https://www.dell.com/support). For COD license issues, select the affected PowerMax array as the primary product and specify COD / licensing as the impacted component.

## Information to Collect

Before opening a case:

- Array SID: `symcfg list`
- Current license state: `symlicense -sid <SID> list`
- Full error from failed license install: `symlicense -sid <SID> install -file <file> 2>&1`
- License file (do not share publicly — attach securely to the case)
- Unisphere version and SCG connectivity status

## Escalation Path

1. Open a standard support case via Dell support portal
2. If the activation is time-critical (emergency capacity event), request **Priority 1** escalation and contact your Dell account team directly to expedite
3. For license file re-issuance issues (wrong SID), the Dell License Management team handles this separately from standard support — your account team can connect you directly
