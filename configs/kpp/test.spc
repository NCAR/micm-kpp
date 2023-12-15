#INCLUDE atoms.kpp

#DEFVAR
O   = O;             { Oxygen atomic ground state }
O1D = O;             { Oxygen atomic excited state }
O3  = O + O + O;     { Ozone }
NO  = N + O;         { Nitric oxide }
NO2 = N + O + O;     { Nitrogen dioxide }
NO3 = N + O + O + O; { Nitric acid ion }

H2O = O + H + H; {Water}
OH  = O + H;     {Hydroxyl Radical}

HNO3 = H + N + O + O + O; { Nitric acid }

#DEFFIX
M   = O + O + N + N; { Atmospheric generic molecule }
O2  = O + O;         { Molecular oxygen }
