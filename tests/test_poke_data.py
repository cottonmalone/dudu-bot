import GetPokeInfo


def test_poke_data():

    data = GetPokeInfo.getPokeInfoString("tests/data/out.pk8")

    print(f"\n\n```asciidoc\n{data}\n```\n\n")
