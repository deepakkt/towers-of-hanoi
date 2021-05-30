from time import perf_counter as perf_counter_ns
from copy import copy


def perform_op(op):
    # perform is just printing the op
    if op["stack"] == 1:
        print("Move 1 from {} to {}".format(op["from"], op["to"]))
        return 1

    if op["stack"] == 2:
        print("Move 1 from {} to {}".format(op["from"], op["intermediate"]))
        print("Move 2 from {} to {}".format(op["from"], op["to"]))
        print("Move 1 from {} to {}".format(op["intermediate"], op["to"]))
        return 3

    print("Move {} from {} to {}".format(op["stack"], op["from"], op["to"]))
    return 1


def seed_ops_stack(ops_template, stacks, origin, destination, intermediate, terminate=False):
    ops_seed = []

    first = copy(ops_template)
    first["stack"] = stacks - 1
    first["from"] = origin
    first["to"] = intermediate
    first["intermediate"] = destination
    first["atomic"] = (stacks - 1) <= 2

    ops_seed.append(first)

    second = copy(ops_template)
    second["atomic"] = True
    second["single"] = True
    second["from"] = origin
    second["to"] = destination
    second["intermediate"] = intermediate
    second["stack"] = stacks

    ops_seed.append(second)

    third = copy(ops_template)
    third["from"] = intermediate
    third["to"] = destination
    third["intermediate"] = origin
    third["stack"] = stacks - 1
    third["atomic"] = (stacks - 1) <= 2

    ops_seed.append(third)

    if terminate:
        term = copy(ops_template)
        term["terminate"] = True
        ops_seed.append(term)

    return ops_seed


def non_recursive(stacks):
    # don't change ops template. this will impact rest of the code
    op_template = {
        "atomic": False,
        "single": False,
        "terminate": False,
        "from": "A",
        "to": "C",
        "intermediate": "B",
        "stack": 2
    }

    if stacks <= 2:
        current_op = copy(op_template)
        current_op["atomic"] = True
        current_op["stack"] = stacks
        ops = perform_op(current_op)
        return ops

    # seed the op stack
    ops_list = seed_ops_stack(op_template, stacks, "A", "C", "B", terminate=True)

    work_idx = 0
    total_ops = 0
    while True:
        current_op = ops_list[work_idx]

        if current_op["terminate"]:
            break

        if current_op["atomic"]:
            total_ops += perform_op(current_op)
            work_idx += 1
            continue

        sub_ops_list = seed_ops_stack(op_template,
                                  current_op["stack"],
                                  current_op["from"],
                                  current_op["to"],
                                  current_op["intermediate"],
                                  )

        ops_list.pop(work_idx)
        for oneop in sub_ops_list[-1::-1]:
            ops_list.insert(work_idx, oneop)
        continue

    return total_ops


def recursive(stacks, origin, destination, intermediate):
    if stacks == 1:
        print("Move 1 from {} to {}".format(origin, destination))
        return 1

    if stacks == 2:
        print("Move 1 from {} to {}".format(origin, intermediate))
        print("Move 2 from {} to {}".format(origin, destination))
        print("Move 1 from {} to {}".format(intermediate, destination))
        return 3

    total_ops = 0
    total_ops += recursive(stacks - 1, origin, intermediate, destination)
    print("Move {} from {} to {}".format(stacks, origin, destination))
    total_ops += 1
    total_ops += recursive(stacks - 1, intermediate, destination, origin)

    return total_ops


if __name__ == "__main__":
    rec_start = perf_counter_ns()
    total_ops = recursive(10, "P1", "P3", "P2")
    rec_end = perf_counter_ns()
    print("Completed in {} ops".format(total_ops))

    non_rec_start = perf_counter_ns()
    total_ops = non_recursive(10)
    non_rec_end = perf_counter_ns()
    print("Completed in {} ops".format(total_ops))

    print("Recursive => {:0.5f}".format(rec_end - rec_start))
    print("Non Recursive => {:0.5f}".format(non_rec_end - non_rec_start))
