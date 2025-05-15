set COLORS;
set REPRESENTATIVE;

param cost {COLORS, REPRESENTATIVE};
param p;

var x {COLORS, REPRESENTATIVE} binary;
var y {REPRESENTATIVE} binary;

minimize total_cost: sum {i in COLORS, j in REPRESENTATIVE} cost[i,j] * x[i,j];

subject to assign_colors {i in COLORS}:
   sum{j in REPRESENTATIVE} x[i,j] = 1;

subject to choose_representative {i in COLORS, j in REPRESENTATIVE}:
   x[i,j] <= y[j];

subject to p_choose_representative:
   sum{j in REPRESENTATIVE} y[j] = p;