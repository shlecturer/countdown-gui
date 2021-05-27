import numbers


class PostfixCalculator:
    """The PostfixCalculator class performs operations like a
    postfix calculator (hence the name). You can push numbers
    onto the stack and then apply operations to the topmost
    numbers on the stack.

    If you push 2 onto an empty stack, then 5, then perform
    'multiply", the result will be 10, which will be placed
    on the stack. Any operands used by an operation will be
    removed (popped) from the stack. That means that after
    this example, the stack depth (which can be queried with
    'len') will be 1.

    Order matters only for 'minus' and 'divides'. For example
    push(5) push(3) minus() yields a result of 2. However,
    push(3) push(5) minus() yields a result of -2. The same
    rule holds for divides where the first number pushed is
    the the dividend and the second one the divider, e.g.,
    push(25) push (5) divides() yields 5.
    """
    def __init__(self):
        self.__stack = []

    def peek(self):
        """Have a look at the topmost value of the stack.
        This operation does not alter the stack in any way.
        """
        return self.__stack[-1]

    def push(self, val):
        """Push a number onto the stack. Increments the depth.
        """
        assert isinstance(val, numbers.Number)
        self.__stack.append(val)

    def plus(self):
        """Perform the plus operation on the topmost two numbers
        on the stack. Those numbers are popped from the stack and
        the result is pushed onto the stack.
        """
        return self.__calc('+')

    def minus(self):
        """Perform the minus operation on the topmost two numbers
        on the stack. Those numbers are popped from the stack and
        the result is pushed onto the stack.

        To calculate x - y, you must first push x, then y.
        """
        return self.__calc('-')

    def times(self):
        """Perform the times operation on the topmost two numbers
        on the stack. Those numbers are popped from the stack and
        the result is pushed onto the stack.
        """
        return self.__calc('*')

    def divides(self):
        """Perform the divide operation on the topmost two numbers
        on the stack. Those numbers are popped from the stack and
        the result is pushed onto the stack.

        To calculate x / y, you must first push x, then y.
        """
        return self.__calc('/')

    def clear(self):
        """Clear the stack. After this operation, the stack
        depth is 0 and you should not perform any operation
        other than push.
        """
        self.__stack.clear()

    def __calc(self, oper):
        """Utility function that performs the requested operation
        on the top of the stack. The right operand and left operand
        are popped from the stack, the operation is performed, and
        the result is pushed onto the stack.

        The result is also returned by this function.
        """
        if oper in '+-*/':
            ropnd, lopnd = self.__stack.pop(), self.__stack.pop()
            result = eval(f'{lopnd} {oper} {ropnd}')
            self.push(result)
            return result

    def __len__(self):
        """Return the depth of the stack.
        """
        return len(self.__stack)


def main():
    calc = PostfixCalculator()
    calc.push(9)
    calc.push(3)
    calc.times()
    calc.push(3)
    calc.push(50)
    calc.plus()
    calc.plus()
    calc.push(5)
    calc.minus()
    calc.push(5)
    calc.divides()
    assert calc.peek() == 15
    assert len(calc) == 1


if __name__ == '__main__':
    main()
