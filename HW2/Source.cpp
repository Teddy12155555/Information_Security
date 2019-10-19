#include "DES.h"
#include <sstream>

int main(int argc, char* argv[]) {
	// Format: EncryptDES Key Plaintext

	// Meet the Input Format
	if (argc != 3) {
		return 0;
	}

	string Plaintext = argv[2], Key = argv[1];
	bitset<64>bit_plain, bit_key, bit_cipher;

	// Preprocessing
	bit_plain = StrToBits(Plaintext);
	bit_key = StrToBits(Key);

	// Do DES
	MakeKeys(bit_key);
	bit_cipher = DES_SYS(bit_plain);
	
	// Output DES Ciphertext
	stringstream ss;
	string Cipher;
	ss << std::hex << bit_cipher.to_ullong();
	ss >> Cipher;
	for (int i = 0; i < Cipher.size(); i++) {
		Cipher[i] = toupper(Cipher[i]);
	}
	cout << bit_cipher << endl << std::hex << "0x" << Cipher << endl;
	



	// Format: DecryptDES Key Plaintext
	bit_plain = DES_SYS(bit_cipher);

	system("pause");
}
