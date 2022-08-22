#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int * find_primitive_roots(int n){
  for(int g=1; g < n-1; g++){
    // needs to be an array of size n
    int candidate[n-2];
    int valid_results = 0;

    for(int k=0; k < n-2; k++){
      int result = pow(g,k); 
      result = result % n;
      //candidate[k]=result;
      printf("%d^%d mod %d = %d\n", g,k,n,result);
      bool duplicate = 0;
      for(int j=0; j<k; j++){
        if(result==candidate[j]){
          duplicate = 1;
          break;
        }
      }
      if(duplicate){
        printf("Disqualified!\n");
        break;
      }
      candidate[k]=result;
      valid_results++;
    }
    printf("We found %d valid results, out of %d\n", valid_results, n-2);
    for(int k=0; k < valid_results; k++){
      printf("%d ", candidate[k]);
    }
    if(valid_results == n-2){
      printf("\n%d IS INDEED A PRIMITIVE ROOT MODULO\n", g);
    }
    printf("\n=============================\n");
  }
  static int r[3] = {6,6,6};
   
  return r;
}

// example, 3000, len is 3, so min output is 100
int generate_sieve_prime(int n, int prime_len) {
    // TODO: if the prime_len doesn't make sense, handle it
    // 0 doesn't make sense
    // 5 doesn't make sense when my n is 4 digits
    int sieve_floor = pow(10,prime_len-1);
    int sieve_ceiling = n;

    if(prime_len == 0 || sieve_floor > n){
      printf("The significant figure of length %d is not valid.", prime_len); 
      return 0;
    }
    bool candidates[n+1];
    memset(candidates, true, sizeof(candidates));
    bool hit_limit = false;

    printf("FLOOR: %d", sieve_floor);
    for(int start=2; start < sqrt(sieve_ceiling); start++){
    	if(candidates[start]==true){
      		float start_point = (sieve_floor - pow(start,2))/start;
      		if(start_point > 0){
        		if (start_point != (int)start_point){
          			start_point = (int)start_point + 1;
        		}
      		}
      		else{
        		start_point = 0;
      		}
		for(int m=start_point; pow(start,2)+(m*start) <= sieve_ceiling; m++){
        		int found_prime = pow(start,2)+m*start;
        		candidates[found_prime]=false;
      		}
    	}
    }
    srand((unsigned) time(NULL));
    int index = sieve_floor + (rand() % sieve_ceiling);
    printf("FLOOR: %d", sieve_floor);
    bool picked_random_pickle = false;
    while(picked_random_pickle!=true){
        if(candidates[index]){
            picked_random_pickle = true;
        }
        else{
            index++;
        }
    }

    return index;
}
