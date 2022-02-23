import cv2
import random
import glob


class Neuron():

    def __init__(self):

        self.S = 0
        self.theta = 10
        self.iterations = 0
        self.Xj = []
        self.Wj = [random.randint(1, 3) for i in range(400)]
        self.presets = {}

    def result(self, number):
        self.S = 0

        for i in range(400):
            self.S += self.presets[number][i] * self.Wj[i]
        return 1 if self.S >= self.theta else 0

    def increase_weights_active_inputs(self, number):
        for i in range(400):
            if self.presets[number][i] == 1:
                self.Wj[i] += 1

    def decrease_weights_active_inputs(self, number):
        for i in range(400):
            if self.presets[number][i] == 1:
                self.Wj[i] -= 1


n = Neuron()


for image in glob.iglob('numbers/*.png'):
    n.Xj = []
    number = int(image[-5])

    img = cv2.imread(image)

    for line in img:
        for pixel in line:
            x = 0
            if not pixel.any():
                x = 1
            n.Xj.append(x)

    n.presets[number] = n.Xj


flag = False
n.iterations = 0

while not flag:

    isCorrect = True

    for i in n.presets:

        if i % 2 == 0:
            print(i, "Even")
            expectation = 1
        else:
            print(i, 'Odd')
            expectation = 0

        res = n.result(i)

        if expectation != res:
            print(f'Expectation - {expectation}, Got - {res}')
            if res:
                n.decrease_weights_active_inputs(i)
                print('\tWeights decreased')
                isCorrect = False
            else:
                n.increase_weights_active_inputs(i)
                print('\tWeights increased')
                isCorrect = False

        n.iterations += 1

        print(f'Number {i} corrected with {n.iterations} iteration(s)\n---------------------------------------')

    if isCorrect:
        flag = True

    
