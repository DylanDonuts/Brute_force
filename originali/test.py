import algoritmo as algo
import pytest


def testCreacampione() :
    for i in range(100):
        a = algo.get_random_string(i, algo.dictionary)
        elements = 100 
        campione = algo.creaCampione(a, elements)
        
        assert len(campione) == elements -1
        for j in range(len(campione)) :
            print("qui")
            assert len(campione[j]) == i 


def testGenerapassword():
    for i in range(5, 1000):
        pwd_a = algo.generapassword(i)
        pwd_b = algo.generapassword(i)
        assert pwd_a != pwd_b
        assert len(pwd_a) == i and len(pwd_b) == i


if __name__ == "__main__":
    testCreacampione()
    testGenerapassword()
