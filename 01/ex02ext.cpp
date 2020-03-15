#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <bitset>
using namespace std;

const int MAX = 100;
int random_array[MAX];

int predict(int index) {
    random_array[index] = random_array[index - 31] + random_array[index - 3] % 2147483648;
    return random_array[index];
}

int main() {
    srand(1);
    int expected, predicted;
    float success;
    unsigned int correct_counter = 0;
    int index;

    for (int index = 0; index < 30; index++) {
        random_array[index] = rand();
    }

    for (; index < MAX; index++) {
        expected = rand();
        predicted = predict(index);
        bitset<32> bits(expected ^ ~predicted);
        correct_counter += bits.count();
        success = (float) correct_counter / (float)((index + 1) * 32);
        cout << success << endl;

        if (predicted != expected) {
            random_array[index] = expected % 2147483648;
        }
    }
}