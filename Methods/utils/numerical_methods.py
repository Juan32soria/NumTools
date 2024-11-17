import math

def bisection_method(Xi, Xs, Tol, Niter, Fun, to_math):
    fm = []
    error = []
    fi = eval(Fun, {"x": Xi, "math": math}, to_math)
    fs = eval(Fun, {"x": Xs, "math": math}, to_math)

    if fi == 0:
        return [], [], Xi, 0
    elif fs == 0:
        return [], [], Xs, 0
    elif fs * fi < 0:
        c = 0
        Xm = (Xi + Xs) / 2
        fe = eval(Fun, {"x": Xm, "math": math}, to_math)
        fm.append(fe)
        error.append(100)

        while error[c] > Tol and fe != 0 and c < Niter:
            if fi * fe < 0:
                Xs = Xm
                fs = eval(Fun, {"x": Xs, "math": math}, to_math)
            else:
                Xi = Xm
                fs = eval(Fun, {"x": Xi, "math": math}, to_math)

            Xa = Xm
            Xm = (Xi + Xs) / 2
            fe = eval(Fun, {"x": Xm, "math": math}, to_math)
            fm.append(fe)
            Error = abs(Xm - Xa)
            error.append(Error)
            c += 1

        if fe == 0 or Error < Tol:
            return fm, error, Xm, c
        else:
            return fm, error, Xm, Niter
    else:
        return [], [], None, None