#include <stdio.h>
#include <stdlib.h>

#define MAX 500

int * generate_glibc(int seed) {
  int r[MAX];
  int results[MAX];
  int i;

  r[0] = seed;
  results[0] = r[0];

  for (i = 1; i < MAX; i++) {
    r[i] = (16807LL * r[i - 1]) % 2147483647;
    if (r[i] < 0) {
      r[i] += 2147483647;
    }
    results[i] = r[i];
  }

  for (i = 31; i < 34; i++) {
    r[i] = r[i - 31];
    results[i] = r[i];
  }

  for (i = 34; i < 344; i++) {
    r[i] = r[i - 31] + r[i - 3];
    results[i] = r[i];
  }

  for (i = 344; i < MAX; i++) {
    r[i] = r[i - 31] + r[i - 3];
    results[i] = (unsigned int)r[i] >> 1;
  }

  return results;
}

int main() {
    srand(1);
    int * r = generate_glibc(1);
    for (int i = 344; i < MAX; i++) {
        printf("%d:\n", i);
        printf("%d\n", rand());
        printf("%d\n\n", r[i]);
    }
}