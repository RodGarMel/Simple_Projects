#Equation_System_Calculator

E1x = 4
E1y = 2
E1a = 1

Equation_1 = (f"{E1x}x + {E1y}y = {E1a}")

E2x = 6
E2y = 1
E2a = 2

Equation_2 = (f"{E2x}x + {E2y}y = {E2a}")

print(Equation_1)
print(Equation_2)

#Multiplicar las variables por su valor en la otra ecuacion empezando por x
#Checar si x no es el mismo valor en las dos ecuaciones
#Si no lo es (lo más probable), que se multipliquen a la inversa

times_pt1x = E2x*E1x
times_pt2x = E2x*E1y
times_pt3x = E2x*E1a
times_pt1y = E1x*E2x
times_pt2y = E1x*E2y
times_pt3y = E1x*E2a

if E1x != E2x:
    print(f"{times_pt1x}x + {times_pt2x}y = {times_pt3x}")
    print(f"{times_pt1y}x + {times_pt2y}y = {times_pt3y}")

    #Resolve 

    X_Ray = (times_pt1x - times_pt1y)
    Yankee = (times_pt2x - times_pt2y)
    Alpha = (times_pt3x - times_pt3y)

    print(f"{X_Ray}x + {Yankee}y = {Alpha}")

    #Now we can resolve y

    ans_y = Alpha/Yankee
    print(f"Answer of y is: {ans_y}")

    #Now we can resolve x

    ans_x = (E1a - E1y * ans_y)/E1x

    print(f"The answer of x is: {ans_x}")
else:

    takeout_x = E1x - E2x
    takeout_y = E1y - E2y
    takeout_a = E1a - E2a

    print(f"{takeout_x}x + {takeout_y} = {takeout_a}")

    div = takeout_a/takeout_y

    print(f"y = {div}")

    resolve = (E1a - (E1y*div)/E1x)

    print(f"The answer of x is: {resolve}\n The answer of y is: {div}")


