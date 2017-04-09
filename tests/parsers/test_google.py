import os
import re
from parsers import google

SPACELESS = re.compile(r'(\s|<br\/?>)', re.MULTILINE)
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "templates", "google")


def test_parse_categories():
    """
        Test that category list parser is working 
    """
    grossing = {'name': 'Top Grossing Android Apps', 'url': 'https://play.google.com/store/apps/collection/topgrossing'}

    template = open(os.path.join(TEMPLATES_PATH, "categories.html")).read()
    categories = google.categories(template)

    assert 6 == len(categories)
    assert grossing['name'] in [c['name'] for c in categories]
    assert grossing['url'] in [c['url'] for c in categories if c['name'] == grossing['name']]


def test_parse_top_by_category():
    """
        Test top apps inside a category
    """
    books = [{
        'name': 'Super Mario Run',
        'url': 'https://play.google.com/store/apps/details?id=com.nintendo.zara'
    }, {
        'name': 'Exploração Pro',
        'url': 'https://play.google.com/store/apps/details?id=com.explorationbase.proversion1',
    }, {
        'name': 'Show do Milhão - Oficial',
        'url': 'https://play.google.com/store/apps/details?id=com.sbt.showdomilhao'
    }]
    top_count = 50

    template = open(os.path.join(TEMPLATES_PATH, "single-category.html")).read()
    top_free_games = google.top_apps_from_category(template)

    assert top_count == len(top_free_games)
    for i in range(0, 3):
        expected = books[i]
        got = top_free_games[i]
        assert expected['name'] == got['name']
        assert expected['url'] == got['url']


