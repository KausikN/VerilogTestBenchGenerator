`include "FullAdder.v"
`include "HalfAdder.v"
`include "BitWiseAND.v"


module WallaceMultiplier(A,B,prod);
    
    input [8:1] A,B;
    output [18:1] prod;

    wire s11,s12,s13,s14,s15,s16,s17,s18,s19,s110,s111,s112,s113,s114,s115,s116,s117,s118,s119,s120,s121;
    wire s21,s22,s23,s24,s25,s26,s27,s28,s29,s210,s211,s212,s213,s214,s215,s216;
    wire s31,s32,s33,s34,s35,s36,s37,s38,s39,s310,s311,s312;
    wire s41,s42,s43,s44,s45,s46,s47,s48,s49,s410,s411,s412;
    wire s51,s52,s53,s54,s55,s56,s57,s58,s59,s510,s511,s512;

    wire c11,c12,c13,c14,c15,c16,c17,c18,c19,c110,c111,c112,c113,c114,c115,c116,c117,c118,c119,c120,c121;
    wire c21,c22,c23,c24,c25,c26,c27,c28,c29,c210,c211,c212,c213,c214,c215,c216;
    wire c31,c32,c33,c34,c35,c36,c37,c38,c39,c310,c311,c312;
    wire c41,c42,c43,c44,c45,c46,c47,c48,c49,c410,c411,c412;
    wire c51,c52,c53,c54,c55,c56,c57,c58,c59,c510,c511,c512;

    wire [8:1] p1,p2,p3,p4,p5,p6,p7,p8;

    BitWiseAND ba1(A, B[1], p1);
    BitWiseAND ba2(A, B[2], p2);
    BitWiseAND ba3(A, B[3], p3);
    BitWiseAND ba4(A, B[4], p4);
    BitWiseAND ba5(A, B[5], p5);
    BitWiseAND ba6(A, B[6], p6);
    BitWiseAND ba7(A, B[7], p7);
    BitWiseAND ba8(A, B[8], p8);
  
    assign prod[1] = p1[1];
    assign prod[2] = s11;
    assign prod[3] = s21;
    assign prod[4] = s31;
    assign prod[5] = s41;
    assign prod[6] = s51;
    assign prod[7] = s52;
    assign prod[8] = s53;
    assign prod[9] = s54;
    assign prod[10] = s55;
    assign prod[11] = s56;
    assign prod[12] = s57;
    assign prod[13] = s58;
    assign prod[14] = s59;
    assign prod[15] = s510;
    assign prod[16] = s511;
    assign prod[17] = s512;
    assign prod[18] = c512;

    // ----- Step 1 --------------------------------------

    HalfAdder ha11 (p1[2],p2[1],s11,c11);

    FullAdder fa12 (p1[3],p2[2],p3[1],s12,c12);

    FullAdder fa13 (p1[4],p2[3],p3[2],s13,c13);

    FullAdder fa14 (p1[5],p2[4],p3[3],s14,c14);
    HalfAdder ha14 (p4[2],p5[1],s15,c15);

    FullAdder fa151 (p1[6],p2[5],p3[4],s16,c16);
    FullAdder fa152 (p4[3],p5[2],p6[1],s17,c17);

    FullAdder fa161 (p1[7],p2[6],p3[5],s18,c18);
    FullAdder fa162 (p4[4],p5[3],p6[2],s19,c19);

    FullAdder fa171 (p1[8],p2[7],p3[6],s110,c110);
    FullAdder fa172 (p4[5],p5[4],p6[3],s111,c111);
    HalfAdder ha17  (p7[2],p8[1],s112,c112);

    FullAdder fa181 (p2[8],p3[7],p4[6],s113,c113);
    FullAdder fa182 (p5[5],p6[4],p7[3],s114,c114);

    FullAdder fa191 (p3[8],p4[7],p5[6],s115,c115);
    FullAdder fa192 (p6[5],p7[4],p8[3],s116,c116);

    FullAdder fa110 (p4[8],p5[7],p6[6],s117,c117);
    HalfAdder ha110 (p7[5],p8[4],s118,c118);

    FullAdder fa111 (p5[8],p6[7],p7[6],s119,c119);

    FullAdder fa112 (p6[8],p7[7],p8[6],s120,c120);

    HalfAdder ha113 (p7[8],p8[7],s121,c121);

    // ----- Step 1 --------------------------------------

    // ----- Step 2 --------------------------------------

    HalfAdder ha21 (c11,s12,s21,c21);

    FullAdder fa22 (c12,s13,p4[1],s22,c22);

    FullAdder fa23 (c13,s14,s15,s23,c23);

    FullAdder fa24 (c14,c15,s16,s24,c24);

    FullAdder fa25 (c16,c17,s18,s25,c25);
    HalfAdder ha25 (s19,p7[1],s26,c26);

    FullAdder fa26 (c18,c19,s110,s27,c27);
    HalfAdder ha26 (s111,s112,s28,c28);

    FullAdder fa271 (c110,c111,c112,s29,c29);
    FullAdder fa272 (s113,s114,p8[2],s210,c210);

    FullAdder fa28 (c113,c114,s115,s211,c211);

    FullAdder fa29 (c115,c116,s117,s212,c212);

    FullAdder fa210 (c117,c118,s119,s213,c213);

    HalfAdder ha211 (c119,s120,s214,c214);

    HalfAdder ha212 (c120,s121,s215,c215);

    HalfAdder ha213 (c121,p8[8],s216,c216);

    // ----- Step 2 --------------------------------------

    // ----- Step 3 --------------------------------------

    HalfAdder ha31 (c21,s22,s31,c31);

    HalfAdder ha32 (c22,s23,s32,c32);

    FullAdder fa33 (c23,s24,s17,s33,c33);

    FullAdder fa34 (c24,s25,s26,s34,c34);

    FullAdder fa35 (c25,c26,s27,s35,c35);

    FullAdder fa36 (c27,c28,s29,s36,c36);

    FullAdder fa37 (c29,c210,s211,s37,c37);

    FullAdder fa38 (c211,s212,s118,s38,c38);

    FullAdder fa39 (c212,s213,p8[5],s39,c39);

    HalfAdder ha310 (c213,s214,s310,c310);

    HalfAdder ha311 (c214,s215,s311,c311);

    HalfAdder ha312 (c215,s216,s312,c312);

    // ----- Step 3 --------------------------------------

    // ----- Step 4 --------------------------------------

    HalfAdder ha41 (c31,s32,s41,c41);

    HalfAdder ha42 (c32,s33,s42,c42);

    HalfAdder ha43 (c33,s34,s43,c43);

    FullAdder fa44 (c34,s35,s28,s44,c44);

    FullAdder fa45 (c35,s36,s210,s45,c45);

    FullAdder fa46 (c36,s37,s116,s46,c46);

    HalfAdder ha47 (c37,s38,s47,c47);

    HalfAdder ha48 (c38,s39,s48,c48);

    HalfAdder ha49 (c39,s310,s49,c49);

    HalfAdder ha410 (c310,s311,s410,c410);

    HalfAdder ha411 (c311,s312,s411,c411);

    HalfAdder ha412 (c312,c216,s412,c412);

    // ----- Step 4 --------------------------------------

    // ----- Step 5 --------------------------------------

    HalfAdder ha51 (c41,s42,s51,c51);
    FullAdder fa52 (c51,c42,s43,s52,c52);
    FullAdder fa53 (c52,c43,s44,s53,c53);
    FullAdder fa54 (c53,c44,s45,s54,c54);
    FullAdder fa55 (c54,c45,s46,s55,c55);
    FullAdder fa56 (c55,c46,s47,s56,c56);
    FullAdder fa57 (c56,c47,s48,s57,c57);
    FullAdder fa58 (c57,c48,s49,s58,c58);
    FullAdder fa59 (c58,c49,s410,s59,c59);
    FullAdder fa510(c59,c410,s411,s510,c510);
    FullAdder fa511(c510,c411,s412,s511,c511);
    HalfAdder ha512 (c511,c412,s512,c512);

    // ----- Step 5 --------------------------------------
/*
always@(*) 
    $display(": Intermediate Binary: A = %b (%d), B = %b (%d), Product: %b (%d) -- --%b--", A, A, B, B, prod, prod, p1);
*/
endmodule