#!/usr/bin/env python3
"""
Fix duplicate diagrams in KB markdown files.

Three cases handled:
1. Identical duplicates (642 files): first copy is properly fenced,
   second copy has no open fence but has a trailing close fence.
   Fix: remove second copy + its trailing fence.

2. Different diagrams — small old + large new (16 files): keep the
   full-width proper diagram, remove the small pre-existing one + its fences.

3. Multi-box flow diagrams (72 files): legitimate separate boxes
   connected by arrows — leave alone.
"""
import glob, sys

FULL_WIDTH_MIN = 100   # chars — outer box is 103 chars wide
FLOW_GAP_MAX   = 5     # lines gap between boxes → flow diagram


def classify(lines, tops, bots):
    """Return 'identical', 'large_small', or 'flow'."""
    if len(tops) < 2:
        return 'single'

    # Check for identical pair FIRST (before gap check):
    # true duplicates have identical content regardless of gap size.
    if len(bots) >= 2:
        d1 = ''.join(lines[tops[0]:bots[0] + 1])
        d2 = ''.join(lines[tops[1]:bots[1] + 1])
        if d1 == d2:
            return 'identical'

    # Check if any pair is a flow (close together with different content)
    for i in range(len(tops) - 1):
        gap = tops[i + 1] - (bots[i] if i < len(bots) else tops[i])
        if gap <= FLOW_GAP_MAX:
            return 'flow'

    # Different diagrams separated by content — determine which is full-width
    return 'large_small'


def fix_identical(lines, tops, bots):
    """Remove the second copy of an identical duplicate + its trailing fence.

    The duplicate structure is always:
      [open-fence] [d1] [close-fence] [d2-no-open-fence] [close-fence]
    We keep [open-fence] [d1] [close-fence] and delete [d2] [close-fence].
    """
    t2 = tops[1]
    b2 = bots[1] if len(bots) > 1 else t2

    # Start deletion at the top of d2 (NOT any preceding fence which belongs to d1)
    start = t2

    # Find the close fence immediately after b2 and include it in deletion
    post_fence = None
    for j in range(b2 + 1, min(len(lines), b2 + 4)):
        if lines[j].strip() == '```':
            post_fence = j
            break

    end = (post_fence + 1) if post_fence is not None else (b2 + 1)

    return lines[:start] + lines[end:]


def fix_large_small(lines, tops, bots):
    """Keep the full-width diagram, remove the smaller one + its fences.

    When ALL diagrams are full-width (≥ FULL_WIDTH_MIN) they are independent
    learning sections — leave the file untouched.
    """
    full_idxs  = [i for i, t in enumerate(tops) if len(lines[t].rstrip()) >= FULL_WIDTH_MIN]
    small_idxs = [i for i, t in enumerate(tops) if len(lines[t].rstrip()) <  FULL_WIDTH_MIN]

    # All full-width → independent sections; do nothing
    if not small_idxs:
        return lines

    if not full_idxs or len(small_idxs) != 1:
        # Can't determine safely — leave alone
        return lines

    remove_idx = small_idxs[0]
    t_rm = tops[remove_idx]
    b_rm = bots[remove_idx] if remove_idx < len(bots) else t_rm

    # Extend removal to include any adjacent fence lines
    pre_fence = None
    for j in range(max(0, t_rm - 3), t_rm):
        if lines[j].strip() == '```':
            pre_fence = j

    post_fence = None
    for j in range(b_rm + 1, min(len(lines), b_rm + 4)):
        if lines[j].strip() == '```':
            post_fence = j
            break

    start = pre_fence if pre_fence is not None else t_rm
    end   = (post_fence + 1) if post_fence is not None else (b_rm + 1)

    return lines[:start] + lines[end:]


def process_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    tops = [i for i, l in enumerate(lines) if l.startswith('┌')]
    bots = [i for i, l in enumerate(lines) if l.startswith('└')]

    if len(tops) < 2:
        return 'skip'

    kind = classify(lines, tops, bots)

    if kind == 'flow':
        return 'flow_skip'

    if kind == 'identical':
        new_lines = fix_identical(lines, tops, bots)
        action = 'identical'
    elif kind == 'large_small':
        new_lines = fix_large_small(lines, tops, bots)
        action = 'large_small'
    else:
        return 'skip'

    if new_lines == lines:
        return 'no_change'

    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)

    return action


def main():
    dry_run = '--dry-run' in sys.argv
    pages   = sorted(glob.glob('docs/**/*.md', recursive=True))

    counts = {'identical': 0, 'large_small': 0, 'flow_skip': 0,
              'no_change': 0, 'skip': 0}

    for p in pages:
        result = process_file(p, dry_run=dry_run)
        counts[result] = counts.get(result, 0) + 1
        if result in ('identical', 'large_small'):
            print(f"  [{result}] {p}")

    print(f"\nResults ({'DRY RUN' if dry_run else 'APPLIED'}):")
    print(f"  Identical duplicates fixed : {counts['identical']}")
    print(f"  Large+small diagram fixed  : {counts['large_small']}")
    print(f"  Flow diagrams (skipped)    : {counts['flow_skip']}")
    print(f"  No change needed           : {counts['no_change']}")
    print(f"  Single diagram (skipped)   : {counts['skip']}")


if __name__ == '__main__':
    main()
