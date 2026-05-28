"""
Data protection, database, integration, inventory, performance, architecture, networking.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import kb_diagram, make_helpers, bTop, bMid, bBot, sections, arrow, connector, merge, title_border, row

# ── Data Protection ───────────────────────────────────────────────────────────

@kb_diagram(
    'data-protection',
    'docs/data-protection/index.md',
    'Data Protection landing — classification, encryption, retention, key management and recovery',
)
def data_protection_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Data Protection — Classification, Encryption, Retention & Recovery'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data protection: classify data by sensitivity → encrypt at rest and in transit →')))
    lines.append(R(bMid(IV_L, IV_R, 'enforce retention schedules → manage encryption keys → test recovery procedures')))
    lines.append(R(bMid(IV_L, IV_R, 'Foundation: know what data exists, where it lives, who owns it, and for how long')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Classify → Encrypt → Retain → Test recovery → Govern access → Audit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Classification'), bMid(B2_L, B2_R, 'Encryption'), bMid(B3_L, B3_R, 'Retention & Keys'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Public / Internal'), bMid(B2_L, B2_R, 'AES-256 at rest'), bMid(B3_L, B3_R, 'Schedules by type'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confidential'), bMid(B2_L, B2_R, 'TLS 1.2/1.3 transit'), bMid(B3_L, B3_R, 'Legal hold process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Restricted / PII'), bMid(B2_L, B2_R, 'KMS key management'), bMid(B3_L, B3_R, 'Deletion verified'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MIP sensitivity lbls'), bMid(B2_L, B2_R, 'Key rotation sched'), bMid(B3_L, B3_R, 'Restore testing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Handling controls'), bMid(B2_L, B2_R, 'BYOK for compliance'), bMid(B3_L, B3_R, 'Compliance reports'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  PII        = Personally Identifiable Information; highest classification; GDPR/CCPA applies'))
    lines.append(txt_row('  PHI        = Protected Health Information; HIPAA regulated; strict access and audit logging'))
    lines.append(txt_row('  PCI        = Payment Card Industry; cardholder data subject to PCI DSS controls'))
    lines.append(txt_row('  AES-256    = Advanced Encryption Standard 256-bit; standard for encryption at rest'))
    lines.append(txt_row('  KMS        = Key Management Service; manages encryption key lifecycle and access policies'))
    lines.append(txt_row('  HSM        = Hardware Security Module; tamper-resistant device for key storage'))
    lines.append(txt_row('  Legal hold = Suspend deletion of data pending litigation or regulatory investigation'))
    lines.append(txt_row('  DLP        = Data Loss Prevention; prevents unauthorised data exfiltration'))
    lines.append(txt_row('  BYOK       = Bring Your Own Key; customer-managed keys in cloud KMS for compliance'))
    lines.append(txt_row('  MIP        = Microsoft Information Protection; sensitivity labels on Office content'))
    lines.append(txt_row('  DEK        = Data Encryption Key; key that directly encrypts a data object'))
    lines.append(txt_row('  KEK        = Key Encryption Key; wraps and protects data encryption keys'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-backup-validation',
    'docs/data-protection/backup-validation/index.md',
    'Backup validation — verify job completion, restore testing, retention compliance',
)
def dp_backup_validation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Data Protection — Backup Validation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Backup validation: confirm jobs complete, data is intact, restores work before needed')))
    lines.append(R(bMid(IV_L, IV_R, 'Automated: every job — checksums + VM boot test; evidence in job log')))
    lines.append(R(bMid(IV_L, IV_R, 'Manual: quarterly — full application restore with user acceptance and signed report')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Automated Validation'), bMid(B2_L, B2_R, 'Manual Restore Testing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Veeam SureBackup: boot VM test'), bMid(B2_L, B2_R, 'Quarterly full restore test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Commvault: snap verify mount'), bMid(B2_L, B2_R, 'Application-level acceptance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NBU bpverify: media integrity'), bMid(B2_L, B2_R, 'User validates restored data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Checksum validation on file'), bMid(B2_L, B2_R, 'Document result + sign-off'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert on job failure or skip'), bMid(B2_L, B2_R, 'Update test calendar entry'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Tier', 'Method', 'Frequency', 'Success criteria', 'Evidence'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Auto/basic', 'Job log check', 'Every backup', 'Job success', 'Job log entry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Auto/deep', 'Mount/boot VM', 'Daily/weekly', 'VM boots clean', 'SureBackup log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Manual', 'Full restore', 'Quarterly', 'App functional', 'Signed report'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SureBackup  = Veeam automated recovery verification; boots VM from backup in isolated sandbox'))
    lines.append(txt_row('  bpverify    = NetBackup command; reads backup image and verifies data integrity on media'))
    lines.append(txt_row('  Checksum    = Hash of backup data; mismatch indicates corruption in backup storage'))
    lines.append(txt_row('  RTO         = Recovery Time Objective; max time to restore; verified in manual restore tests'))
    lines.append(txt_row('  RPO         = Recovery Point Objective; max data loss; validated by backup job frequency'))
    lines.append(txt_row('  Snap verify = Mount snapshot in sandbox and run application check scripts'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-data-classification',
    'docs/data-protection/data-classification/index.md',
    'Data classification — tiers, labelling requirements, handling rules per sensitivity level',
)
def dp_data_classification():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Data Protection — Data Classification'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Classification defines how sensitive information must be labelled, handled, and stored')))
    lines.append(R(bMid(IV_L, IV_R, 'Four tiers: Public → Internal → Confidential → Restricted; each has handling rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Apply the highest classification that any data element in a set warrants')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Classification Levels'), bMid(B2_L, B2_R, 'Labelling Requirements'), bMid(B3_L, B3_R, 'Handling Controls'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Public'), bMid(B2_L, B2_R, 'Optional label'), bMid(B3_L, B3_R, 'No restrictions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Internal'), bMid(B2_L, B2_R, 'Header/footer label'), bMid(B3_L, B3_R, 'Employee access only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confidential'), bMid(B2_L, B2_R, 'MIP label required'), bMid(B3_L, B3_R, 'Need-to-know; encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Restricted/PII/PHI'), bMid(B2_L, B2_R, 'Purview sensitivity'), bMid(B3_L, B3_R, 'Strict; audit logged'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Examples per level'), bMid(B2_L, B2_R, 'Email + docs + storage'), bMid(B3_L, B3_R, 'Encrypted volume'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Level', 'Examples', 'Storage', 'Email', 'Access'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Public', 'Marketing', 'No requirement', 'No label', 'Anyone'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Internal', 'Policies, plans', 'Standard ACL', 'Label only', 'Employees'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Confidential', 'Finance, HR', 'Encrypted vol', '+encrypt ext', 'Need-to-know'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Restricted', 'PII, PCI, PHI', 'HSM-backed', '+DLP policy', 'Strict + audit'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Sensitivity label  = Tag applied to document/email; drives DLP and encryption policies'))
    lines.append(txt_row('  MIP / Purview      = Microsoft tools for applying and enforcing sensitivity labels'))
    lines.append(txt_row('  Need-to-know       = Access granted only when required by job function; not role alone'))
    lines.append(txt_row('  Data owner         = Business-unit leader accountable for a dataset and its classification'))
    lines.append(txt_row('  DLP policy         = Enforces labelling rules; blocks transfer of classified data outside perimeter'))
    lines.append(txt_row('  Reclassification   = Formal review to raise or lower a classification based on changed context'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-data-encryption',
    'docs/data-protection/data-encryption/index.md',
    'Data encryption — at rest and in transit, standards, key management and compliance',
)
def dp_data_encryption():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Data Protection — Data Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Encrypt all sensitive data at rest and all data in transit regardless of classification')))
    lines.append(R(bMid(IV_L, IV_R, 'At rest: AES-256 minimum; managed via KMS or HSM; keys rotated on schedule')))
    lines.append(R(bMid(IV_L, IV_R, 'In transit: TLS 1.2 minimum, 1.3 preferred; no unencrypted admin protocols (Telnet/FTP)')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption at Rest'), bMid(B2_L, B2_R, 'Encryption in Transit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux: LUKS volume encryption'), bMid(B2_L, B2_R, 'TLS 1.3 for HTTPS APIs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Windows: BitLocker + TPM'), bMid(B2_L, B2_R, 'SSH for admin access'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage array native encrypt'), bMid(B2_L, B2_R, 'IPsec site-to-site VPN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cloud: AWS KMS / AKV'), bMid(B2_L, B2_R, 'mTLS for service mesh'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB: TDE (Transparent DE)'), bMid(B2_L, B2_R, 'LDAPS (not plain LDAP)'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  LUKS       = Linux Unified Key Setup; block device encryption; key stored in LUKS header'))
    lines.append(txt_row('  BitLocker  = Windows full-volume encryption; TPM stores key; recoverable via AD/Azure AD'))
    lines.append(txt_row('  TDE        = Transparent Data Encryption; DB-level encryption; transparent to application'))
    lines.append(txt_row('  AKV        = Azure Key Vault; managed HSM for keys, secrets, and certificates in Azure'))
    lines.append(txt_row('  mTLS       = Mutual TLS; both client and server present certificates; service-to-service auth'))
    lines.append(txt_row('  TPM        = Trusted Platform Module; chip that stores BitLocker key; ties disk to hardware'))
    lines.append(txt_row('  Cipher     = Algorithm used for encryption; AES-256-GCM is standard for new deployments'))
    lines.append(txt_row('  TLS 1.3    = Latest TLS version; removes weak ciphers; mandatory for public-facing services'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-data-governance',
    'docs/data-protection/data-governance/index.md',
    'Data governance — ownership, access controls, audit requirements, regulatory alignment',
)
def dp_data_governance():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Data Protection — Data Governance'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data governance: define who owns data, who can access it, and how its use is audited')))
    lines.append(R(bMid(IV_L, IV_R, 'Roles: owner (accountable) → steward (operational) → custodian (IT stores/secures)')))
    lines.append(R(bMid(IV_L, IV_R, 'Aligned to regulations: GDPR (EU PII), HIPAA (PHI), SOX (financial), PCI DSS (cards)')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data Ownership'), bMid(B2_L, B2_R, 'Access Controls'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Owner: BU lead'), bMid(B2_L, B2_R, 'RBAC + least priv'), bMid(B3_L, B3_R, 'GDPR — EU PII'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Steward: BU member'), bMid(B2_L, B2_R, 'Quarterly access rev'), bMid(B3_L, B3_R, 'HIPAA — PHI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Custodian: IT/ops'), bMid(B2_L, B2_R, 'JIT / PIM for priv'), bMid(B3_L, B3_R, 'SOX — financial'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Processor: vendor'), bMid(B2_L, B2_R, 'Audit log all access'), bMid(B3_L, B3_R, 'PCI DSS — cards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DPA agreements'), bMid(B2_L, B2_R, 'Breach notification'), bMid(B3_L, B3_R, 'Annual DPA review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Data owner    = Business accountable for a dataset; approves access and classification'))
    lines.append(txt_row('  Data steward  = Day-to-day oversight of data quality and policy compliance in a domain'))
    lines.append(txt_row('  Data custodian= IT team responsible for storing, securing, and backing up the data'))
    lines.append(txt_row('  DPA           = Data Processing Agreement; contract with vendors who process personal data'))
    lines.append(txt_row('  GDPR          = EU regulation; rights over personal data; 72h breach notification'))
    lines.append(txt_row('  JIT           = Just-In-Time access; privileged access granted for a time-limited session'))
    lines.append(txt_row('  PIM           = Privileged Identity Management; Azure AD tool for JIT role activation'))
    lines.append(txt_row('  Access review = Periodic check that all current permissions are still appropriate and needed'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-retention-policy',
    'docs/data-protection/data-retention-policy/index.md',
    'Data retention policy — schedules by data type, legal holds, deletion verification',
)
def dp_retention_policy():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Data Protection — Data Retention Policy'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Retention policy: minimum time data must be kept; maximum time before secure deletion')))
    lines.append(R(bMid(IV_L, IV_R, 'Legal hold suspends all deletion for data subject to litigation or regulatory inquiry')))
    lines.append(R(bMid(IV_L, IV_R, 'Verify deletions: cryptographic erasure or physical destruction with certificate')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Retention Schedules'), bMid(B2_L, B2_R, 'Deletion Procedures'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Financial records: 7+ years'), bMid(B2_L, B2_R, 'Check no active legal hold'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HR records: varies by region'), bMid(B2_L, B2_R, 'Confirm retention period met'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit/security logs: 1-3 yr'), bMid(B2_L, B2_R, 'Cryptographic erasure or DoD'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email: 3-7 years (policy)'), bMid(B2_L, B2_R, 'Certificate of destruction'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backups: per RPO tier'), bMid(B2_L, B2_R, 'Remove from all systems'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Data type', 'Min retain', 'Max retain', 'Regulation', 'Delete method'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Financial', '7 years', '10 years', 'SOX/local', 'Secure erase'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Security logs', '1 year', '3 years', 'PCI / ISO', 'Log purge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PII/personal', '2 years', '5 years', 'GDPR', 'Crypto erase'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Backups', 'Per RPO', '90 days', 'Policy', 'Tape destroy'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Legal hold       = Suspend all deletion for data subject to litigation; placed by legal team'))
    lines.append(txt_row('  Crypto erasure   = Delete encryption key so data is permanently unreadable without destruction'))
    lines.append(txt_row('  DoD 5220.22-M    = US DoD secure wipe standard; multiple overwrite passes on magnetic media'))
    lines.append(txt_row('  Retention period = Minimum time data must exist before deletion can be authorised'))
    lines.append(txt_row('  eDiscovery       = Search and collection of electronic data for legal proceedings'))
    lines.append(txt_row('  Disposition      = Final action on data: delete, archive, or transfer at end of retention'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-key-management',
    'docs/data-protection/key-management/index.md',
    'Key management — KMS architecture, key rotation, HSM integration references',
)
def dp_key_management():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Data Protection — Key Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Key management: generate, store, rotate, and retire encryption keys securely')))
    lines.append(R(bMid(IV_L, IV_R, 'Envelope encryption: DEK encrypts data; KEK (in KMS/HSM) wraps the DEK')))
    lines.append(R(bMid(IV_L, IV_R, 'Rotation: annual minimum; immediate on suspected compromise; automate in KMS')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Lifecycle'), bMid(B2_L, B2_R, 'HSM & Cloud KMS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Generate (KMS or HSM)'), bMid(B2_L, B2_R, 'AWS KMS: CMK / data keys'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Activate + distribute'), bMid(B2_L, B2_R, 'Azure Key Vault: keys/secrets'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Rotate on schedule'), bMid(B2_L, B2_R, 'HashiCorp Vault: transit eng'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Revoke on compromise'), bMid(B2_L, B2_R, 'BYOK: import customer key'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Archive then destroy'), bMid(B2_L, B2_R, 'HSM: FIPS 140-2 Level 3'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DEK          = Data Encryption Key; AES-256 key that encrypts actual data blocks'))
    lines.append(txt_row('  KEK          = Key Encryption Key; wraps the DEK; stored in HSM or KMS; not exported'))
    lines.append(txt_row('  Envelope enc = Encrypt DEK with KEK; only KEK needs HSM protection; scales efficiently'))
    lines.append(txt_row('  CMK          = Customer Master Key (AWS); top-level KMS key used to derive data keys'))
    lines.append(txt_row('  BYOK         = Bring Your Own Key; customer generates key material and imports to cloud KMS'))
    lines.append(txt_row('  FIPS 140-2   = US standard for cryptographic module security; Level 3 = HSM tamper-evident'))
    lines.append(txt_row('  Key rotation = Generate new key version; re-encrypt new data; retain old to decrypt existing'))
    lines.append(txt_row('  Transit eng  = Vault secrets engine; encrypts/decrypts via API without exposing key material'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dp-recovery-testing',
    'docs/data-protection/recovery-testing/index.md',
    'Recovery testing — restore test procedures, DR test schedules, test result documentation',
)
def dp_recovery_testing():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Data Protection — Recovery Testing'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery testing validates that backup data is restorable and DR procedures work')))
    lines.append(R(bMid(IV_L, IV_R, 'Schedule: file restore monthly; VM restore quarterly; full DR exercise annually')))
    lines.append(R(bMid(IV_L, IV_R, 'Always document: start time, end time, RTO/RPO achieved, issues found, sign-off')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test Types'), bMid(B2_L, B2_R, 'Scheduling'), bMid(B3_L, B3_R, 'Evidence Required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'File restore test'), bMid(B2_L, B2_R, 'Monthly'), bMid(B3_L, B3_R, 'File hash match'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM restore test'), bMid(B2_L, B2_R, 'Quarterly'), bMid(B3_L, B3_R, 'VM boots; app OK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB restore test'), bMid(B2_L, B2_R, 'Quarterly'), bMid(B3_L, B3_R, 'Row count + query'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Full DR failover'), bMid(B2_L, B2_R, 'Annually'), bMid(B3_L, B3_R, 'RTO/RPO met'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tabletop exercise'), bMid(B2_L, B2_R, 'Annually'), bMid(B3_L, B3_R, 'Actions recorded'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Test type', 'Freq', 'Success criteria', 'RTO target', 'Documented by'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['File restore', 'Monthly', 'File matches source', '< 1h', 'Ops team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['VM restore', 'Quarterly', 'VM boots; app runs', '< 4h', 'Ops + app owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['DR failover', 'Annually', 'All svcs at DR site', 'Per BCP', 'DR lead + mgmt'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Tabletop exercise = Walk through DR scenario verbally; identify gaps without production impact'))
    lines.append(txt_row('  RTO tested        = Actual restore time measured during test; compared to RTO target'))
    lines.append(txt_row('  RPO tested        = Latest recovery point verified; gap between backup and incident time'))
    lines.append(txt_row('  Sign-off          = Manager/owner approval confirming test was successful and documented'))
    lines.append(txt_row('  Restore report    = Formal record of test result; filed for audit evidence'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Database ──────────────────────────────────────────────────────────────────

@kb_diagram(
    'database',
    'docs/database/index.md',
    'Database landing — health checks, backup validation, failover, maintenance and performance',
)
def database_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Database — Health, Backup, Failover & Performance'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Database operational references: PostgreSQL, MySQL/MariaDB, and SQL Server procedures')))
    lines.append(R(bMid(IV_L, IV_R, 'Covers: daily health checks, backup validation, planned/unplanned failover, maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'Performance: slow query diagnosis, blocking chains, lock contention, I/O bottlenecks')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Monitor → Backup → Maintain → Capacity plan → Troubleshoot → Failover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health & Monitoring'), bMid(B2_L, B2_R, 'Backup & Recovery'), bMid(B3_L, B3_R, 'Performance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connection counts'), bMid(B2_L, B2_R, 'Job completion check'), bMid(B3_L, B3_R, 'Slow query log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Blocking/deadlocks'), bMid(B2_L, B2_R, 'Restore verification'), bMid(B3_L, B3_R, 'EXPLAIN / AWR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Long-running txns'), bMid(B2_L, B2_R, 'Replication lag'), bMid(B3_L, B3_R, 'Lock contention'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Error log review'), bMid(B2_L, B2_R, 'Failover procedure'), bMid(B3_L, B3_R, 'I/O bottlenecks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity alerts'), bMid(B2_L, B2_R, 'Maintenance windows'), bMid(B3_L, B3_R, 'Index rebuild'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  WAL          = Write-Ahead Log (PostgreSQL); transaction log; used for replication and PITR'))
    lines.append(txt_row('  Always On AG = SQL Server availability group; synchronous replica; automatic failover capable'))
    lines.append(txt_row('  RMAN         = Oracle Recovery Manager; backup and restore tool for Oracle databases'))
    lines.append(txt_row('  pgBackRest   = PostgreSQL backup tool; supports full/diff/incr; WAL archiving and PITR'))
    lines.append(txt_row('  AWR          = Automatic Workload Repository (Oracle); performance snapshot repository'))
    lines.append(txt_row('  PITR         = Point-In-Time Recovery; restore DB to a specific moment using WAL/log replay'))
    lines.append(txt_row('  Blocking     = Query holding locks that other queries are waiting on; degrades throughput'))
    lines.append(txt_row('  TDE          = Transparent Data Encryption; encrypts DB files at rest; transparent to app'))
    lines.append(txt_row('  Deadlock     = Two transactions each waiting for the other to release locks; DB auto-kills one'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-backup-validation',
    'docs/database/database-backup-validation/index.md',
    'Database backup validation — job status, integrity checks, restore verification',
)
def db_backup_validation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Database — Backup Validation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Confirm database backups are completing successfully and restores work before needed')))
    lines.append(R(bMid(IV_L, IV_R, 'PostgreSQL: pgBackRest info + WAL archiving; MySQL: mysqldump + binary logs')))
    lines.append(R(bMid(IV_L, IV_R, 'SQL Server: RESTORE VERIFYONLY; Oracle: RMAN validate; check agent job history')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup Status Checks'), bMid(B2_L, B2_R, 'Restore Verification'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'pgBackRest: stanza info'), bMid(B2_L, B2_R, 'Restore to test instance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check last backup timestamp'), bMid(B2_L, B2_R, 'Run row count + key queries'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify WAL archiving current'), bMid(B2_L, B2_R, 'RESTORE VERIFYONLY (MSSQL)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SQL Agent job history'), bMid(B2_L, B2_R, 'RMAN validate backupset'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert on missed jobs'), bMid(B2_L, B2_R, 'Document test result'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Platform', 'Check command', 'Restore verify', 'Frequency', 'Alert on'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PostgreSQL', 'pgbackrest info', 'pg_restore test', 'Daily', 'WAL gap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SQL Server', 'Agent job history', 'VERIFY ONLY', 'Daily', 'Job failure'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['MySQL', 'mysqlcheck', 'Restore + query', 'Daily', 'Binlog gap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Oracle', 'RMAN list', 'RMAN validate', 'Daily', 'RMAN failure'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  pgBackRest   = PostgreSQL backup tool; stanza = named backup config for a cluster'))
    lines.append(txt_row('  WAL archiving= PostgreSQL ships WAL segments to archive; gap = missing logs; PITR broken'))
    lines.append(txt_row('  VERIFY ONLY  = SQL Server command; reads backup and validates checksums without restoring'))
    lines.append(txt_row('  RMAN validate= Oracle checks backup set integrity; reports any corrupt blocks found'))
    lines.append(txt_row('  Binary log   = MySQL changelog of every committed transaction; needed for PITR'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-capacity-monitoring',
    'docs/database/database-capacity-monitoring/index.md',
    'Database capacity monitoring — tablespace, log space, growth forecasting',
)
def db_capacity_monitoring():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Database — Capacity Monitoring'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Track database growth, tablespace usage, log space, and forecast expansion needs')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert at 75% usage; plan expansion at 85%; emergency at 90%; autogrow is a safety net')))
    lines.append(R(bMid(IV_L, IV_R, 'Monitor: data files, log files, temp/undo space, index fragmentation, row growth rate')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Current Capacity'), bMid(B2_L, B2_R, 'Growth Forecasting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PG: pg_database_size()'), bMid(B2_L, B2_R, 'Trend: 30/60/90 day growth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MSSQL: sys.dm_db_file_space'), bMid(B2_L, B2_R, 'Forecast to 90% threshold'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MySQL: information_schema'), bMid(B2_L, B2_R, 'Alert: % full + growth rate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Log space: VLF / undo seg'), bMid(B2_L, B2_R, 'Capacity request lead time'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Temp: active session usage'), bMid(B2_L, B2_R, 'Archive + partition old data'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Tablespace   = Named storage container for database objects; monitored per datafile'))
    lines.append(txt_row('  VLF          = Virtual Log File (SQL Server); fragmented log slows backup and recovery'))
    lines.append(txt_row('  Autogrow     = Auto-expand datafile; emergency safety net — not a capacity management plan'))
    lines.append(txt_row('  Undo segment = Oracle/MySQL space for rolled-back transactions; ORA-01555 on shortage'))
    lines.append(txt_row('  pg_database_size= PostgreSQL function returning total size of named database in bytes'))
    lines.append(txt_row('  Partitioning = Split large tables by range/list/hash; move old partitions to cheaper storage'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-failover',
    'docs/database/database-failover/index.md',
    'Database failover — planned and unplanned failover for PostgreSQL, SQL Server, MySQL',
)
def db_failover():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Database — Failover Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Promote standby to primary when primary becomes unavailable or for planned maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-check: confirm failure (not network partition); check replication lag; notify teams')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-failover: update DNS/VIP; rebuild old primary as new standby; monitor replication')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Failover'), bMid(B2_L, B2_R, 'Promote Standby'), bMid(B3_L, B3_R, 'Post-Failover'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm primary down'), bMid(B2_L, B2_R, 'PG: pg_ctl promote'), bMid(B3_L, B3_R, 'Update DNS / VIP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check repl lag/RPO'), bMid(B2_L, B2_R, 'MSSQL: AG failover'), bMid(B3_L, B3_R, 'Notify app teams'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Notify: DBA + app'), bMid(B2_L, B2_R, 'MySQL: STOP REPLICA'), bMid(B3_L, B3_R, 'Validate app login'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify failover method'), bMid(B2_L, B2_R, 'CHANGE REPL SOURCE'), bMid(B3_L, B3_R, 'Rebuild as standby'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Open change ticket'), bMid(B2_L, B2_R, 'Oracle: DG switchover'), bMid(B3_L, B3_R, 'Monitor replication'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Platform', 'Promote cmd', 'DNS update', 'Rebuild cmd', 'RTO estimate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PostgreSQL', 'pg_ctl promote', 'pg_hba + reload', 'pg_rewind', '5-15 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SQL Server', 'AG failover wiz', 'Listener auto', 'Resync replica', '< 30s auto AG'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['MySQL', 'STOP REPLICA', 'Update app DSN', 'CHANGE SOURCE', '5-30 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Oracle', 'DG switchover', 'TNS alias update', 'reinstate', 'DG: < 1 min'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  pg_ctl promote = Promotes PostgreSQL standby to primary; creates recovery.signal removal'))
    lines.append(txt_row('  pg_rewind      = Resync old primary to new primary using WAL; avoids full re-base copy'))
    lines.append(txt_row('  Always On AG   = SQL Server availability group; listener DNS auto-redirects after failover'))
    lines.append(txt_row('  GTID           = MySQL Global Transaction Identifier; simplifies replica reconnect after failover'))
    lines.append(txt_row('  Data Guard     = Oracle HA/DR product; synchronous/async standby; switchover/failover modes'))
    lines.append(txt_row('  Split-brain    = Two nodes both believe they are primary; never promote without fencing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-health-check',
    'docs/database/database-health-check/index.md',
    'Database health check — connections, blocking, long-running queries, error logs',
)
def db_health_check():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Database — Daily Health Check'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Daily DB health: connections, blocking queries, long-running txns, replication, logs')))
    lines.append(R(bMid(IV_L, IV_R, 'Run each morning; alert on blocking > 5 min, connections > 80%, error log entries')))
    lines.append(R(bMid(IV_L, IV_R, 'Document anomalies; escalate blocking chains that cannot be cleared within threshold')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health Check Items'), bMid(B2_L, B2_R, 'Alert Thresholds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active connections vs max'), bMid(B2_L, B2_R, '>80% connection pool = alert'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Blocking chains (head/waiters)'), bMid(B2_L, B2_R, '>5 min block = page DBA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Long-running transactions'), bMid(B2_L, B2_R, '>30 min txn = investigate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Error log: ORA-/FATAL/ERROR'), bMid(B2_L, B2_R, 'Any ORA-600/4031 = P1'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Replication lag check'), bMid(B2_L, B2_R, '>30s lag = investigate'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Blocking chain  = Series of queries waiting on each other; head blocker holds the lock'))
    lines.append(txt_row('  pg_stat_activity= PostgreSQL view; shows all active connections, state, and wait events'))
    lines.append(txt_row('  sys.dm_exec_reqs= SQL Server DMV; lists active requests with wait type and blocking session'))
    lines.append(txt_row('  INFORMATION_SCHEMA= Standard SQL views for connection and schema metadata'))
    lines.append(txt_row('  ORA-600         = Oracle internal error; always escalate; indicates potential corruption'))
    lines.append(txt_row('  Wait event      = Reason a session is not running; categorised by type (I/O, lock, CPU, etc.)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-maintenance',
    'docs/database/database-maintenance/index.md',
    'Database maintenance — index rebuilds, statistics updates, log truncation, scheduled tasks',
)
def db_maintenance():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Database — Maintenance Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Scheduled DB maintenance keeps performance stable and prevents space exhaustion')))
    lines.append(R(bMid(IV_L, IV_R, 'Index maintenance: rebuild (>30% fragmentation) or reorganise (10-30% fragmentation)')))
    lines.append(R(bMid(IV_L, IV_R, 'Run during low-traffic maintenance windows; monitor impact on production workloads')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Index Maintenance'), bMid(B2_L, B2_R, 'Statistics Update'), bMid(B3_L, B3_R, 'Log Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PG: REINDEX TABLE'), bMid(B2_L, B2_R, 'PG: ANALYZE / auto'), bMid(B3_L, B3_R, 'PG: WAL truncation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PG: VACUUM FULL'), bMid(B2_L, B2_R, 'MSSQL: UPDATE STATS'), bMid(B3_L, B3_R, 'MSSQL: DBCC SHRINK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MSSQL: ALTER INDEX'), bMid(B2_L, B2_R, 'MySQL: ANALYZE TABLE'), bMid(B3_L, B3_R, 'MySQL: PURGE BINARY'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check fragmentation'), bMid(B2_L, B2_R, 'Stale stats = bad plan'), bMid(B3_L, B3_R, 'Log backup first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Online vs offline'), bMid(B2_L, B2_R, 'Trigger after bulk load'), bMid(B3_L, B3_R, 'Monitor VLF count'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VACUUM        = PostgreSQL process; reclaims dead row space; VACUUM FULL rewrites table'))
    lines.append(txt_row('  autovacuum    = PostgreSQL background process; runs VACUUM/ANALYZE automatically'))
    lines.append(txt_row('  Fragmentation = Index leaf pages out of order; > 30% triggers REBUILD (full rewrite)'))
    lines.append(txt_row('  REORGANIZE    = Online defrag (SQL Server); moves leaf pages in-place; low-impact'))
    lines.append(txt_row('  Statistics    = Histogram of data distribution; query planner uses them for plan selection'))
    lines.append(txt_row('  VLF           = Virtual Log File (SQL Server); many small VLFs slow log operations'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-perf-ts',
    'docs/database/database-performance-troubleshooting/index.md',
    'Database performance troubleshooting — slow queries, blocking, lock contention, I/O bottlenecks',
)
def db_perf_ts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Database — Performance Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnose DB performance: slow queries, blocking chains, lock contention, I/O saturation')))
    lines.append(R(bMid(IV_L, IV_R, 'Start with wait events to identify bottleneck type before looking at individual queries')))
    lines.append(R(bMid(IV_L, IV_R, 'Use EXPLAIN ANALYZE to confirm query plan; index changes need testing before production')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnose'), bMid(B2_L, B2_R, 'Resolve'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify wait event type'), bMid(B2_L, B2_R, 'Kill blocking head query'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Find top CPU/IO queries'), bMid(B2_L, B2_R, 'Add/rebuild missing index'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'EXPLAIN ANALYZE slow query'), bMid(B2_L, B2_R, 'Rewrite query (avoid N+1)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check index usage/missing'), bMid(B2_L, B2_R, 'Increase work_mem / buffer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review I/O wait on storage'), bMid(B2_L, B2_R, 'Partition or archive data'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'Likely cause', 'Diagnose with', 'Resolution', 'Validate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Slow SELECT', 'Missing index', 'EXPLAIN ANALYZE', 'CREATE INDEX', 'Query time drop'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['High wait', 'Lock contention', 'pg_locks/DMV', 'Kill blocker', 'Wait clears'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['I/O spike', 'Full table scan', 'iostat + EXPLAIN', 'Index + partition', 'I/O normalises'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CPU spike', 'Bad query plan', 'AWR / top SQLs', 'Stats update', 'CPU drops'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Wait event    = Reason a DB session is idle; lock/IO/CPU waits indicate bottleneck type'))
    lines.append(txt_row('  EXPLAIN ANALYZE= PostgreSQL; shows actual execution plan with row counts and timings'))
    lines.append(txt_row('  N+1 problem   = Loop issuing one query per item instead of one bulk query; kills DB'))
    lines.append(txt_row('  work_mem      = PostgreSQL per-sort memory; increase to avoid temp file disk spills'))
    lines.append(txt_row('  DMV           = SQL Server Dynamic Management View; real-time query and session stats'))
    lines.append(txt_row('  Seq scan      = Full table scan; normal for small tables; bad for large + OLTP queries'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'db-replication-check',
    'docs/database/database-replication-check/index.md',
    'Database replication check — lag, sync state, replica health for HA configurations',
)
def db_replication_check():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Database — Replication Check'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Verify replication lag, sync state, and replica health for all HA database pairs')))
    lines.append(R(bMid(IV_L, IV_R, 'PostgreSQL: pg_stat_replication + replication slots; MySQL: SHOW REPLICA STATUS')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert: lag > 30s; replica stopped; WAL slot bloat; disconnected replica')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Replication Status'), bMid(B2_L, B2_R, 'Lag Investigation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PG: pg_stat_replication'), bMid(B2_L, B2_R, 'Check replica I/O load'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PG: pg_replication_slots'), bMid(B2_L, B2_R, 'WAL slot size growing?'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MySQL: SHOW REPLICA STATUS'), bMid(B2_L, B2_R, 'Seconds_Behind_Source'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MSSQL: AG sync state DMV'), bMid(B2_L, B2_R, 'Log send/redo queue size'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Oracle: V$DATAGUARD_STATS'), bMid(B2_L, B2_R, 'DG apply lag metric'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Replication slot  = PostgreSQL object that tracks WAL position for a replica; prevents WAL purge'))
    lines.append(txt_row('  Slot bloat        = Inactive replication slot retaining WAL; can fill disk; drop if unused'))
    lines.append(txt_row('  Seconds_Behind_Source= MySQL metric; seconds replica is behind primary; 0 = caught up'))
    lines.append(txt_row('  Log send queue    = SQL Server AG: bytes of log not yet sent to replica; measures send lag'))
    lines.append(txt_row('  Redo queue        = SQL Server AG: bytes received but not yet applied; measures apply lag'))
    lines.append(txt_row('  Synchronous rep   = Primary waits for replica ACK before committing; zero data loss; slower'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines

# ── Integration ───────────────────────────────────────────────────────────────

@kb_diagram(
    'integration',
    'docs/integration/index.md',
    'Integration landing — API connectivity, certificate trust, directory, email, NTP, SMTP',
)
def integration_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Integration — API, Certificate, Directory, Email & NTP'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Integration references: patterns for connecting infrastructure to shared services')))
    lines.append(R(bMid(IV_L, IV_R, 'Covers: REST API auth, CA trust store setup, LDAP/AD directory, SMTP relay, NTP')))
    lines.append(R(bMid(IV_L, IV_R, 'External connectivity: outbound proxy config, firewall rules, service integration patterns')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity & Certs'), bMid(B2_L, B2_R, 'Network Services'), bMid(B3_L, B3_R, 'App Integrations'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD directory'), bMid(B2_L, B2_R, 'NTP hierarchy'), bMid(B3_L, B3_R, 'ServiceNow CMDB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CA trust stores'), bMid(B2_L, B2_R, 'SMTP relay config'), bMid(B3_L, B3_R, 'Monitoring agents'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'API auth patterns'), bMid(B2_L, B2_R, 'DNS resolution'), bMid(B3_L, B3_R, 'SIEM log forwarding'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS cert install'), bMid(B2_L, B2_R, 'Proxy config'), bMid(B3_L, B3_R, 'Backup agent reg'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML/SSO patterns'), bMid(B2_L, B2_R, 'Firewall rules'), bMid(B3_L, B3_R, 'Ticketing webhooks'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  LDAP         = Lightweight Directory Access Protocol; query AD for user/group membership'))
    lines.append(txt_row('  LDAPS        = LDAP over TLS; use port 636; never send credentials over plain LDAP'))
    lines.append(txt_row('  Trust store  = OS/app certificate store; CA cert must be here for TLS validation to succeed'))
    lines.append(txt_row('  NTP stratum  = Distance from reference clock; stratum 0 = atomic; infra uses stratum 2-3'))
    lines.append(txt_row('  SMTP relay   = Mail server that forwards alerts; authenticated relay prevents open relay abuse'))
    lines.append(txt_row('  mTLS         = Mutual TLS; both sides present certificates; service-to-service auth'))
    lines.append(txt_row('  Proxy        = Outbound HTTP/HTTPS forwarder; set http_proxy env var for CLI tools'))
    lines.append(txt_row('  SAML         = Federated SSO standard; IdP issues assertions; SP trusts them'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-api-connectivity',
    'docs/integration/api-connectivity/index.md',
    'API connectivity — testing REST API endpoints, authentication, TLS certificate validation',
)
def int_api_connectivity():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Integration — API Connectivity'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Test REST API connectivity: reachability, authentication, TLS cert chain, response codes')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth types: API key (header), Bearer token (OAuth2/JWT), Basic (base64), mTLS cert')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS: verify cert chain with curl -v; check expiry; confirm CA in trust store')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connectivity Testing'), bMid(B2_L, B2_R, 'Common Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'curl -v https://endpoint'), bMid(B2_L, B2_R, 'SSL: unable to verify → add CA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'curl -H "Authorization: Bearer"'), bMid(B2_L, B2_R, '401 = bad token or expired'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'openssl s_client -connect'), bMid(B2_L, B2_R, '403 = auth OK; no permission'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check cert expiry (s_client)'), bMid(B2_L, B2_R, '502/504 = upstream timeout'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test via proxy: curl --proxy'), bMid(B2_L, B2_R, 'Connection refused = FW/DNS'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Bearer token   = Short-lived JWT or opaque token; sent in Authorization: Bearer <token>'))
    lines.append(txt_row('  OAuth2         = Delegation framework; client obtains token from IdP; presents to API'))
    lines.append(txt_row('  mTLS           = Mutual TLS; both client and server authenticate with certificates'))
    lines.append(txt_row('  SNI            = Server Name Indication; TLS extension; server selects correct cert by hostname'))
    lines.append(txt_row('  HTTP 401       = Unauthorized; credentials missing or invalid; re-authenticate'))
    lines.append(txt_row('  HTTP 403       = Forbidden; authenticated but not authorised for the resource'))
    lines.append(txt_row('  openssl s_client= Test TLS handshake; shows cert chain, expiry, cipher negotiated'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-cert-trust',
    'docs/integration/certificate-trust/index.md',
    'Certificate trust — adding CA certificates to trust stores on Linux, Windows, appliances',
)
def int_cert_trust():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Integration — Certificate Trust'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Add CA certificates to trust stores so TLS connections to internal services succeed')))
    lines.append(R(bMid(IV_L, IV_R, 'Linux: copy .crt to /etc/pki/ca-trust/source/anchors/ then update-ca-trust')))
    lines.append(R(bMid(IV_L, IV_R, 'Windows: import to Trusted Root CA store; deploy via GPO for domain machines')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux Trust Store'), bMid(B2_L, B2_R, 'Windows & Appliances'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RHEL: /etc/pki/ca-trust/'), bMid(B2_L, B2_R, 'MMC → Cert snap-in → import'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ubuntu: /usr/local/share/ca/'), bMid(B2_L, B2_R, 'GPO: Computer Config → Certs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'update-ca-trust (RHEL)'), bMid(B2_L, B2_R, 'Appliance: upload via UI/API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'update-ca-certificates (Deb)'), bMid(B2_L, B2_R, 'Java: keytool -import'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify: curl https://internal'), bMid(B2_L, B2_R, 'Test: curl / PowerShell Invoke'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Platform', 'CA store path', 'Add command', 'Verify', 'Scope'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['RHEL/CentOS', '/etc/pki/anchors', 'update-ca-trust', 'curl https://', 'System-wide'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Ubuntu/Debian', '/usr/local/share', 'update-ca-certs', 'curl https://', 'System-wide'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Windows', 'Trusted Root CA', 'certlm.msc/GPO', 'IE/Edge/curl', 'Machine store'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Java apps', 'JRE cacerts', 'keytool -import', 'Java HTTPS call', 'JVM-scoped'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Root CA      = Top of certificate chain; self-signed; must be in trust store for chain to verify'))
    lines.append(txt_row('  Intermediate = Signed by Root CA; signs end-entity certs; must be in cert bundle sent by server'))
    lines.append(txt_row('  update-ca-trust= RHEL command; rebuilds the consolidated trust bundle from source anchors'))
    lines.append(txt_row('  keytool      = Java utility; manages JVM trust store (cacerts); import with -importcert'))
    lines.append(txt_row('  GPO          = Group Policy Object; deploys CA cert to all domain machines automatically'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-directory-integration',
    'docs/integration/directory-integration/index.md',
    'Directory integration — LDAP/LDAPS with Active Directory for auth and group membership',
)
def int_directory_integration():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Integration — Directory Integration (LDAP / Active Directory)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Integrate infrastructure services with Active Directory via LDAPS for authentication')))
    lines.append(R(bMid(IV_L, IV_R, 'Service account: dedicated bind account; read-only to OU; password rotation tracked')))
    lines.append(R(bMid(IV_L, IV_R, 'Required: LDAPS (port 636) only; import AD CA cert; test bind before production')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP Config'), bMid(B2_L, B2_R, 'Troubleshooting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Server: DC IP or FQDN'), bMid(B2_L, B2_R, 'ldapsearch bind test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port: 636 (LDAPS)'), bMid(B2_L, B2_R, 'Check CA in trust store'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bind DN: svc-ldap@domain'), bMid(B2_L, B2_R, 'Verify service acct not locked'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Base DN: DC=corp,DC=local'), bMid(B2_L, B2_R, 'Check OU search permissions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Group filter: memberOf'), bMid(B2_L, B2_R, 'AD event log: 4771/4776'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Bind DN      = Distinguished Name of service account used to authenticate to LDAP'))
    lines.append(txt_row('  Base DN      = Search root in directory tree; e.g. DC=corp,DC=local for full domain'))
    lines.append(txt_row('  LDAPS        = LDAP over TLS port 636; required; plain LDAP (389) transmits creds in clear'))
    lines.append(txt_row('  memberOf     = AD attribute listing group DNs; used for group-based role mapping'))
    lines.append(txt_row('  ldapsearch   = CLI tool to test LDAP queries; confirm bind and attribute retrieval'))
    lines.append(txt_row('  Event 4776   = AD credential validation attempt; logged on DC; useful for bind failures'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-email-relay',
    'docs/integration/email-relay/index.md',
    'Email relay — SMTP relay config for infrastructure alerts, monitoring notifications, appliances',
)
def int_email_relay():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Integration — Email Relay (SMTP)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Configure SMTP relay so monitoring, backup, and infrastructure appliances send email')))
    lines.append(R(bMid(IV_L, IV_R, 'Use authenticated SMTP relay; never configure an open relay; TLS required')))
    lines.append(R(bMid(IV_L, IV_R, 'Test: telnet/openssl to relay port; send a test alert after config change')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SMTP Config'), bMid(B2_L, B2_R, 'Common Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Relay host: smtp.internal'), bMid(B2_L, B2_R, 'Connection refused = FW/port'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port: 587 (STARTTLS)'), bMid(B2_L, B2_R, 'Auth fail = check creds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auth: PLAIN or LOGIN'), bMid(B2_L, B2_R, 'TLS error = add relay CA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'From: alerts@domain'), bMid(B2_L, B2_R, 'Relay denied = check allow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test: send test mail'), bMid(B2_L, B2_R, 'SPF fail = add relay IP'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  STARTTLS     = Upgrade plain SMTP connection to TLS on port 587; required for auth'))
    lines.append(txt_row('  Open relay   = SMTP server accepting mail for any domain; used for spam; never configure'))
    lines.append(txt_row('  SPF          = Sender Policy Framework; DNS TXT record listing authorised sending IPs'))
    lines.append(txt_row('  Port 25      = SMTP; blocked by most cloud providers for outbound; use 587 or 465'))
    lines.append(txt_row('  Port 587     = Submission port; requires authentication; preferred for relay config'))
    lines.append(txt_row('  Relay allow  = List of IPs permitted to relay through SMTP server without auth (use sparingly)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-external-connectivity',
    'docs/integration/external-connectivity/index.md',
    'External connectivity — outbound internet access, proxy config, firewall rule documentation',
)
def int_external_connectivity():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Integration — External Connectivity'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Outbound internet access: proxy config, allowed destinations, firewall rule requests')))
    lines.append(R(bMid(IV_L, IV_R, 'Proxy: set http_proxy/https_proxy env vars; add no_proxy for internal subnets')))
    lines.append(R(bMid(IV_L, IV_R, 'Document all outbound FW rules: source, destination, port, protocol, business justification')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy Configuration'), bMid(B2_L, B2_R, 'Firewall Rule Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'http_proxy=http://proxy:3128'), bMid(B2_L, B2_R, 'Request: src/dst/port/proto'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'https_proxy same value'), bMid(B2_L, B2_R, 'Business justification reqd'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'no_proxy=.internal,10.0.0.0/8'), bMid(B2_L, B2_R, 'Change ticket + approval'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'yum/apt: proxy in config'), bMid(B2_L, B2_R, 'Test after implementation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Container: env in compose'), bMid(B2_L, B2_R, 'Annual rule review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  http_proxy   = Environment variable; tool (curl, yum, apt) uses this for HTTP connections'))
    lines.append(txt_row('  no_proxy     = Comma-separated list of hosts/CIDRs to bypass proxy; add all internal ranges'))
    lines.append(txt_row('  Egress rule  = Outbound firewall rule; controls what the server can connect to externally'))
    lines.append(txt_row('  FQDN filter  = Firewall rules by hostname instead of IP; needs DNS-aware inspection'))
    lines.append(txt_row('  Transparent proxy= Intercepts traffic without client config; needs CA cert for HTTPS inspection'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-service-integrations',
    'docs/integration/service-integrations/index.md',
    'Service integrations — ServiceNow, monitoring, backup, SIEM integration patterns',
)
def int_service_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Integration — Service Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Patterns for integrating infrastructure components with ITSM, monitoring, backup, SIEM')))
    lines.append(R(bMid(IV_L, IV_R, 'Typically via: REST API (webhook/poll), SNMP traps, syslog, agent, or file export')))
    lines.append(R(bMid(IV_L, IV_R, 'Use dedicated service accounts; minimal scope; rotate credentials on schedule')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM (ServiceNow)'), bMid(B2_L, B2_R, 'Monitoring'), bMid(B3_L, B3_R, 'Security (SIEM)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB CI sync'), bMid(B2_L, B2_R, 'SNMP trap receiver'), bMid(B3_L, B3_R, 'Syslog forwarding'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Incident auto-create'), bMid(B2_L, B2_R, 'Agent (Zabbix/NR)'), bMid(B3_L, B3_R, 'CEF / JSON events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change feed webhook'), bMid(B2_L, B2_R, 'REST API polling'), bMid(B3_L, B3_R, 'API key for ingest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MID Server for on-prem'), bMid(B2_L, B2_R, 'Alert routing rules'), bMid(B3_L, B3_R, 'TLS syslog (port 6514)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test: CI creation flow'), bMid(B2_L, B2_R, 'Test: send test trap'), bMid(B3_L, B3_R, 'Test: logger command'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  MID Server    = ServiceNow component that runs on-prem; proxies API calls to instance'))
    lines.append(txt_row('  SNMP trap     = Unsolicited alert from device to monitoring; receiver must be configured'))
    lines.append(txt_row('  CEF           = Common Event Format; Syslog header + key=value pairs; standard SIEM intake'))
    lines.append(txt_row('  Syslog/514    = UDP syslog; no guarantee of delivery; TLS syslog (6514) preferred'))
    lines.append(txt_row('  Webhook       = HTTP callback; source POSTs event payload to receiver URL on trigger'))
    lines.append(txt_row('  API key scope = Limit API key to minimum permissions; rotate annually or on staff change'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'int-time-sync',
    'docs/integration/time-synchronization/index.md',
    'Time synchronization — NTP hierarchy, stratum config, drift troubleshooting across platforms',
)
def int_time_sync():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Integration — Time Synchronization (NTP)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Accurate time is critical: Kerberos (5 min skew max), TLS certs, log correlation')))
    lines.append(R(bMid(IV_L, IV_R, 'Hierarchy: external NTP (stratum 1/2) → internal NTP servers → all infra clients')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert: offset > 100ms; drift > 50ms/s; stratum 16 = unsynchronised = investigate')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NTP Config'), bMid(B2_L, B2_R, 'Troubleshooting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Linux: /etc/chrony.conf'), bMid(B2_L, B2_R, 'chronyc tracking (offset)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Windows: w32tm /config'), bMid(B2_L, B2_R, 'timedatectl status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ESXi: host NTP config'), bMid(B2_L, B2_R, 'w32tm /query /status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Appliance: NTP server in UI'), bMid(B2_L, B2_R, 'Stratum 16 = no sync'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Firewall: UDP 123 to NTP'), bMid(B2_L, B2_R, 'Check FW UDP 123 open'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Stratum      = Distance from reference clock; 0 = atomic; infra uses stratum 2-3'))
    lines.append(txt_row('  Offset       = Difference between client time and server time; < 100ms is normal'))
    lines.append(txt_row('  Drift        = Rate at which clock gains/loses time; chrony compensates automatically'))
    lines.append(txt_row('  Stratum 16   = NTP "not synchronised" state; Kerberos will fail within 5 min'))
    lines.append(txt_row('  chronyc      = Chrony client tool; tracking, sources, makestep commands'))
    lines.append(txt_row('  w32tm        = Windows NTP tool; /query /status shows source, stratum, offset'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Inventory ─────────────────────────────────────────────────────────────────

@kb_diagram(
    'inventory',
    'docs/inventory/index.md',
    'Inventory landing — asset tracking, CMDB, environment mapping, lifecycle, licenses',
)
def inventory_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Inventory — Asset Tracking, CMDB, Lifecycle & License Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory: know what assets exist, their state, owners, location, and support status')))
    lines.append(R(bMid(IV_L, IV_R, 'CMDB: track CI relationships and change history; feeds incident and change processes')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: EOL dates drive refresh planning; licence counts prevent compliance gaps')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Asset & Config'), bMid(B2_L, B2_R, 'Lifecycle'), bMid(B3_L, B3_R, 'Licenses & Contracts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hardware asset reg'), bMid(B2_L, B2_R, 'EOL/EOS tracking'), bMid(B3_L, B3_R, 'License inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB CI records'), bMid(B2_L, B2_R, 'Refresh planning'), bMid(B3_L, B3_R, 'Compliance count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Environment mapping'), bMid(B2_L, B2_R, 'Decommission proc'), bMid(B3_L, B3_R, 'Renewal calendar'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'System inventory'), bMid(B2_L, B2_R, 'Migration tracking'), bMid(B3_L, B3_R, 'Vendor contacts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack/rack-unit map'), bMid(B2_L, B2_R, 'HW lifecycle state'), bMid(B3_L, B3_R, 'Support levels'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CMDB         = Configuration Management Database; stores CIs and their relationships'))
    lines.append(txt_row('  CI           = Configuration Item; any asset tracked in CMDB with attributes and relations'))
    lines.append(txt_row('  EOL          = End of Life; vendor no longer sells the product; EOS = end of support'))
    lines.append(txt_row('  Asset register= Authoritative list of all hardware: serial, location, owner, lifecycle state'))
    lines.append(txt_row('  Refresh plan = Scheduled replacement of assets approaching EOL; budgeted in advance'))
    lines.append(txt_row('  SAM          = Software Asset Management; tracks licence entitlements vs actual usage'))
    lines.append(txt_row('  Support contract= Vendor SLA for hardware; coverage level (NBD/4h/24x7); expiry date'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-asset-tracking',
    'docs/inventory/asset-tracking/index.md',
    'Asset tracking — hardware register, serial numbers, rack locations, owners, lifecycle state',
)
def inv_asset_tracking():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Inventory — Asset Tracking'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Hardware asset register: serial number, rack location, owner, function, lifecycle state')))
    lines.append(R(bMid(IV_L, IV_R, 'Update register at: receipt, rack/decommission, ownership change, support change')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: reconcile physical assets against register quarterly; investigate discrepancies')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register Attributes'), bMid(B2_L, B2_R, 'Lifecycle States'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hostname + IP address'), bMid(B2_L, B2_R, 'Ordered: PO raised'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Serial number + model'), bMid(B2_L, B2_R, 'In use: active production'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack / rack unit / DC'), bMid(B2_L, B2_R, 'Maintenance: in repair'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Owner + cost centre'), bMid(B2_L, B2_R, 'EOL: past support end'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Support contract ref'), bMid(B2_L, B2_R, 'Decommissioned: retired'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Field', 'Example', 'Source of truth', 'Updated when', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Serial', 'SVC-12345X', 'Vendor label', 'On receipt', 'Asset team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Rack loc', 'DC1-A01-U14', 'DCIM tool', 'On install', 'DC ops'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Lifecycle', 'Active/EOL', 'CMDB + register', 'On change', 'Asset team'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DCIM         = Data Centre Infrastructure Management tool; tracks rack/power/cooling'))
    lines.append(txt_row('  Rack unit    = 1U = 44.45 mm height; standard measure for data centre rack space'))
    lines.append(txt_row('  Cost centre  = Finance code; determines which team is billed for the asset'))
    lines.append(txt_row('  Asset audit  = Physical reconciliation of assets against register; finds ghost/missing assets'))
    lines.append(txt_row('  Ghost asset  = Asset in register that no longer physically exists; arises from poor process'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-config-management',
    'docs/inventory/configuration-management/index.md',
    'Configuration management — CMDB structure, CI relationships, lifecycle, change linkage',
)
def inv_config_management():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Inventory — Configuration Management (CMDB)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CMDB: central record of CIs (hardware, software, services) and their relationships')))
    lines.append(R(bMid(IV_L, IV_R, 'CI relationships: server hosts VM → VM runs app → app depends on DB; impact analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Change linkage: every change ticket updates affected CI state; audit trail in CMDB')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CI Attributes'), bMid(B2_L, B2_R, 'CI Relationships'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Name, class, owner'), bMid(B2_L, B2_R, 'Hosts / hosted on'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Status (active/retired)'), bMid(B2_L, B2_R, 'Depends on / used by'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Location, environment'), bMid(B2_L, B2_R, 'Connects to / cluster'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OS, software version'), bMid(B2_L, B2_R, 'Impact analysis path'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change/incident links'), bMid(B2_L, B2_R, 'Business service map'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CI           = Configuration Item; any entity tracked in CMDB with attributes and history'))
    lines.append(txt_row('  CI class     = Type of CI (Server, VM, Application, Network Device, Database, etc.)'))
    lines.append(txt_row('  Relationship = Typed link between CIs; powers impact analysis and dependency maps'))
    lines.append(txt_row('  Impact analysis= Determine what is affected by a CI failure or change using relationships'))
    lines.append(txt_row('  Discovery    = Automated CMDB population from network scanning or cloud APIs'))
    lines.append(txt_row('  Reconciliation= Compare discovered data vs CMDB; find stale or missing records'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-environment-mapping',
    'docs/inventory/environment-mapping/index.md',
    'Environment mapping — prod/non-prod/DR environment dependencies and data flow',
)
def inv_environment_mapping():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Inventory — Environment Mapping'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment map: production, staging, dev, DR — document dependencies and data flows')))
    lines.append(R(bMid(IV_L, IV_R, 'Identify: shared services (AD, DNS, NTP) vs environment-specific (app, DB, storage)')))
    lines.append(R(bMid(IV_L, IV_R, 'DR site must mirror prod sizing; test failover path; document RTO/RPO per service')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Production'), bMid(B2_L, B2_R, 'Non-Production'), bMid(B3_L, B3_R, 'DR / Recovery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Live workloads'), bMid(B2_L, B2_R, 'Staging mirrors prod'), bMid(B3_L, B3_R, 'Replication target'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change managed'), bMid(B2_L, B2_R, 'Dev = isolated'), bMid(B3_L, B3_R, 'Tested annually'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitored 24/7'), bMid(B2_L, B2_R, 'No prod data in dev'), bMid(B3_L, B3_R, 'RTO/RPO defined'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLA enforced'), bMid(B2_L, B2_R, 'Refresh from prod'), bMid(B3_L, B3_R, 'Activation runbook'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access controlled'), bMid(B2_L, B2_R, 'Config parity check'), bMid(B3_L, B3_R, 'Config in sync'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Config parity = Staging config matches prod (versions, settings) for realistic testing'))
    lines.append(txt_row('  Data masking  = Replace prod PII with synthetic data before copying to non-prod environments'))
    lines.append(txt_row('  Shared service= Component used across environments (AD, DNS, NTP); single point of attention'))
    lines.append(txt_row('  Blast radius  = Scope of impact if an environment fails; keep prod isolated from dev'))
    lines.append(txt_row('  DR activation = Switch workloads to DR site; requires tested runbook and communications plan'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-hardware-lifecycle',
    'docs/inventory/hardware-lifecycle/index.md',
    'Hardware lifecycle — EOL tracking, refresh planning, decommission, vendor support timelines',
)
def inv_hardware_lifecycle():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Inventory — Hardware Lifecycle'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Track hardware from purchase through active use to end-of-life and decommission')))
    lines.append(R(bMid(IV_L, IV_R, 'EOL: no more patches; EOSL: no more support calls — both require replacement plan')))
    lines.append(R(bMid(IV_L, IV_R, 'Refresh: budget cycle (18-24 months lead); decommission: secure wipe + disposal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lifecycle Phases'), bMid(B2_L, B2_R, 'EOL/Refresh Actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plan: spec + budget'), bMid(B2_L, B2_R, 'Query vendor EOL dates'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Procure: PO + delivery'), bMid(B2_L, B2_R, 'Flag 18-month warning'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deploy: rack + config'), bMid(B2_L, B2_R, 'Raise refresh project'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Operate: maintain + patch'), bMid(B2_L, B2_R, 'Migrate workloads first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Decommission: wipe + retire'), bMid(B2_L, B2_R, 'Secure wipe certificate'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  EOL      = End of Life; vendor stops selling and developing the product'))
    lines.append(txt_row('  EOSL     = End of Service Life; vendor stops providing support and security patches'))
    lines.append(txt_row('  Refresh  = Replace ageing hardware with current generation before EOSL'))
    lines.append(txt_row('  Secure wipe= Cryptographic erasure or DoD overwrite before disposal to prevent data recovery'))
    lines.append(txt_row('  ITAD     = IT Asset Disposition; certified disposal with chain-of-custody and destruction cert'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-license-management',
    'docs/inventory/license-management/index.md',
    'License management — software inventory, compliance tracking, renewals, consumption monitoring',
)
def inv_license_management():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Inventory — License Management'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Track software licence entitlements vs actual usage to maintain compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'Types: per-socket, per-core, per-user, subscription, concurrent; each has different count')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: compare entitlements to discovered installations; renew 60 days before expiry')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licence Register'), bMid(B2_L, B2_R, 'Compliance Checks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Product + version'), bMid(B2_L, B2_R, 'Entitlement vs usage'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licence type + count'), bMid(B2_L, B2_R, 'Discovery scan (SCCM)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expiry + renewal date'), bMid(B2_L, B2_R, 'Alert: < 20% headroom'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Purchase order ref'), bMid(B2_L, B2_R, 'Quarterly audit cycle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vendor + contact'), bMid(B2_L, B2_R, 'Reclaim unused licences'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Entitlement  = Number or type of licences purchased; documented by purchase order + cert'))
    lines.append(txt_row('  Per-socket   = Licence per physical CPU socket; common for server OS and hypervisors'))
    lines.append(txt_row('  Per-core     = Licence per CPU core; Microsoft SQL Server uses this model'))
    lines.append(txt_row('  Subscription = Time-limited licence; expires on date; must renew or lose access'))
    lines.append(txt_row('  Compliance gap= Installed instances exceed entitlements; vendor audit risk'))
    lines.append(txt_row('  SCCM         = Microsoft System Center; discovers installed software for licence counting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-support-contracts',
    'docs/inventory/support-contracts/index.md',
    'Support contracts — coverage levels, expiry dates, escalation contacts, vendor SLAs',
)
def inv_support_contracts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Inventory — Support Contracts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Vendor support contract register: coverage level, expiry dates, escalation contacts')))
    lines.append(R(bMid(IV_L, IV_R, 'Know before an incident: contract number, support level, and how to open a P1 case')))
    lines.append(R(bMid(IV_L, IV_R, 'Renew 90 days before expiry; lapsed support = no access to updates or TAC')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register Fields'), bMid(B2_L, B2_R, 'Support Levels'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Contract / case number'), bMid(B2_L, B2_R, 'NBD: next business day'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vendor + product'), bMid(B2_L, B2_R, '4h: 4-hour onsite parts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Coverage level'), bMid(B2_L, B2_R, '24x7x4: critical SLA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expiry date'), bMid(B2_L, B2_R, 'Software: patch + TAC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TAC contact number'), bMid(B2_L, B2_R, 'Premier: named support'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Level', 'Parts SLA', 'Support hours', 'Patch access', 'Use case'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['NBD', 'Next bus day', 'Business hours', 'Yes', 'Non-critical'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['4h onsite', '4 hours', '24x7', 'Yes', 'Business crit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['24x7x4', '4h + onsite', '24x7x365', 'Yes', 'Mission crit'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  TAC          = Technical Assistance Centre; vendor support portal for raising cases'))
    lines.append(txt_row('  NBD          = Next Business Day; parts dispatched by end of next working day'))
    lines.append(txt_row('  EOSL         = End of Service Life; after this date, contract cannot be renewed'))
    lines.append(txt_row('  Case number  = Reference for a support incident; keep for escalation and follow-up'))
    lines.append(txt_row('  SLA breach   = Vendor misses response time; escalate to account manager immediately'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'inv-system-inventory',
    'docs/inventory/system-inventory/index.md',
    'System inventory — server, VM, appliance inventory with hostname, IP, OS version, function',
)
def inv_system_inventory():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Inventory — System Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Server, VM, and appliance inventory: hostname, IP, OS version, owner, function')))
    lines.append(R(bMid(IV_L, IV_R, 'Use for: change impact scoping, patching campaigns, DR planning, capacity review')))
    lines.append(R(bMid(IV_L, IV_R, 'Keep current: discovery scan monthly; audit reconcile quarterly; decommission promptly')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inventory Fields'), bMid(B2_L, B2_R, 'Maintenance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hostname (FQDN)'), bMid(B2_L, B2_R, 'Discovery scan monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IP address (v4/v6)'), bMid(B2_L, B2_R, 'Reconcile vs CMDB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OS / version / patch'), bMid(B2_L, B2_R, 'Update on OS change'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Function / role'), bMid(B2_L, B2_R, 'Archive decommissioned'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Environment + owner'), bMid(B2_L, B2_R, 'Flag unpatched systems'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FQDN         = Fully Qualified Domain Name; hostname + domain; needed for cert and DNS'))
    lines.append(txt_row('  Discovery    = Automated scan (Nmap, SCCM, vCenter) to find all active systems'))
    lines.append(txt_row('  Ghost system = System in inventory that no longer exists; remove after confirmation'))
    lines.append(txt_row('  Patch level  = OS patch currency; inventory identifies systems behind patch baseline'))
    lines.append(txt_row('  Role tag     = System function label (web, db, backup, infra); used for change scoping'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines

# ── Performance ───────────────────────────────────────────────────────────────

@kb_diagram(
    'performance',
    'docs/performance/index.md',
    'Performance landing — capacity planning, baselining, reliability engineering, SLOs',
)
def performance_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Performance — Capacity, Baselining, Reliability & SLOs'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Performance management: baseline current state → monitor trends → plan capacity →')))
    lines.append(R(bMid(IV_L, IV_R, 'optimise resource usage → test failure modes → measure availability against SLOs')))
    lines.append(R(bMid(IV_L, IV_R, 'SLOs translate business expectations into measurable infra targets with error budgets')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity & Baseline'), bMid(B2_L, B2_R, 'Optimisation'), bMid(B3_L, B3_R, 'SLO & Reliability'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance baseline'), bMid(B2_L, B2_R, 'Right-size VMs'), bMid(B3_L, B3_R, 'SLO definition'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity forecasting'), bMid(B2_L, B2_R, 'Reclaim idle storage'), bMid(B3_L, B3_R, 'Error budget'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trend analysis'), bMid(B2_L, B2_R, 'Network QoS'), bMid(B3_L, B3_R, 'MTTR / MTBF'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alerting on growth'), bMid(B2_L, B2_R, 'Storage tiering'), bMid(B3_L, B3_R, 'Availability calc'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resource headroom'), bMid(B2_L, B2_R, 'Failure testing'), bMid(B3_L, B3_R, 'SLA reporting'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SLO          = Service Level Objective; target for availability/latency/error rate'))
    lines.append(txt_row('  SLA          = Service Level Agreement; contractual commitment, usually above SLOs'))
    lines.append(txt_row('  SLI          = Service Level Indicator; the metric measured (e.g. request success rate)'))
    lines.append(txt_row('  Error budget  = Allowable downtime before SLO is breached; consumed by incidents'))
    lines.append(txt_row('  MTTR         = Mean Time To Recover; average incident duration; lower is better'))
    lines.append(txt_row('  MTBF         = Mean Time Between Failures; average uptime between incidents'))
    lines.append(txt_row('  Baseline     = Normal performance values for a system; deviations trigger investigation'))
    lines.append(txt_row('  Right-sizing = Match VM/instance resources to actual usage; remove over-provisioning'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-capacity-forecasting',
    'docs/performance/capacity-forecasting/index.md',
    'Capacity forecasting — projecting compute, storage, network from trend data',
)
def perf_capacity_forecasting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Capacity Forecasting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Project future capacity needs from historical growth trends for compute/storage/network')))
    lines.append(R(bMid(IV_L, IV_R, 'Collect 90-day trend data; extrapolate to 12/18/24 month horizon; add headroom buffer')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert at 75% usage; plan procurement at 80%; never operate above 90% sustained')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Metrics to Forecast'), bMid(B2_L, B2_R, 'Forecast Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU: peak + average util %'), bMid(B2_L, B2_R, 'Collect 90-day history'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAM: committed vs balloon'), bMid(B2_L, B2_R, 'Calculate growth rate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage: used + growth/month'), bMid(B2_L, B2_R, 'Extrapolate to 12/24 mo'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network: peak bandwidth %'), bMid(B2_L, B2_R, 'Add 20% headroom buffer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM count + density ratio'), bMid(B2_L, B2_R, 'Raise procurement request'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Headroom     = Buffer above projected peak; allows for spikes and unplanned growth'))
    lines.append(txt_row('  Balloon mem  = VMware memory balloon driver; reclaims VM memory under host pressure'))
    lines.append(txt_row('  Growth rate  = Measured increase per month/quarter; used to project future consumption'))
    lines.append(txt_row('  Procurement lead = Time from request to delivered capacity; plan 3-6 months ahead'))
    lines.append(txt_row('  Overcommit   = Allocating more vCPU/RAM than physical; acceptable with headroom tracking'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-failure-testing',
    'docs/performance/failure-testing/index.md',
    'Failure testing — chaos engineering and fault injection for validating HA and DR',
)
def perf_failure_testing():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Failure Testing'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Failure testing: deliberately inject faults to verify HA and DR actually work')))
    lines.append(R(bMid(IV_L, IV_R, 'Test in isolation first; graduate to production with maintenance window and rollback')))
    lines.append(R(bMid(IV_L, IV_R, 'Document hypothesis, expected result, actual result, and any gaps found')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test Types'), bMid(B2_L, B2_R, 'Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node/host failure (power off)'), bMid(B2_L, B2_R, 'Define hypothesis'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network partition test'), bMid(B2_L, B2_R, 'Raise change ticket'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage path failure'), bMid(B2_L, B2_R, 'Inject fault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service kill / crash'), bMid(B2_L, B2_R, 'Measure RTO actual'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resource exhaustion'), bMid(B2_L, B2_R, 'Document gaps found'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Chaos engineering= Deliberate fault injection to reveal weaknesses before they cause incidents'))
    lines.append(txt_row('  Game day       = Scheduled failure testing exercise; all stakeholders notified; results shared'))
    lines.append(txt_row('  Blast radius   = Scope of failure; limit during tests by isolating to one component'))
    lines.append(txt_row('  Steady state   = Known-good performance baseline before fault injection begins'))
    lines.append(txt_row('  Rollback       = Restore normal state after test; documented before injection starts'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-baselining',
    'docs/performance/performance-baselining/index.md',
    'Performance baselining — establishing compute, storage, network baselines before changes',
)
def perf_baselining():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Baselining'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Baseline: capture normal performance before a change so deviations are detectable')))
    lines.append(R(bMid(IV_L, IV_R, 'Capture during representative load: peak business hours over 5-7 days minimum')))
    lines.append(R(bMid(IV_L, IV_R, 'Store baselines in monitoring platform; compare post-change and post-incident')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Metrics to Baseline'), bMid(B2_L, B2_R, 'Baseline Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU: avg, peak, p95'), bMid(B2_L, B2_R, 'Collect 7-day window'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Memory: used, swap, balloon'), bMid(B2_L, B2_R, 'Include peak business hrs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage: IOPS, latency, tput'), bMid(B2_L, B2_R, 'Export to spreadsheet/TSDB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network: bps, pps, errors'), bMid(B2_L, B2_R, 'Tag with date + event'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App: response time, TPS'), bMid(B2_L, B2_R, 'Compare after change'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  p95 / p99    = 95th/99th percentile; shows tail latency; better than average for SLOs'))
    lines.append(txt_row('  IOPS         = Input/Output Operations Per Second; key storage performance metric'))
    lines.append(txt_row('  Throughput   = Data volume per second (MB/s); different from IOPS; both matter'))
    lines.append(txt_row('  TSDB         = Time Series Database (e.g. Prometheus, InfluxDB); stores metric history'))
    lines.append(txt_row('  Deviation    = Metric outside normal range; signals regression or capacity issue'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-reliability-engineering',
    'docs/performance/reliability-engineering/index.md',
    'Reliability engineering — MTTR/MTBF tracking, failure mode analysis, reliability improvement',
)
def perf_reliability_engineering():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Reliability Engineering'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Reliability engineering: measure, track, and improve system dependability over time')))
    lines.append(R(bMid(IV_L, IV_R, 'MTTR: reduce by improving detection, runbooks, and automation of recovery steps')))
    lines.append(R(bMid(IV_L, IV_R, 'MTBF: improve by eliminating failure causes via root cause analysis and hardening')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Metrics'), bMid(B2_L, B2_R, 'Improvement Actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MTTR per service'), bMid(B2_L, B2_R, 'Automate detection (alerts)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MTBF per service'), bMid(B2_L, B2_R, 'Improve runbook quality'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Availability %'), bMid(B2_L, B2_R, 'RCA + corrective actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Incident frequency'), bMid(B2_L, B2_R, 'Eliminate repeat failures'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change failure rate'), bMid(B2_L, B2_R, 'Improve test coverage'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  MTTR         = Mean Time To Recover; total incident downtime / number of incidents'))
    lines.append(txt_row('  MTBF         = Mean Time Between Failures; total uptime / number of failures'))
    lines.append(txt_row('  Availability = (MTBF / (MTBF + MTTR)) * 100%; four nines = 99.99% = ~52 min/yr'))
    lines.append(txt_row('  Change fail rate= % of changes causing incidents; target < 5% per DORA metrics'))
    lines.append(txt_row('  FMEA         = Failure Mode and Effects Analysis; proactive failure scenario assessment'))
    lines.append(txt_row('  Toil         = Repetitive manual work; automate to reduce MTTR and operator error'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-resource-optimization',
    'docs/performance/resource-optimization/index.md',
    'Resource optimization — right-sizing VMs, reclaiming storage, reducing idle resource consumption',
)
def perf_resource_optimization():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Resource Optimisation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Optimisation: identify over-provisioned or idle resources and reduce waste')))
    lines.append(R(bMid(IV_L, IV_R, 'Right-size VMs using 30-day p95 CPU/RAM; reclaim unused storage and old snapshots')))
    lines.append(R(bMid(IV_L, IV_R, 'Test right-sizing in non-prod first; communicate with app owner before production change')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify Waste'), bMid(B2_L, B2_R, 'Reclaim Actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU < 10% avg: oversized'), bMid(B2_L, B2_R, 'Reduce vCPU count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAM < 20% used: oversized'), bMid(B2_L, B2_R, 'Reduce vRAM allocation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshots > 7 days old'), bMid(B2_L, B2_R, 'Delete old snapshots'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Powered-off VMs > 30 days'), bMid(B2_L, B2_R, 'Decommission or archive'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Unused datastores/LUNs'), bMid(B2_L, B2_R, 'Reclaim after confirm'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Right-sizing = Match vCPU/vRAM to actual workload demand; reduces host overcommit ratio'))
    lines.append(txt_row('  vCPU ratio   = Total vCPUs assigned / physical cores; > 4:1 can cause CPU ready contention'))
    lines.append(txt_row('  Balloon      = VMware memory reclaim driver; active balloon means host is under memory pressure'))
    lines.append(txt_row('  Thin-prov    = Disk allocated lazily; reclaim by deleting data and running a reclaim task'))
    lines.append(txt_row('  Snapshot chain= Each snapshot added to chain; long chains slow reads; delete after use'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-service-availability',
    'docs/performance/service-availability/index.md',
    'Service availability — measurement, downtime tracking, reporting against SLA targets',
)
def perf_service_availability():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Performance — Service Availability'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Measure and report service availability; track downtime; compare against SLA targets')))
    lines.append(R(bMid(IV_L, IV_R, 'Availability = (total time - downtime) / total time * 100; track per service per month')))
    lines.append(R(bMid(IV_L, IV_R, 'Planned maintenance excluded from calculation if pre-approved and communicated')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Availability Tiers'), bMid(B2_L, B2_R, 'Measurement'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '99.9% = 8.7h/yr downtime'), bMid(B2_L, B2_R, 'Monitor: synthetic check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '99.95% = 4.4h/yr'), bMid(B2_L, B2_R, 'Log outage: start/end time'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '99.99% = 52 min/yr'), bMid(B2_L, B2_R, 'Calculate monthly percent'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '99.999% = 5.2 min/yr'), bMid(B2_L, B2_R, 'Report to stakeholders'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Target per service tier'), bMid(B2_L, B2_R, 'Trend vs SLA target'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Availability', 'Downtime/yr', 'Downtime/mo', 'Tier', 'Example'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['99.9%', '8.7 hours', '43.8 min', 'Standard', 'Dev/test'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['99.95%', '4.4 hours', '21.9 min', 'Business', 'Internal apps'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['99.99%', '52 min', '4.4 min', 'Critical', 'Prod services'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['99.999%', '5.2 min', '26 sec', 'Mission', 'Core infra'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Synthetic check = Automated probe that tests service endpoint; detects outages before users'))
    lines.append(txt_row('  Maintenance window= Planned downtime; communicated in advance; excluded from availability calc'))
    lines.append(txt_row('  Error budget  = 1 - SLO; allowable downtime; consumed by incidents and planned maintenance'))
    lines.append(txt_row('  Nines         = Number of 9s in availability %; four nines (99.99%) = 52 min/yr max'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'perf-slo',
    'docs/performance/service-level-objectives/index.md',
    'Service level objectives — defining, measuring, reporting SLOs for infrastructure services',
)
def perf_slo():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Performance — Service Level Objectives (SLOs)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SLOs: agree what "good" looks like; measure it with SLIs; budget for error allowance')))
    lines.append(R(bMid(IV_L, IV_R, 'SLI → SLO → Error budget: define metric → set target → calculate allowable failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Report SLO status monthly; burn rate alerts when budget is consumed too fast')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLO Definition'), bMid(B2_L, B2_R, 'Reporting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLI: request success %'), bMid(B2_L, B2_R, 'Monthly SLO report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLO: 99.9% success rate'), bMid(B2_L, B2_R, 'Error budget remaining %'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Window: 30-day rolling'), bMid(B2_L, B2_R, 'Burn rate alert (fast)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Error budget: 0.1%'), bMid(B2_L, B2_R, 'Freeze changes if depleted'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Latency SLO: p99 < 500ms'), bMid(B2_L, B2_R, 'Review with stakeholders'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SLI     = Service Level Indicator; the measured metric (e.g. % requests returning 2xx)'))
    lines.append(txt_row('  SLO     = Service Level Objective; target value for the SLI (e.g. 99.9% success rate)'))
    lines.append(txt_row('  SLA     = Service Level Agreement; contractual SLO with financial/legal consequences'))
    lines.append(txt_row('  Error budget= 1 - SLO; how much unreliability is acceptable; zero budget = freeze changes'))
    lines.append(txt_row('  Burn rate   = Speed at which error budget is consumed; fast burn = alert immediately'))
    lines.append(txt_row('  Rolling window= SLO measured over last 30 days; older incidents age out of calculation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Architecture ──────────────────────────────────────────────────────────────

@kb_diagram(
    'architecture',
    'docs/architecture/index.md',
    'Architecture landing — HA, storage design, network topology, DR design principles',
)
def architecture_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Architecture — HA Design, Storage, Networking & Disaster Recovery'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Architecture design guides for enterprise infrastructure: HA, storage, network, DR')))
    lines.append(R(bMid(IV_L, IV_R, 'Design principles: eliminate single points of failure; automate failover; test recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'All designs must state: RPO/RTO targets, failure domain boundaries, and recovery path')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compute & HA'), bMid(B2_L, B2_R, 'Storage & Network'), bMid(B3_L, B3_R, 'DR & Recovery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'N+1 host capacity'), bMid(B2_L, B2_R, 'Storage tiering'), bMid(B3_L, B3_R, 'RPO / RTO targets'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DRS + vSphere HA'), bMid(B2_L, B2_R, 'Redundant paths'), bMid(B3_L, B3_R, 'Active-passive DR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failure domain plan'), bMid(B2_L, B2_R, 'L3 segmentation'), bMid(B3_L, B3_R, 'Replication design'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Anti-affinity rules'), bMid(B2_L, B2_R, 'Spine-leaf topology'), bMid(B3_L, B3_R, 'Failover runbook'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resource pools'), bMid(B2_L, B2_R, 'BGP peering design'), bMid(B3_L, B3_R, 'Recovery testing'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  N+1          = One more host than minimum required; one failure without service impact'))
    lines.append(txt_row('  Failure domain= Boundary within which a single failure has impact; AZ / rack / PDU'))
    lines.append(txt_row('  Anti-affinity = Rule keeping workloads on different hosts for HA; opposite of affinity'))
    lines.append(txt_row('  Spine-leaf   = Data centre switching topology; spine = core, leaf = ToR; no STP needed'))
    lines.append(txt_row('  Active-passive= Primary handles all traffic; standby takes over on failure (vs active-active)'))
    lines.append(txt_row('  RPO/RTO      = Recovery Point/Time Objectives; quantify acceptable data loss and downtime'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'arch-dr-design',
    'docs/architecture/disaster-recovery-design/index.md',
    'DR design — RPO/RTO targets, site topology, failover patterns, DR architecture decisions',
)
def arch_dr_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Architecture — Disaster Recovery Design'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DR design: select site topology and replication pattern to meet RPO/RTO targets')))
    lines.append(R(bMid(IV_L, IV_R, 'Tiers: hot standby (< 1 min RTO), warm (< 4h), cold (> 4h, data only backup)')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: synchronous (zero RPO, latency cost) vs async (small RPO, no latency)')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DR Tiers'), bMid(B2_L, B2_R, 'Replication Options'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hot: always-on sync'), bMid(B2_L, B2_R, 'Sync: zero RPO; ≤ 100km'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Warm: replicated async'), bMid(B2_L, B2_R, 'Async: RPO minutes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cold: backup only'), bMid(B2_L, B2_R, 'SRM / Zerto / vVols'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DR site sizing: N+x'), bMid(B2_L, B2_R, 'Storage-level replication'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test annually minimum'), bMid(B2_L, B2_R, 'App-consistent snapshots'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Tier', 'RPO', 'RTO', 'Cost', 'Technology'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Hot standby', 'Near zero', '< 15 min', 'Highest', 'Sync rep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Warm standby', '< 15 min', '1-4 hours', 'Medium', 'Async rep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Cold standby', '< 24 hours', '> 4 hours', 'Lowest', 'Backup/tape'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RPO          = Recovery Point Objective; max acceptable data loss; drives replication freq'))
    lines.append(txt_row('  RTO          = Recovery Time Objective; max acceptable downtime; drives DR tier selection'))
    lines.append(txt_row('  Synchronous  = Write confirmed only after replica ACK; zero data loss; limited by distance'))
    lines.append(txt_row('  Asynchronous = Write confirmed locally; replica slightly behind; RPO = replication interval'))
    lines.append(txt_row('  SRM          = VMware Site Recovery Manager; orchestrates VM failover between vCenter sites'))
    lines.append(txt_row('  BCP          = Business Continuity Plan; broader than DR; includes people, process, comms'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'arch-ha',
    'docs/architecture/high-availability/index.md',
    'High availability design — HA patterns, redundancy, automatic failover, cluster design',
)
def arch_ha():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Architecture — High Availability Design'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'HA design: eliminate single points of failure; automate detection and failover')))
    lines.append(R(bMid(IV_L, IV_R, 'Layers: compute (vSphere HA), storage (multi-path/RAID), network (bonding/LACP)')))
    lines.append(R(bMid(IV_L, IV_R, 'Rule: every component has a redundant path; failure triggers automatic recovery')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA Patterns'), bMid(B2_L, B2_R, 'Redundancy Layers'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active-active: both serve'), bMid(B2_L, B2_R, 'Compute: N+1 hosts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active-passive: auto failover'), bMid(B2_L, B2_R, 'Storage: dual paths MPIO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'N+1 / N+2 host capacity'), bMid(B2_L, B2_R, 'Network: bonding / LACP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Anti-affinity rules'), bMid(B2_L, B2_R, 'Power: dual PSU + PDU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heartbeat monitoring'), bMid(B2_L, B2_R, 'Site: AZ or DC pair'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SPOF         = Single Point of Failure; any component whose failure stops the service'))
    lines.append(txt_row('  MPIO         = Multi-Path I/O; multiple physical paths to storage; path failure is transparent'))
    lines.append(txt_row('  LACP         = Link Aggregation Control Protocol; bonds multiple NICs into one logical link'))
    lines.append(txt_row('  vSphere HA   = Restarts VMs on surviving hosts within minutes of host failure'))
    lines.append(txt_row('  Fencing      = Isolate a failed node before failover to prevent split-brain'))
    lines.append(txt_row('  Quorum       = Cluster consensus mechanism; majority of nodes must agree on cluster state'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'arch-network-design',
    'docs/architecture/network-design/index.md',
    'Network design — topology, segmentation, routing, BGP peering, security zones',
)
def arch_network_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Architecture — Network Design'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Enterprise network design: spine-leaf topology, L3 segmentation, security zones, BGP')))
    lines.append(R(bMid(IV_L, IV_R, 'Spine-leaf: no STP; any leaf to any leaf = 2 hops; ECMP for load distribution')))
    lines.append(R(bMid(IV_L, IV_R, 'Zones: untrusted → DMZ → internal → restricted; firewalls at zone boundaries')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Topology'), bMid(B2_L, B2_R, 'Segmentation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Spine: 2+ core switches'), bMid(B2_L, B2_R, 'VLANs per function/zone'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Leaf: ToR per rack'), bMid(B2_L, B2_R, 'L3 boundary per zone'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ECMP load balancing'), bMid(B2_L, B2_R, 'FW between zones'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'BGP for DC routing'), bMid(B2_L, B2_R, 'Micro-seg (NSX)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dual uplinks per leaf'), bMid(B2_L, B2_R, 'ACL on VLAN SVIs'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Spine-leaf   = Two-tier DC fabric; spines interconnect all leaves; no STP; predictable latency'))
    lines.append(txt_row('  ECMP         = Equal-Cost Multi-Path; traffic distributed across multiple equal-cost paths'))
    lines.append(txt_row('  ToR          = Top of Rack switch; leaf switch physically mounted at top of server rack'))
    lines.append(txt_row('  BGP          = Border Gateway Protocol; used for DC internal routing and WAN peering'))
    lines.append(txt_row('  SVI          = Switched Virtual Interface; L3 gateway for a VLAN; ACLs applied here'))
    lines.append(txt_row('  Micro-seg    = Per-VM firewall rules (NSX DFW); east-west traffic control inside DC'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'arch-storage-design',
    'docs/architecture/storage-design/index.md',
    'Storage design — tiering, protocols, redundancy, performance, and capacity planning',
)
def arch_storage_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Architecture — Storage Design'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Storage design: tier workloads by I/O profile; select protocol; plan redundancy')))
    lines.append(R(bMid(IV_L, IV_R, 'Tiers: NVMe (< 0.1ms) → SSD (< 1ms) → SAS/NL-SAS (2-5ms) → archive/cloud')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocol: FC (SAN/high perf), iSCSI (SAN/cost), NFS/SMB (file), S3 (object)')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Design Considerations'), bMid(B2_L, B2_R, 'Redundancy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Workload I/O profile'), bMid(B2_L, B2_R, 'RAID 5/6 or erasure code'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity now + 3yr'), bMid(B2_L, B2_R, 'Dual controllers'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocol selection'), bMid(B2_L, B2_R, 'Multipath (MPIO)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thin vs thick prov'), bMid(B2_L, B2_R, 'Replication to DR site'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption at rest'), bMid(B2_L, B2_R, 'Snapshot policy'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  NVMe         = Non-Volatile Memory Express; PCIe-attached flash; lowest latency storage'))
    lines.append(txt_row('  FC           = Fibre Channel; dedicated SAN fabric; high performance and reliability'))
    lines.append(txt_row('  iSCSI        = SCSI over IP; block storage over Ethernet; lower cost than FC'))
    lines.append(txt_row('  Erasure code = Striping with parity across drives; space-efficient; used in scale-out arrays'))
    lines.append(txt_row('  Thin prov    = Space allocated on-demand; must monitor actual usage vs overcommit'))
    lines.append(txt_row('  MPIO         = Multi-Path I/O; multiple paths to array; transparent failover on path loss'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines

# ── Networking ────────────────────────────────────────────────────────────────

@kb_diagram(
    'networking',
    'docs/networking/index.md',
    'Networking landing — switching, routing, security, services and troubleshooting',
)
def networking_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []
    lines.append(title_border(W2, 'Networking — Switching, Routing, Security & Services'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Networking KB: design references, configuration procedures, and troubleshooting guides')))
    lines.append(R(bMid(IV_L, IV_R, 'Covers: VLANs, BGP/OSPF, firewall validation, DNS, load balancing, connectivity tests')))
    lines.append(R(bMid(IV_L, IV_R, 'Foundation: segment by function, redundant paths, document every rule and change')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switching & Routing'), bMid(B2_L, B2_R, 'Security'), bMid(B3_L, B3_R, 'Services & TS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VLANs / trunking'), bMid(B2_L, B2_R, 'Firewall rules'), bMid(B3_L, B3_R, 'DNS resolution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'BGP / OSPF routing'), bMid(B2_L, B2_R, 'VPN tunnels'), bMid(B3_L, B3_R, 'Load balancer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Subnetting / CIDR'), bMid(B2_L, B2_R, 'ACL validation'), bMid(B3_L, B3_R, 'Connectivity tests'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'STP / LACP'), bMid(B2_L, B2_R, 'NAT / PAT'), bMid(B3_L, B3_R, 'Packet capture'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'QoS marking'), bMid(B2_L, B2_R, 'IDS/IPS rules'), bMid(B3_L, B3_R, 'Path tracing'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VLAN         = Virtual LAN; logical broadcast domain; isolates traffic by function or tenant'))
    lines.append(txt_row('  BGP          = Border Gateway Protocol; path-vector routing; used for WAN and DC fabric'))
    lines.append(txt_row('  OSPF         = Open Shortest Path First; link-state IGP; used within a campus or data centre'))
    lines.append(txt_row('  LACP         = Link Aggregation; bonds NICs for bandwidth + redundancy; IEEE 802.3ad'))
    lines.append(txt_row('  STP          = Spanning Tree Protocol; loop prevention; RSTP preferred; MSTP for VLANs'))
    lines.append(txt_row('  ECMP         = Equal-Cost Multi-Path; load-balance across redundant L3 paths'))
    lines.append(txt_row('  NAT          = Network Address Translation; maps private IPs to public; hides topology'))
    lines.append(txt_row('  QoS          = Quality of Service; priority marking to protect latency-sensitive traffic'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'net-switching-routing',
    'docs/networking/switching-routing/index.md',
    'Switching and routing — VLANs, inter-VLAN routing, BGP, OSPF, subnetting, TCP/IP',
)
def net_switching_routing():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Networking — Switching & Routing'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VLANs segment broadcast domains; trunk ports carry multiple VLANs between switches')))
    lines.append(R(bMid(IV_L, IV_R, 'Routing: OSPF for internal; BGP for DC fabric and WAN; static for management paths')))
    lines.append(R(bMid(IV_L, IV_R, 'Subnetting: plan IP space per VLAN; document in IPAM; leave growth headroom')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switching'), bMid(B2_L, B2_R, 'Routing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VLAN: show vlan brief'), bMid(B2_L, B2_R, 'OSPF: show ip ospf neigh'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trunk: show int trunk'), bMid(B2_L, B2_R, 'BGP: show bgp summary'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'STP: show span brief'), bMid(B2_L, B2_R, 'Route table: show ip route'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LACP: show etherchannel'), bMid(B2_L, B2_R, 'Ping + traceroute verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MAC table: show mac addr'), bMid(B2_L, B2_R, 'MTU: ping with df-bit set'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['VLAN', 'Name', 'Subnet', 'Gateway', 'Purpose'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['10', 'Management', '10.0.10.0/24', '10.0.10.1', 'OOB / IPMI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['20', 'vMotion', '10.0.20.0/24', '10.0.20.1', 'VMware vMotion'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['30', 'Storage', '10.0.30.0/24', '10.0.30.1', 'iSCSI / NFS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['100', 'Production', '10.1.0.0/22', '10.1.0.1', 'VM workloads'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Trunk port   = Switch port carrying multiple VLANs with 802.1Q tagging'))
    lines.append(txt_row('  Native VLAN  = Untagged VLAN on a trunk; must match both sides; mismatch causes loops'))
    lines.append(txt_row('  SVI          = Switched Virtual Interface; L3 gateway for a VLAN on a layer-3 switch'))
    lines.append(txt_row('  ECMP         = Equal-Cost Multi-Path; multiple routes to destination; load balanced'))
    lines.append(txt_row('  IPAM         = IP Address Management; tracks allocations; prevents duplicate IPs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'net-security',
    'docs/networking/security/index.md',
    'Network security — firewall rule validation, VPN, ACL, NAT, IDS/IPS references',
)
def net_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Networking — Network Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network security: validate FW rules, confirm VPN tunnels, audit ACLs, review NAT')))
    lines.append(R(bMid(IV_L, IV_R, 'FW validation: test required traffic with packet tracer; review deny logs for gaps')))
    lines.append(R(bMid(IV_L, IV_R, 'VPN: check tunnel state, phase 1/2, SA lifetime, interesting traffic; test end-to-end')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Firewall Checks'), bMid(B2_L, B2_R, 'VPN & ACL'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Packet tracer test'), bMid(B2_L, B2_R, 'show crypto isakmp sa'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review deny log hits'), bMid(B2_L, B2_R, 'show crypto ipsec sa'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rule order matters'), bMid(B2_L, B2_R, 'ACL: show access-list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check NAT translation'), bMid(B2_L, B2_R, 'NAT: show ip nat trans'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Unused rules: review/remove'), bMid(B2_L, B2_R, 'Test from both sides'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Packet tracer  = Cisco tool; simulates traffic through FW to determine permit/deny outcome'))
    lines.append(txt_row('  IKE phase 1    = VPN control plane; authenticates peers; establishes management SA'))
    lines.append(txt_row('  IKE phase 2    = VPN data plane; negotiates IPsec SA for encrypting user traffic'))
    lines.append(txt_row('  Interesting traffic= VPN traffic selector; defines what source/dest pairs trigger the tunnel'))
    lines.append(txt_row('  ACL            = Access Control List; permits or denies traffic by src/dst/port/protocol'))
    lines.append(txt_row('  PAT            = Port Address Translation; maps multiple private IPs to one public IP+port'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'net-services',
    'docs/networking/services/index.md',
    'Network services — DNS, load balancers, DHCP, IPAM management references',
)
def net_services():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Networking — Network Services'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network services: DNS (name resolution), DHCP (IP assignment), load balancers, IPAM')))
    lines.append(R(bMid(IV_L, IV_R, 'DNS: every server needs forward + reverse records; split-horizon for internal names')))
    lines.append(R(bMid(IV_L, IV_R, 'Load balancer: health checks must match app check; monitor pool member state daily')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DNS'), bMid(B2_L, B2_R, 'Load Balancer & DHCP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'A record: name → IP'), bMid(B2_L, B2_R, 'VIP: virtual IP for pool'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PTR record: IP → name'), bMid(B2_L, B2_R, 'Pool: backend servers'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CNAME: alias record'), bMid(B2_L, B2_R, 'Health check: HTTP/TCP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test: nslookup / dig'), bMid(B2_L, B2_R, 'DHCP: scope + exclusions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TTL: lower for planned changes'), bMid(B2_L, B2_R, 'IPAM: track allocations'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  A record     = DNS forward lookup; hostname → IPv4 address'))
    lines.append(txt_row('  PTR record   = DNS reverse lookup; IP → hostname; needed for SMTP and some auth'))
    lines.append(txt_row('  TTL          = Time To Live; how long resolvers cache the record; lower before cutover'))
    lines.append(txt_row('  Split-horizon= Different DNS answers for internal vs external queries for same name'))
    lines.append(txt_row('  VIP          = Virtual IP; load balancer frontend; clients connect here, not to backend'))
    lines.append(txt_row('  SNAT         = Source NAT on load balancer; ensures response traffic returns via LB'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'net-troubleshooting',
    'docs/networking/troubleshooting/index.md',
    'Network troubleshooting — connectivity, packet loss, path tracing, reachability validation',
)
def net_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []
    lines.append(title_border(W2, 'Networking — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network troubleshooting: work from layer 1 up; isolate the failure layer first')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: ping (L3 reachability), traceroute (path), tcpdump/Wireshark (packet capture)')))
    lines.append(R(bMid(IV_L, IV_R, 'Process: define symptom → test from multiple points → narrow to single failure point')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnostic Steps'), bMid(B2_L, B2_R, 'Common Causes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'L1: link up? SFP seated?'), bMid(B2_L, B2_R, 'FW rule blocking traffic'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'L2: MAC learned? VLAN OK?'), bMid(B2_L, B2_R, 'VLAN mismatch / missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'L3: ping gateway + dest'), bMid(B2_L, B2_R, 'Routing missing/incorrect'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trace: traceroute path'), bMid(B2_L, B2_R, 'MTU mismatch (DF bit)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capture: tcpdump src/dst'), bMid(B2_L, B2_R, 'DNS: name not resolving'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Layer', 'Check', 'Tool', 'Symptom', 'Fix direction'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L1 Physical', 'Link state', 'show int', 'err-disabled', 'Cable/SFP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L2 Data link', 'MAC + VLAN', 'show mac', 'No L2 learn', 'VLAN config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L3 Network', 'Route + ping', 'traceroute', 'Unreachable', 'Route/FW'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['L4+ App', 'Port + cert', 'nc / curl -v', 'Conn refused', 'FW/app/TLS'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OSI model    = 7-layer reference model; troubleshoot from bottom up (L1 → L7)'))
    lines.append(txt_row('  MTU          = Maximum Transmission Unit; 1500B Ethernet; jumbo = 9000; mismatch = drops'))
    lines.append(txt_row('  DF bit       = Do Not Fragment; test MTU by pinging with DF set and large payload'))
    lines.append(txt_row('  tcpdump      = Packet capture on Linux; filter by host, port, protocol; save to pcap'))
    lines.append(txt_row('  err-disabled = Switch port auto-disabled; cause: BPDU guard, port security, duplex mismatch'))
    lines.append(txt_row('  Asymmetric   = Forward and return path differ; FW stateful check fails; causes drops'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Singles (top-level pages) ─────────────────────────────────────────────────



@kb_diagram(
    'start-here',
    'docs/start-here/index.md',
    'Start Here — how to navigate and use the KB effectively',
)
def kb_start_here():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []
    lines.append(title_border(W2, 'Start Here — How to Navigate the KB'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'This KB is built for practical infrastructure work: quick notes, runbooks, standards')))
    lines.append(R(bMid(IV_L, IV_R, 'Navigate: top platform → vendor/product → specific procedure or reference')))
    lines.append(R(bMid(IV_L, IV_R, 'Add field notes as issues come up; keep it current; link from tickets and runbooks')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'How to Use'), bMid(B2_L, B2_R, 'Main Workflows'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Start with major area'), bMid(B2_L, B2_R, 'Incident: go straight to TS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Open vendor or platform'), bMid(B2_L, B2_R, 'Change: use runbook page'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Use cards for deep dives'), bMid(B2_L, B2_R, 'New system: check arch page'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add notes after field work'), bMid(B2_L, B2_R, 'Audit: use inventory section'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site Map for full index'), bMid(B2_L, B2_R, 'Learning: browse by topic'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Site Map     = Full index of all KB pages; use to find content when browsing fails'))
    lines.append(txt_row('  Card grid    = Landing page layout; click a card to go to a specific sub-topic'))
    lines.append(txt_row('  kb-summary   = Concise overview block at the top of every landing page'))
    lines.append(txt_row('  Runbook      = Step-by-step procedure for a common operational task'))
    lines.append(txt_row('  Field notes  = Observations from real incidents; add to relevant page for future reference'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'offline',
    'docs/offline/index.md',
    'Offline page — shown when the user has no internet connection (PWA fallback)',
)
def kb_offline():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []
    lines.append(title_border(W2, 'Offline — No Internet Connection'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'This page is displayed when the browser cannot reach the KB server')))
    lines.append(R(bMid(IV_L, IV_R, 'Pages visited before going offline are available from the service worker cache')))
    lines.append(R(bMid(IV_L, IV_R, 'Use the navigation menu to browse cached content while offline')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Service worker = Browser background script; caches pages for offline access (PWA pattern)'))
    lines.append(txt_row('  PWA            = Progressive Web App; installable; works offline using service worker cache'))
    lines.append(txt_row('  Cache          = Local copy of page content stored by the service worker on first visit'))
    lines.append(txt_row('  Fallback page  = Shown when a requested URL is not in cache and network is unavailable'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
