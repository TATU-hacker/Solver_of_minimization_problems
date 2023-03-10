# -*- coding: utf-8 -*-
from IHS import *

class I_IHSAlgorithm(IHSAlgorithm):
    def __init__(self, parameters):
        IHSAlgorithm.__init__(self)
        assert len(parameters) == 9
        self.setHMCR(parameters[3:5])
        self.setPAR(parameters[5:7])
        self.setBW(parameters[7:9])
        self.setHMS(parameters[2])
        self.setNumOfIterations(parameters[1])
        self.setVariables(parameters[0])
        self._setDefaultBounds()
        self.setFunction(parameters[0])


    def setHMCR(self, HMCR):
        self._setPair('HMCR', 0, 1, HMCR)

    def setPAR(self, PAR):
        self._setPair('PAR', 0, 1, PAR)

    def setBW(self, BW):
        self._setPair('BW', 1e-20, 1e20, BW)

    def setNumOfIterations(self, NumOfIterations):
        self._setInteger('NumOfIterations', NumOfIterations)

    def setHMS(self, HMS):
        self._setInteger('HMS', HMS)

    def _setPair(self, parameter, minLimit, maxLimit, inputList):
        assert len(inputList) == 2, parameter + " input list has wrong size"
        assert isinstance(inputList[0], float) and isinstance(inputList[1], float), parameter + \
                                                                                    " should be a pair of floats"
        try:
            parameterMin = float(inputList[0])
            parameterMax = float(inputList[1])
        except ValueError:
            raise ValueError(parameter + " its floats but something went wrong")

        assert parameterMin <= parameterMax, parameter + ": parameterMin should be <= parameterMax"
        assert parameterMin >= minLimit, parameter + ": parameterMin should be >= minLimit"
        assert parameterMax <= maxLimit, parameter + ": parameterMax should be <= maxLimit"
        exec('self._' + parameter + 'max = parameterMax')
        exec('self._' + parameter + 'min = parameterMin')

    def _setInteger(self, parameter, value):
        try:
            value = int(value)
        except:
            raise Exception(parameter + " should be an integer")

        if value <= 1:
            raise Exception(parameter + " should be bigger than 1")
        else:
            exec('self._' + parameter + ' = value')

    def setVariables(self, expression, constants={}):
        try:
            p = VariablesParser(expression, constants)
            variables = p.getVariables()
            self._variables = variables
        except Exception as ex:

            print(ex.args)

    def getVariables(self):
        return self._variables

    def setFunction(self, inputBoxExpression):
        strOfVars = ''
        strOfVarsFinal = ''
        for var in self._variables:
            strOfVars += var
            strOfVarsFinal += "X['" + var + "']"
            if var != self._variables[-1]:
                strOfVars += ', '
                strOfVarsFinal += ', '
        self._objective_function = eval('lambda ' + strOfVars + ': ' + inputBoxExpression)
        self.compute = eval('lambda self, X: self._objective_function(%s)' % strOfVarsFinal)

    def setBounds(self, index, lower, upper):
        if len(self._varLowerBounds) <= index:
            self._varLowerBounds.append(lower)
            self._varUpperBounds.append(upper)
        else:
            self._varLowerBounds[index] = lower
            self._varUpperBounds[index] = upper

    def _setDefaultBounds(self):
        for i in range(len(self._variables)):
            self.setBounds(i, -10, 10)

    def getBounds(self):
        return self._varLowerBounds, self._varUpperBounds



if __name__ == "__main__":
    def initIHS(HMS, HMCR, PAR, BW, NumOfIterations, function):

        ihs = I_IHSAlgorithm([function, NumOfIterations, HMS, HMCR[0], HMCR[1], PAR[0],
                              PAR[1], BW[0], BW[1]])
        ihs.doYourTask()


        return ihs


    NumOfIterations = 200000

    ihs = initIHS(10, [0.85, 0.95], [0.2, 0.8], [0.00001, 0.2], NumOfIterations,
                  "2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")

    print(ihs._f)
    print(ihs._HM)