def test_parse_app_detail():
    """
        Test app details
    """
    expected = dict(
        name='Super Mario Run',
        icon='//lh3.googleusercontent.com/ERlp5QdPfuJeiU0_O5knXjnyvsoraJ2vfR3AaORksQR5ml63zLtyPL-i_umCSudkng=w300',
        price=0.0,
        description="""Uma nova aventura do Mario para jogar com apenas uma mão.<br><br>Você controla o Mario tocando 
        na tela, enquanto ele avança continuamente. Os seus reflexos irão definir a resposta do personagem, 
        então você precisa mostrar a sua habilidade em manobras, saltos estilosos, giros no ar e escaladas em parede 
        para coletar moedas e chegar ao objetivo final!<br><br>O Super Mario Run pode ser baixado gratuitamente e, 
        após a compra do jogo, você terá acesso a todo conteúdo do jogo sem um pagamento adicional. Os três modos de 
        jogo podem ser testados antes de fazer a sua compra: Mundos, corridas e construção do reino.<br><br>■ 
        Mundos<br>Corra e salte com estilo para resgatar a princesa Peach das garras do Bowser!<br><br>Aventure-se em 
        planícies, cavernas, mansões fantasmagóricas, aeronaves, castelos e muito mais!<br><br>Para chegar ao castelo 
        do Bowser, conclua 24 fases em seis mundos diferentes. Há vários aspectos de diversão nas fases, 
        como colecionar os três tipos diferentes de moedas coloridas ou competir com os seus amigos. Você pode jogar 
        o primeiro mundo completo (do mundo 1-1 ao 1-4) gratuitamente.<br><br>■ Corridas<br>Exiba as manobras 
        estilosas do Mario, compita contra amigos e desafie pessoas do mundo todo.<br><br>Um modo de desafio onde a 
        competição é diferente toda vez que você joga.<br><br>Compita contra as manobras estilosas de outros 
        jogadores enquanto você coleta moedas e atrai uma multidão de Toads para a sua torcida. Complete a barra da 
        febre de moedas executando acrobacias para fazer chover moedas. Se o seu desempenho for impressionante, 
        pode ser até que os Toads se mudem para o seu reino e ele será expandido.<br><br>■ Construção do 
        reino<br>Colete moedas e atraia Toads para construir o seu próprio reino.<br><br>Crie um reino sem igual, 
        com decorações e itens adquiridos com as moedas coletadas nas corridas e nas fases. São mais de 100 itens na 
        construção do reino para construir um reino esplêndido! Se você impressionar mais Toads, o número de 
        construções e decorações disponíveis irá aumentar. Com ajuda dos seus amigos Toads, você vai construir o seu 
        reino gradativamente, melhorando-o e expandindo-o cada vez mais! <br><br>■ O que é possível fazer depois de 
        comprar os seis mundos<br><br>・ Todos as fases de Mundos estarão disponíveis<br>Você poderá jogar nas 24 
        fases dos seis mundos. Por que não dá uma chance a todos os desafios e excitação que as 24 fases 
        oferecem?<br><br>・ Mais personagens jogáveis<br>Se você concluir o mundo 6-4 e resgatar a Peach, 
        além de construir as casas do Luigi, Yoshi e Toadette, você poderá usá-los como personagens nos mundos e nas 
        corridas. As habilidades de cada um destes personagens jogáveis são diferentes das do Mario, então por que 
        não tenta se familiarizar com as características especiais de cada um?<br><br>・ Mais fases nas 
        corridas<br>Agora serão sete fases diferentes disponíveis nas corridas, aumentando a diversão!<br>Nas novas 
        fases, Toads roxos e amarelos podem torcer por você.<br><br>・ Mais construções e decorações para o seu 
        reino<br>Os tipos de construções disponíveis aumentará e você pode devolver o esplendor ao seu reino com 
        estes itens adicionais. Coloque a ponte arco-íris para expandir o reino.<br><br>*É necessário ter acesso a 
        uma conexão de internet para jogar. Encargos de dados de celular podem ser aplicáveis.""",
        screenshots=[
           '//lh3.googleusercontent.com/rkdl-NUU9EvLeQVpS67ALTP5kyqV-a8jsn392Iv282WAlFPvJgF7ZI1m-21nCnU51NI=h900',
           '//lh3.googleusercontent.com/tHEWLsXu_LxHXi4OgR9mwgI9_aLmXLo_VPMbZKEbNzVY8udbf2IxduKxrLPDbz1XQwM=h900',
           '//lh3.googleusercontent.com/HgUx4_Gw0UVDdVxGSXTzwNkPzRmMBQQoBOq74RLVVMpaf6YxW6QgegBI__O8qE38CsdW=h900',
           '//lh3.googleusercontent.com/yZepZjzIj7Gu3ZpnZjG_bQ2wOBswxH9H2Uc9VIdPbbW83dyBQBD_No4tMUr111b30zg=h900',
            '//lh3.googleusercontent.com/DR5JCkxZibH66GkrFLI3GXw2zG91Igw8qYu148o20nv9eRxLOpW-_HF_WDB_2VLBmKk=h900',
            '//lh3.googleusercontent.com/9q0yTaBiIBTrgx3W5G-AAJ4ewfSZaXJ0c4Jg1mTJD7UO92n05LiZQC3mMwOomRsk2sU=h900',
            '//lh3.googleusercontent.com/04R_aNrB78mmRRyM8PxBkuLcstG4gcLZBbuFRIvUJkBuMYHA4-_zT2RpgPiSMTDFbF8=h900',
            '//lh3.googleusercontent.com/gwU0Mg4OZVNm_OhWRe_YycTe9Kbht__rDJEzM3dtUg2hXdfTHgS2Ehj6-IbbzeVgnUt8=h900',
            '//lh3.googleusercontent.com/w9uwVJ-T1-5dByRT_kDctRDielsciisWBC-RqoxlDQkfC-rdLbKmpyIqoTO0zuEB8hw=h900',
            '//lh3.googleusercontent.com/Hz7uWS1SanIp1vS7BYncOUm4ETdUGVk4MBYCwIs8BdeveH-Oxf8KwdJgCEaye18rzw=h900',
            '//lh3.googleusercontent.com/1LqOIEw_DR_y06x_V9mNZl7VKA_iIN_RYwK4DZ6qq62fcrS7WJoNv7m6J9zW_7yr9Uc=h900',
            '//lh3.googleusercontent.com/yCw7XESsl71ESSpinOt_3KqDGdKFhyqoKi3zF92smFUG7O4izVZjfCBsSp26ts8IT-E=h900',
            '//lh3.googleusercontent.com/_4AA29D0Kcf5qM2sK7WkS035NtFbN0khovdA2_jAnvGMGSu-4PhX4-vT7yeQCJUbJMw=h900',
            '//lh3.googleusercontent.com/X7FEjBWfCcEIL0ONB6KoZfQt6-VMO7BL7cmpK4U3BdCcMvyiHyWTT1zqfCNGCEWzedo=h900',
            '//lh3.googleusercontent.com/Ama4JS8Q14TnmT7MuSGNt3oZpIBdFDI1NW1sMqKyU1IVB4-mtxyOQujOvrUnuwjgkg=h900'
        ],
        video=dict(
            url="https://www.youtube.com/embed/pS3FRgZAsH0?ps=play&vq=large&rel=0&autohide=1&showinfo=0&autoplay=1",
            thumb="//i.ytimg.com/vi/pS3FRgZAsH0/hqdefault.jpg"
        ),
        review=dict(
            count=681007,
            value=3.6234474182128906,
            version='2.0.1'
        )
    )

    template = open(os.path.join(TEMPLATES_PATH, "free-app.html")).read()
    mario = google.app(template)
    for key in expected:
        if key == 'description':  # no way to make this string comparison using spaces
            assert SPACELESS.sub('', expected[key]).strip() == SPACELESS.sub('', mario[key]).strip()
            continue
        assert expected[key] == mario[key]


