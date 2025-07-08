#2nd_Grade_Equations_Solver
import math

a = 1
b = 6
c = 9

#Una computadora no puede usar numeros imaginarios (raíces de números negativos), así que al calcular, por ejemplo, trinomios cuadrados perfectos resulta en error

equation = (-4*a*c)
root = math.sqrt((b**2) + equation)

x1 = (-b + root)/(2*a)
x2 = (-b - root)/(2*a)

#La solución de este error está en el -4*a*c, ya que al restar esa ecuación de b^2 es lo que causa una raíz negativa

#Esta parte del código (if) verifica si -4*a*c es negativo (< 0 ), de ser el caso, se multiplica a sí mismo por -1 para invertir el signo, obtener una raíz positiva, hacer la operación, volverse a multiplicar a sí mismo por -1 para simular haber sacado una raíz negativa y seguir con la fórmula general

if equation < 0:
    equation*-1
    root*-1
    print(f"El valor de x1 es: {x1} \n El valor de x2 es: {x2}")
else:
    print(equation)
    x_1 = (-b + root)/(2*a)
    x_2 = (-b - root)/(2*a)
    print(f"El valor de x1 es: {x_1} \nEl valor de x2 es: {x_2}")
