module AND (a,b,v);
input [2:1] a, b;
output [2:1] v;
	assign v[1] = a[1] & b[1];
	assign v[2] = a[2] & b[2];
endmodule
