from typing import TextIO, Iterable

from aoc24.helpers.main import run_solution


Rules = dict[int, set[int]]


def load_rules(lines: Iterable[str]) -> Rules:
    # Loads rules, returning a dict where keys must come before the corresponding values
    rules: dict[int, set[int]] = {}
    for l in lines:
        l = l.strip()
        if not l:
            break
        a, b = [int(c) for c in l.split("|")]
        rules.setdefault(a, set()).add(b)
    return rules


def is_update_valid(update: list[int], rules: Rules) -> bool:
    seen: set[int] = set()
    for page in update:
        if page in rules and (seen & rules[page]):
            # If we've already seen an item which must come after `page`, the update is invalid
            return False
        seen.add(page)
    return True


def explode_rules(rules: Rules) -> None:
    # Explode rules - if 1|2 and 2|3 add 1|3
    for k, values in rules.items():
        done: set[int] = set()
        while done != values:
            for v in values - done:
                values |= rules.get(v, set())
                done.add(v)
        assert k not in values, f"Cycle detected: {k} {values}"


def p5a(f: TextIO) -> int:
    lines = iter(f)
    rules = load_rules(lines)

    total = 0
    for l in lines:
        update = [int(c) for c in l.strip().split(",")]
        if is_update_valid(update, rules):
            # All rules followed
            total += update[len(update) // 2]
    return total


def p5b(f: TextIO) -> int:
    lines = iter(f)
    before_rules = load_rules(lines)

    total = 0
    for l in lines:
        update = [int(c) for c in l.strip().split(",")]
        if not is_update_valid(update, before_rules):
            # For there to be a unique ordering, we should be able to explode the ruleset (i.e. add rules for all
            # transitive rules, e.g. if 1|3 and 3|4 then add 1|4) then sort by the number of rules. The page with the
            # most rules must be before all of the other rules
            # Note, there can be (and are!) cycles in the overall ruleset (e.g. 1|2 2|3 3|1) but there can't be any
            # cycles in the partial ruleset for each update
            nums = set(update)
            update_rules = {k: before_rules[k] & nums for k in nums}
            explode_rules(update_rules)
            update = sorted(update, key=lambda i: len(update_rules[i]), reverse=True)
            total += update[len(update) // 2]
    return total


if __name__ == "__main__":
    run_solution(p5a, p5b, 5)
