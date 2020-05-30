`include "AND.v"
module AND_tb;
reg [2:1]a;
reg [2:1]b;

wire [2:1]v;

initial begin
	$dumpfile("AND_tb.vcd");
	$dumpvars(0, AND_tb);
	$monitor($time, ": , a: %b, b: %b, v: %b", a, b, v);
end
AND AND_(.a(a), .b(b), .v(v));


initial begin
a = 2'b00; 
b = 2'b00; 

#10 a = 2'b10; b = 2'b00; 
#10 a = 2'b01; b = 2'b00; 
#10 a = 2'b11; b = 2'b00; 
#10 a = 2'b00; b = 2'b10; 
#10 a = 2'b10; b = 2'b10; 
#10 a = 2'b01; b = 2'b10; 
#10 a = 2'b11; b = 2'b10; 
#10 a = 2'b00; b = 2'b01; 
#10 a = 2'b10; b = 2'b01; 
#10 a = 2'b01; b = 2'b01; 
#10 a = 2'b11; b = 2'b01; 
#10 a = 2'b00; b = 2'b11; 
#10 a = 2'b10; b = 2'b11; 
#10 a = 2'b01; b = 2'b11; 
#10 a = 2'b11; b = 2'b11; 
#10 a = 2'b00; b = 2'b00; 

end
endmodule
