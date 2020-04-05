'''
A  function that, given an input n, returns the nth prime palindrome
(prime number that reads same forwards as backwards  Ex: 727).

'''
import mysql.connector
import math

mydb = mysql.connector.connect(
    host="localhost",
    user="youruser",
    passwd="yourpass",
    database="yourdatabase",
    auth_plugin='mysql_native_password'
)

'''
CREATE TABLE `yourdatabase`.`primepalindrome` (
  `id` INT NOT NULL,
  `primepalindromecol` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `primepalindrome_UNIQUE` (`primepalindrome` ASC) VISIBLE);
'''



def nth_prime_palindrome(n: int):

    mycursor = mydb.cursor()

    #Check if we already know what the nth prime palindrome is
    mycursor.execute("SELECT primepalindrome FROM primepalindromes where ID="+str(n)+" Order by id asc limit 1")
    prime = mycursor.fetchone()
    if prime!=None:
        return prime[0]

    #Nope, we don't know what it is. Let's try and compute it.
    # look for primes
    # Let's start by getting the largest prime we have computed so far.
    mycursor.execute("SELECT ID,primepalindrome FROM primepalindromes Order by id desc limit 1 ")
    result = mycursor.fetchone()
    if  result!=None:
        prime_pal_counter = result[0]
        prime=result[1]
    else:
        # Oh, the database is empty?  Then let's start at the begining
        prime_pal_counter=0
        prime=1


    # Look for primes
    while True:
        prime += 1
        #Check and skip to next number if it is not prime
        for i in range(2, int(math.sqrt(prime))):
            if (prime % i) == 0:
                break


        # Can't divide it by anything, must be prime Check if it is also a palindrome
        else:
            if str(prime) == "".join(list(reversed(str(prime)))):
                # Yes, then save prime palindrome for next time
                prime_pal_counter += 1
                print("Next prime in the sequence is ID: "+str(prime_pal_counter)+"\tPrimepalindrome: "+str(prime)+" Is not  the prime we are looking for")

                sql ="INSERT INTO primepalindromes (id, primepalindrome) VALUES (%s, %s)"
                val = (prime_pal_counter,prime)
                mycursor.execute(sql, val)
                mydb.commit()

                # If this is the prime palindrome we are looking for, then exit
                if prime_pal_counter == n:
                    return prime


# Test function
var = input("What nth prime palindrome shall we look for: ")
print("The "+str(int(var))+"th prime palindrome is: ", end =" ")
print(nth_prime_palindrome(int(var)))
