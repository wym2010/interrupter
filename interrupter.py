def is_atom(e):
    return type(e) is not list


def is_number(e):
    return type(e) is int


def text_of(e):
    return e[1]


def lookup_in_table(e, table):
    if not table:
        raise TypeError('{0} not found!'.format(e))
    for entity in table:
        if entity.has_key(e):
            return entity[e]
        else:
            pass

    raise TypeError('{0} not found!'.format(e))


def extend_table(table, formals, vals):
    table.insert(0, new_entity(formals, vals))
    return table


def new_entity(keys, vals):
    ret = {}
    for key in keys:
        value = vals[keys.index(key)]
        ret[key] = value

    return ret


def initial_table(name):
    return []


def atom_to_action(e):
    if is_number(e):
        return CONST
    if e == '#t':
        return CONST
    if e == '#f':
        return CONST
    if e == 'cons':
        return CONST
    if e == 'car':
        return CONST
    if e == 'cdr':
        return CONST
    if e == 'null?':
        return CONST
    if e == 'eq?':
        return CONST
    if e == 'atom?':
        return CONST
    if e == 'zero?':
        return CONST
    if e == 'add1':
        return CONST
    if e == 'sub1':
        return CONST
    if e == 'number?':
        return CONST
    return IDENTIFIER


def list_to_action(e):
    first = e[0]
    if is_atom(first):
        if first == 'quote':
            return QUOTE
        if first == 'lambda':
            return LAMBDA
        if first == 'cond':
            return COND
        return APPLICATION
    else:
        return APPLICATION


def expression_to_action(e):
    if is_atom(e):
        return atom_to_action(e)
    else:
        return list_to_action(e)


def value(e):
    return meaning(e, [])


def meaning(e, table):
    return expression_to_action(e)(e, table)


def CONST(e, table):
    if is_number(e):
        return e
    if e == '#t':
        return '#t'
    if e == '#f':
        return '#f'
    return ['primitive', e]


def QUOTE(e, table):
    return text_of(e)


def IDENTIFIER(e, table):
    return lookup_in_table(e, table)


def COND(e, table):
    pass


def LAMBDA(e, table):
    func = e[1:]
    func.insert(0, table)
    return ['non-primitive', func]


def type_of(f):
    return f[0]


def f_table_formals_body(f):
    return f[1]


def table_of(f):
    return f[1][0]


def formals_of(f):
    return f[1][1]


def body_of(f):
    return f[1][2]


##todo


def evils(args, table):
    if not args:
        return []
    else:
        ret = []
        for arg in args:
            m = meaning(arg, table)
            ret.append(m)
        return ret


def function_of(e):
    return e[0]


def arguments_of(e):
    return e[1:]


def APPLICATION(e, table):
    return APPLY(meaning(function_of(e), table),
                 evils(arguments_of(e), table))


def is_primitive(f):
    return type_of(f) == 'primitive'


def is_non_primitive(f):
    return type_of(f) == 'non-primitive'


def apply_primitive(name, vals):
    first_val = vals[0]

    def second(vals):
        return vals[1]

    if name == 'cons':
        return second(vals).insert(0, first_val)
    if name == 'car':
        return first_val[0]
    if name == 'cdr':
        return first_val[1:]
    if name == 'null?':
        return bool(first_val)
    if name == 'eq?':
        return first_val == second(vals)
    if name == 'atom?':
        return is_atom(first_val)
    if name == 'zero?':
        return first_val == 0
    if name == 'add1':
        return first_val + 1
    if name == 'sub1':
        return first_val - 1
    if name == 'number?':
        return type(first_val) is int


def apply_closure(f, vals):
    table = f[0]
    body = f[2]
    formals = f[1]

    return meaning(body, extend_table(table, formals, vals))


def APPLY(fun, vals):
    if is_primitive(fun):
        return apply_primitive(fun[1], vals)
    if is_non_primitive(fun):
        return apply_closure(f_table_formals_body(fun), vals)


if __name__ == '__main__':
    print value(['lambda', ['input'], ['input']])  # self-defined function
    # (lambda (input)(input))
    print value([['lambda', ['input'], 'input'], '#t'])  # application
    # ((lambda (input) input) #t)
    print value([['lambda', ['input'], ['add1', 'input']], 1])  # appliction
    # ((lambda input) (add1 input)) 1)
    print value(['car', ['quote', [1, 2, 3]]])  # primitive appliction
    # (car (quote (1 2 3)))
    print value(['quote', [1, 2, 3]])  # appliction
    # (quote (1 2 3))