def test_parse_paid_app_detail():
    """
        Test paid app details
    """
    expected = dict(
        name='Chameleon Run',
        icon='//lh3.googleusercontent.com/nmsCeAmO6KclI_VoHnRwlZojTa5f6arzz5Cvw-vj-v1Wb-Ex93nwjhzyIcgGfeO2Gg=w300',
        price=6.49,
        description="""Chameleon Run is a unique, fast and challenging autorunner with a colorful twist. Jump, switch and run through expertly crafted levels that will have you running back for more.

Your goal is to switch your color to match the ground as you run and jump from platform to platform. Sounds easy right? Well think again!

Features

- Fast paced running, jumping and switching colors
- Fun jumping mechanics like "double jump" and "head jump"
- Pixel perfect physics
- Stylish, super smooth and colorful graphics
- Non-linear levels with 3 special objectives in each one
- Compete for the fastest time on each level
- Simple two button controls""",
        screenshots=[
            '//lh3.googleusercontent.com/K_NvAC6ZY8rGZdozjp686cuYuwZXntAaHeabJubMa1r_H0VXFJcE3K4RM9pmDgydIxM=h900',
            '//lh3.googleusercontent.com/S8vrCW8pHjnCYYGmURc4RekZ_FjKLALjVlq3V3hOSeFPAxm7VmMwP3SDlrIBn0Poizs=h900',
            '//lh3.googleusercontent.com/HY0i-P9tG4SO1D05chgyEPg85IfeVPW39YaOxD2zeYVWi9HFfxDWN9I8pQWqeAKlxXU=h900',
            '//lh3.googleusercontent.com/PY9THtndFF0miz27dkan79S7Kf3BuoOZgRstM727ORR1HY9Q6nLpCS9PmviBX7_67A=h900',
            '//lh3.googleusercontent.com/_3r6LRRpz2j5GQqVxeyVMzU39ZDDhyXYqrDVKOJWsqR5MTrk55-XjBkd_KWNk3ciB4M=h900',
            '//lh3.googleusercontent.com/PFUUM_w7qnW5AwcDLyylLY_-3B06Nw1Na3frsjLB3y4938Nt2AXWHq8Q-_yk0XvS448=h900',
            '//lh3.googleusercontent.com/pjdnCINmXRaxFUXf9ijFx75RaW2KKouIS0D7MSZ9Z0aK2El3bOuDjVaEn96FAxKZDA=h900',
            '//lh3.googleusercontent.com/xEPyXnsOjaRqDA6wzoBq0Ietr9eZLVUuikLijjfFS7YUQrjUQ34NM_A1owmdDNGcoQ=h900',
            '//lh3.googleusercontent.com/9YRfwNqb2EklH9It0VMgCyzHSFZuke68R7kAb6slEnt_ItNWE-N2XHxOMp4aY9EPYKw=h900',
            '//lh3.googleusercontent.com/GrZ1OhkKeO6H9vUoDcHpi_zERsUrcNYKyvQ7ZtZrXNCfWPU-MVW_gHQY3NjaEhLKnZY=h900',
            '//lh3.googleusercontent.com/qT30SpHo8mYj5Pctl63h2iNPG73EFghUcMYScxkbuXJIg-0jDMRGoBFWwBNLmTZPXg=h900',
            '//lh3.googleusercontent.com/ggCJ6xU_7PKGtEGqdis8iN2vnfp7K2H7gpnx7vAiB7zVYwXj33jp6BN6xdS6jF0yFg=h900',
            '//lh3.googleusercontent.com/UVffD8f_DENUlTf7_IdlCqZn7QwXhD9jGK_FY_OFjaT2Vn-A4hwOqRd77TFnplFX7Vwi=h900',
            '//lh3.googleusercontent.com/5997scZ7tTiTXaqvxk-4hT1W-YvWX-ozc6JtPgk7vCFGvyTsrCZjNYP4lKHthQLNnYQ=h900',
            '//lh3.googleusercontent.com/IP-S66NPZBNj8nyiSB7cBFNGRmldxVAx8egr_zVGuN7FE23feKGxEfT66tSgjOGhclS4=h900'
        ],
        review=dict(
            count=6777,
            value=4.676995754241943,
            version='2.0.1'
        )
    )

    template = open(os.path.join(TEMPLATES_PATH, "paid-app.html")).read()
    kindle = google.app(template)
    for key in expected:
        if key == 'description': # no way to make this string comparison using spaces
            assert SPACELESS.sub('', expected[key]) == SPACELESS.sub('', kindle[key])
            continue

        assert expected[key] == kindle[key]


def test_is_url_directory():
    """
        Test function that verifies if the URL is a directory or an app
    """
    mario_android = "https://play.google.com/store/apps/details?id=com.nintendo.zara"
    top_selling_free = "https://play.google.com/store/apps/category/GAME/collection/topselling_free?start=0&num=50&numChildren=0&cctcss=square-cover&cllayout=NORMAL"
    assert not google.is_url_directory(mario_android)
    assert google.is_url_directory(top_selling_free)