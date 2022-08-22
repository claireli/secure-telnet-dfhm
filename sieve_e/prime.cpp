#include <iostream>
#include <math.h>
using namespace std;

void generate_sieve_prime(int n, int prime_len){
  bool candidates[n+1];
  int rand_index_counter = 0;
  // read about memset data type
  memset(candidates, true, sizeof(candidates));

  //if n*n is less digits than prime_len mark everything up until then false

  int sieve_floor = pow(10,prime_len-1);
  int sieve_ceiling = n;
  bool hit_limit = false;

  int k = 2;
  cout << "sieve floor " << sieve_floor << endl;
  cout << "sieve ceiling " << sieve_ceiling << endl;

  for(int start=2; start < sqrt(sieve_ceiling); start++){
    cout << "checking for " << start << "^2 + multiples of start" << endl;
    if(candidates[start]==true){
      //int start_point = pow(start,2) + x * start = 100
      float start_point = (sieve_floor - pow(start,2))/start;
      if(start_point > 0){
        cout << "cut off will be below " << start_point << " to generate results that will qualify" << endl;
        if (start_point != (int)start_point){
          start_point = (int)start_point + 1;
          cout << "has fractional, will need to round up to " << start_point << endl;
        }
      }
      else{
        cout << "no cut off necessary" << endl;
        start_point = 0;
      }
      for(int m=start_point; pow(start,2)+(m*start) <= sieve_ceiling; m++){
        cout << "j = " << pow(start,2) << " + " << m  << "*" << start << " = " << pow(start,2)+m*start << endl;
        int found_prime = pow(start,2)+m*start;
        candidates[found_prime]=false;
      }
    }
  }

  int total_prime=-2;
  for(int i=0; i<=sieve_ceiling; i++){
    if(candidates[i]==true){
      cout << i << " ";
      total_prime++;
    }
  }
  cout << "congrats you found " << total_prime << " prime numbers." << endl;
  srand((unsigned) time(NULL));

  int index = 0 + (rand() % sieve_ceiling);
  bool picked_random_pickle = false;
  while(picked_random_pickle!=true){
    if(candidates[index]){
      cout << "We picked " << index << " for you, it is a prime";
      picked_random_pickle = true;
    }
    else{
      cout << "Composite! " << index  << " Go up an index" << endl;
      index++;
    }
  }
  cout << " * * " << index << " * * " << endl;
}
// known things
// candidates is a list of bools, i'm interested in the indices of the numbers that are true
// seed() can take in a range
// unknown
// i need a range, for all of the true (prime) results. How to count this without going up an order of mag?

// objective
// how do I pick a random number : bool true, out of a list of n length?
/*  for(int i=sieve_floor; i<=sieve_ceiling; i++){
    if (candidates[i]){
      cout << i << " ";
      if (i>= index){
        cout << "this one." << i << endl;
        break;
      }
    }
  }
  cout << "picking randoooo out of " << rand_index_counter << " choices." << endl;
}*/

int main() {
  int max_int=500;
  int digit_len_min=0;
  generate_sieve_prime(max_int, digit_len_min);
  return 0;
}
