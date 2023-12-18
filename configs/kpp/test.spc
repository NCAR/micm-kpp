#INCLUDE atoms.kpp

#DEFVAR
O   = O;             { Oxygen atomic ground state }
O1D = O;             { Oxygen atomic excited state }
O3  = O + O + O;     { Ozone }
NO  = N + O;         { Nitric Oxide }
NO2 = N + O + O;     { Nitrogen Dioxide }
NO3 = N + O + O + O; { Nitric Acid ion }

H2O = O + H + H; {Water}
OH  = O + H;     {Hydroxyl Radical}
HO2 = O + O + H;

HNO3 = H + N + O + O + O; { Nitric Acid }

CO   = C + O; { Carbon Monoxide }

#DEFFIX
M   = O + O + N + N; { Atmospheric generic molecule }
O2  = O + O;         { Molecular Oxygen }
CO2 = C + O + O;     { Carbon Dioxide }
