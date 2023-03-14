# class that produces mathematical functions
# these functions can only operate on JunkBox objects
# and return JunkBox objects
# The functions must be returned so that the driver can pass them to the executors
# The driver will then wait for the results and return them to the user.
#
# The driver will expose an api to the user that will allow
# the user to perform matix math operations
# The user will create matrices and then perform operations on them.
# The driver will then create jobs
# and send them to the executors.
# The driver will then wait for the results and return them to the user.
# this class should act like a factory for mathematical functions
# the functions should be returned so that the driver can pass them to the executors


from junkbox.JunkBox import JunkBox
from junkbox.junkbox_driver import JunkBoxPool
import asyncio


class MathPrimitives:
    def __init__(self):
        pass

    async def add(self) -> callable:
        return lambda a, b: a + b

    def subtract(self):
        return lambda a, b: a - b

    def multiply(self):
        return lambda a, b: a * b

    def divide(self):
        return lambda a, b: a / b


class Math:
    # has a junkbox-driver object as a member
    def __init__(self):
        self.primitives = MathPrimitives()

    def add(self, a: JunkBox, b: JunkBox) -> JunkBox:
        if a.shape != b.shape:
            raise ValueError("JunkBox objects must be the same shape")
        else:
            result = JunkBox(a.shape[0], a.shape[1], None)

            with JunkBoxPool() as pool:
                for i in range(a.shape[0]):
                    for j in range(a.shape[1]):
                        result.insert(
                            i,
                            j,
                            pool.apply_async(
                                target=self.primitives.add(),
                                args=(a.get(i, j), b.get(i, j)),
                            ),
                        )

                pool.join()

            return result
