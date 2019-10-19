#include <bitset>
#include <iostream>
#include <string>
#include <vector>
#ifndef DES_h
#define DES_h
using namespace std;
vector<bitset<48>>SubKeys;
//S-Boxes
int S_BOX[8][4][16] = {
    //s1 for MSB
    {
        {14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7},
        {0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8},
        {4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0},
        {15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13}
    },
    {
        {15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10},
        {3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5},
        {0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15},
        {13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9}
    },
    {
        {10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8},
        {13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1},
        {13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7},
        {1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12}
    },
    {
        {7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15},
        {13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9},
        {10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4},
        {3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14}
    },
    {
        {2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9},
        {14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6},
        {4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14},
        {11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3}
    },
    {
        {12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11},
        {10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8},
        {9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6},
        {4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13}
    },
    {
        {4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1},
        {13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6},
        {1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2},
        {6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12}
    },
    {//s8 for LSB
        {13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7},
        {1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2},
        {7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8},
        {2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11}
    }
};
//Initial Permutation
int IP[] = {58, 50, 42, 34, 26, 18, 10, 2,60, 52, 44, 36, 28, 20, 12, 4,62, 54, 46, 38, 30, 22, 14, 6,64, 56, 48, 40, 32, 24, 16, 8,57, 49, 41, 33, 25, 17, 9,  1,59, 51, 43, 35, 27, 19, 11, 3,61, 53, 45, 37, 29, 21, 13, 5,63, 55, 47, 39, 31, 23, 15, 7};
//Final Permutation
int FP[] = {40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41,  9, 49, 17, 57, 25};
//Permutation in "f" function
int P[] = {16,  7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2,  8, 24, 14,
            32, 27,  3,  9,
            19, 13, 30,  6,
            22, 11,  4, 25 };
//Expansion
int E[] = {32,  1,  2,  3,  4,  5,
            4,  5,  6,  7,  8,  9,
            8,  9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32,  1};
//Key 64 to 56 bits
int PC_1[] = { 57, 49, 41, 33, 25, 17, 9,
                1, 58, 50, 42, 34, 26, 18,
                10,  2, 59, 51, 43, 35, 27,
                19, 11,  3, 60, 52, 44, 36,
                63, 55, 47, 39, 31, 23, 15,
                7, 62, 54, 46, 38, 30, 22,
                14,  6, 61, 53, 45, 37, 29,
                21, 13,  5, 28, 20, 12,  4};
//Key 56 to 48 bits
int PC_2[] = {14, 17, 11, 24,  1,  5,
                3, 28, 15,  6, 21, 10,
                23, 19, 12,  4, 26,  8,
                16,  7, 27, 20, 13,  2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32};
//key shift
int Key_Shift[] = {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};
//overloading
bitset<56> operator+(bitset<28>&L,bitset<28>&R){
    bitset<56>temp;
    for (int i=0; i<28; i++)
        temp[i] = R[i];
    for (int i=28; i<56; i++)
        temp[i] = L[i-28];
    return temp;
}
bitset<4>CharToBits(char c){
    switch (c) {
        case '0':
            return bitset<4>(0);
            break;
        case '1':
            return bitset<4>(1);
            break;
        case '2':
            return bitset<4>(2);
            break;
        case '3':
            return bitset<4>(3);
            break;
        case '4':
            return bitset<4>(4);
            break;
        case '5':
            return bitset<4>(5);
            break;
        case '6':
            return bitset<4>(6);
            break;
        case '7':
            return bitset<4>(7);
            break;
        case '8':
            return bitset<4>(8);
            break;
        case '9':
            return bitset<4>(9);
            break;
        case 'a':case 'A':
            return bitset<4>(10);
            break;
        case 'b':case 'B':
            return bitset<4>(11);
            break;
        case 'c':case 'C':
            return bitset<4>(12);
            break;
        case 'd':case 'D':
            return bitset<4>(13);
            break;
        case 'e':case 'E':
            return bitset<4>(14);
            break;
        case 'f':case 'F':
            return bitset<4>(15);
            break;
        default:
            return bitset<4>(0);
            break;
    }
}
bitset<64>StrToBits(string str){
    bitset<64>bits;
    int j = 0;
    for (int i=str.length()-1; i>=2; i--) {
        bitset<4>temp = CharToBits(str[i]);
        for (int l=0; l<4; l++)
            bits[j+l] = temp[l];
        j+=4;
    }
    return bits;
}
bitset<28>Doing_Key_Shift(bitset<28>Key_28bit,int shiftBits){
    bitset<28>temp = Key_28bit;
    for (int i=27; i>=0; i--)
        Key_28bit[(i+shiftBits)%28] = temp[i];
    return Key_28bit;
}
void MakeKeys(bitset<64>Key){
    bitset<56>key_56bits;
    for (int i=0; i<56; i++)
        key_56bits[55-i] = Key[64 - PC_1[i]];
    for (int j=0; j<16; j++) {
        bitset<28>R;
        for (int i=0; i<28; i++)
            R[i] = key_56bits[i];
        bitset<28>L;
        for (int i=28; i<56; i++)
            L[i-28] = key_56bits[i];
        //shift
        L = Doing_Key_Shift(L, Key_Shift[j]);
        R = Doing_Key_Shift(R, Key_Shift[j]);
        key_56bits = L + R;
        bitset<48>key_48bits;
        for(int i=0;i<48;i++)
            key_48bits[47-i] = key_56bits[56-PC_2[i]];
        SubKeys.push_back(key_48bits);
    }
}
//this is the function that doing permutation with diff table
bitset<64>Permutation(bitset<64>input,int table[]){
    bitset<64>P;
    for (int i=0; i<64; i++)
        P[63-i] = input[64-table[i]];
    return P;
}
bitset<32>Xor(bitset<32>R,bitset<48>Key){
    bitset<48> E_txt;
    for(int i=0; i<48; ++i)
        E_txt[47-i] = R[32-E[i]];
    E_txt = E_txt ^ Key;
    bitset<32> value;
    int index = 0;
    for(int i=0; i<48; i=i+6)
    {
        int row = E_txt[47-i]*2 + E_txt[47-i-5];
        int col = E_txt[47-i-1]*8 + E_txt[47-i-2]*4 + E_txt[47-i-3]*2 + E_txt[47-i-4];
        int num = S_BOX[i/6][row][col];
        bitset<4> binary(num);
        for (int i=0; i<4; i++)value[31-index-i] = binary[3-i];
        index += 4;
    }
    bitset<32> tmp = value;
    for(int i=0; i<32; ++i)
        value[31-i] = tmp[32-P[i]];
    return value;
}
bitset<64>DES_SYS(bitset<64>plain){
    plain = Permutation(plain, IP);
    bitset<32> L;
    for(int i=32; i<64; ++i)L[i-32] = plain[i];
    bitset<32> R;
    for(int i=0; i<32; ++i)R[i] = plain[i];
    bitset<32> temp;
    for(int i=0; i<16; i++)
    {
        temp = R;
        R = L ^ Xor(R, SubKeys[i]);
        L = temp;
    }
    bitset<64> value;
    for(int i=0; i<32; ++i)value[i] = L[i];
    for(int i=32; i<64; ++i)value[i] = R[i-32];
    plain = value;
    value = Permutation(plain, FP);
    return value;
}
#endif
