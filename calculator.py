import operator

operator_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def perform_operation(val1, val2, op):
    return operator_map[op](val1, val2)


def calc(input):
    if input == "":
        return 0
    stack = []
    output = []

    priority = {
        # '(': 3,
        '*': 2,
        '/': 2,
        '-': 1,
        '+': 1,
    }
    i = 0
    while i < len(input):
        num = ""
        while i < len(input) and input[i].isnumeric():
            num += input[i]
            i += 1
        if num:
            output.append(float(num))
        else:
            if input[i] == '(':
                stack.append('(')
            elif input[i] == ')':
                while stack and stack[-1] != '(':
                    op = stack.pop()
                    val2, val1 = output.pop(), output.pop()
                    output.append(perform_operation(val1, val2,op))
                stack.pop() # popping '('
            elif stack and stack[-1] != '(' and priority[input[i]] <= priority[stack[-1]]:
                while stack and stack[-1] != '(' and priority[input[i]] <= priority[stack[-1]]:
                    op = stack.pop()
                    val2, val1 = output.pop(), output.pop()
                    output.append(perform_operation(val1, val2,op))
                stack.append(input[i])
            else:
                stack.append(input[i])
            i += 1

    while stack:
        op = stack.pop()
        val2, val1 = output.pop(), output.pop()
        output.append(perform_operation(val1, val2,op))
    return output[0]


if __name__ == '__main__':

    assert calc("13+2*7") == 27.0
    assert calc("13*2+7") == 34.0
    assert calc("(2+67*3-(63+95))/2") == 22.5

