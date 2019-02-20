import json
import logging
import genanki
import urllib.request



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("pdfminer").setLevel(logging.WARNING)


def get_lines():
    URL = "https://gist.githubusercontent.com/histrio/c1a28773e37dd91a99aa78aaee6c2c99/raw/b373960bed186b2529f9c2d43a89fe9e2dc461ba/ham.json"
    FILENAME = "/tmp/ham.json"
    urllib.request.urlretrieve(URL, FILENAME)

    with open(FILENAME, 'rb') as f:
        data = json.load(f)
        for k, v in data.items():
            yield (k, v)


def w_list():
    for idx, item in get_lines():
        c1, c2, c3, c4 = item['choices']
        yield (idx, item['body'], c1, c2, c3, c4, str(item['answer']))


def main():

    my_model = genanki.Model(
        1607392328,
        'RuHamTest',
        css="""
            .card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }
            ul { width: 90%; list-style-type:"A"; margin:auto; padding:0; position:relative; left:5%; }
        """,
        fields=[
            {'name': 'idx'},
            {'name': 'Question'},
            {'name': 'Choice1'},
            {'name': 'Choice2'},
            {'name': 'Choice3'},
            {'name': 'Choice4'},
            {'name': 'Answer'},
        ],
        templates=[{
            'name': 'Card 1',
            'qfmt': '''
                <h2>Вопрос №{{idx}}</h2><br>
                {{Question}}<br>
                <ul type='a'>
                    <li id="1">{{ Choice1 }}</li>
                    <li id="2">{{ Choice2 }}</li>
                    <li id="3">{{ Choice3 }}</li>
                    <li id="4">{{ Choice4 }}</li>
                </ul>
            ''',
            'afmt': '{{FrontSide}}<script> document.getElementById("{{Answer}}").style.backgroundColor = "green"</script> ',
        }])

    my_deck = genanki.Deck(2059400143, 'Ham Test RU')

    for idx, q, c1, c2, c3, c4, a in w_list():
        my_note = genanki.Note(model=my_model, fields=[idx, q, c1, c2, c3, c4, a], sort_field='idx')
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('/output/hamtest.apkg')


if __name__ == "__main__":
    main()
