#!/usr/bin/env python3
"""
Re-insert code blocks for the 8 learning-diagram sections that were stripped
by fix_duplicate_diagrams.py (it kept only the ## heading, not the fence block).

Run from repo root: python3 scripts/repair_aws_diagrams.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from add_aws_learning_diagrams import (
    d_global_infra, d_shared_responsibility, d_well_architected, d_caf, d_seven_rs,
    d_vpc_subnet, d_network_connectivity, d_route53,
    d_iam_model, d_policy_evaluation,
    d_ec2_purchase, d_instance_families, d_compute_services, d_autoscaling_lb,
    d_s3_classes, d_storage_comparison,
    d_pricing_models, d_support_tiers,
    d_security_services,
    d_organizations,
)

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
AWS = os.path.join(DOCS, 'cloud', 'aws')


def section_block(sec):
    """Return just the code-fence block from a section list (no heading/separator)."""
    # sec = ['\n---\n', '## heading\n', '```', ...lines..., '```\n']
    fence_start = next(i for i, x in enumerate(sec) if x == '```')
    return '```\n' + '\n'.join(sec[fence_start + 1:-1]) + '\n```\n'


def insert_block_after_heading(path, heading, sec):
    """Insert the code block immediately after the ## heading line, if not already there."""
    with open(path) as f:
        content = f.read()

    marker = '## ' + heading
    if marker not in content:
        print(f'  SKIP (no heading): {marker}')
        return

    idx = content.index(marker)
    end_of_heading_line = content.index('\n', idx) + 1
    after_heading = content[end_of_heading_line:]

    # Check if a code block with box chars already follows this heading within this section
    next_section = re.search(r'^## ', after_heading, re.MULTILINE)
    section_text = after_heading[:next_section.start()] if next_section else after_heading
    if re.search(r'[┌└]', section_text):
        print(f'  OK (already present): {heading}')
        return

    block = '\n' + section_block(sec)
    new_content = content[:end_of_heading_line] + block + content[end_of_heading_line:]
    with open(path, 'w') as f:
        f.write(new_content)
    print(f'  Repaired: {heading}  in {os.path.relpath(path)}')


def main():
    repairs = [
        (os.path.join(AWS, 'architecture', 'how-it-works', 'index.md'),
         'AWS Global Infrastructure', d_global_infra()),

        (os.path.join(AWS, 'networking', 'vpc', 'index.md'),
         'VPC Subnet Architecture', d_vpc_subnet()),

        (os.path.join(AWS, 'identity', 'iam', 'index.md'),
         'IAM Identity Model', d_iam_model()),

        (os.path.join(AWS, 'compute', 'ec2', 'index.md'),
         'EC2 Purchase Options', d_ec2_purchase()),

        (os.path.join(AWS, 'storage', 's3', 'index.md'),
         'S3 Storage Classes', d_s3_classes()),

        (os.path.join(AWS, 'cost', 'index.md'),
         'EC2 Pricing Models', d_pricing_models()),

        (os.path.join(AWS, 'security', 'index.md'),
         'AWS Security Services Map', d_security_services()),

        (os.path.join(AWS, 'governance', 'aws-organizations', 'index.md'),
         'AWS Organizations Multi-Account Hierarchy', d_organizations()),
    ]

    for path, heading, sec in repairs:
        insert_block_after_heading(path, heading, sec)

    print('\nDone.')


if __name__ == '__main__':
    main()
