import GetPokeInfo


def test_poke_data():

    data = GetPokeInfo.getPokeInfoString("tests/data/out.pk8")

    print(data)
