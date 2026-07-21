Get["reslib.wl"];
assign = {{{1,2},"yz"}, {{1,3},"yz"}, {{2,3},"yz"}, {{1,4},"yz"}};
t0 = AbsoluteTime[];
sol = solveSystem[assign];
t1 = AbsoluteTime[];
Print["time: ", t1-t0, "s   nsolutions: ", Length[sol]];
Print[sol // Short];
