from backend.models import BookCreate

import xml.etree.ElementTree as ET
from rdflib import Graph
from io import StringIO
import httpx
from PIL import Image
from io import BytesIO


def clean_isbn(value):
    isbn, sep, remainder = value.strip().partition(" ")
    if len(isbn) < 10:
        return ""
    for char in "-:.;":
        isbn = isbn.replace(char, "")
    return isbn


# PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# SELECT *
# WHERE {
# ?Oeuvre rdfs:label ?title; dcterms:creator ?creator.
# ?edition bnf-onto:isbn '2-7028-4777-3' ;
# rdarelationships:workManifested ?Oeuvre.
# ?creator foaf:name ?name.
# ?concept foaf:focus ?edition.
# OPTIONAL { ?edition dcterms:date ?date }
# OPTIONAL { ?edition bnf-onto:isbn ?isbn }
# OPTIONAL { ?edition dcterms:publisher ?publisher }
# OPTIONAL { ?edition bibo:isbn13 ?isbn13 }
# } LIMIT 100


async def isbn2book_sudoc(isbn: int) -> BookCreate | None:
    """Query Sudoc api to find a book notice

    Parameters
    ----------
    isbn : int
        ISBN to search

    Returns
    -------
    BookCreate or None
        Book if found
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://www.sudoc.fr/services/isbn2ppn/{isbn}")
        # print(r.text)

        root = ET.fromstring(r.text)
        # print(root.tag)

        err = root.find("error")
        if err is not None:
            print(f"return isbn2ppn Error : {err.text}")
            return None

        x = root.find("query/resultNoHolding")
        if x is None:
            x = root.find("query/result")

        ppn = x.find("ppn").text
        print(f"Got PPN: {ppn}")

        r = await client.get(f"https://www.sudoc.fr/{ppn}.rdf")
        # print(r.text)

        # Create a Graph
        g = Graph()

        # Parse in an RDF file hosted on the Internet
        g.parse(StringIO(r.text), format="application/rdf+xml")

        knows_query3 = """
        select ?book ?title ?abstract ?date ?publisher ?format where {
            ?book a bibo:Book .
            ?book dc:title ?title .
            OPTIONAL { ?book dcterms:abstract ?abstract }
            ?book dc:date ?date .
            ?book dc:publisher ?publisher .
            ?book dc:format ?format .
        }"""

        qres = g.query(knows_query3)
        for row in qres:
            # debug(row)
            print(f"{row.book} knows {row.title}")

            title = row.title.split(" / ")

            if len(title) > 1:
                author = title[1].split(" ; ")[0]
            else:
                author = ""

            publisher = row.publisher.split(" : ")[1].split(" , ")[0].strip("[]")

            book = BookCreate(
                title=title[0],
                abstract=row.abstract or "",
                publication_date=row.date,
                publisher=publisher,
                author=author,
                format=row.format,
                language="fr",
                isbn=isbn,
            )
            break

        # debug(book)

    return book


async def isbn2book_bnf(isbn) -> BookCreate | None:
    """Query bnf SRU api to find a book notice
    https://api.bnf.fr/api-sru-catalogue-general
    https://couverture.geobib.fr/
    https://github.com/hackathonBnF/hackathon2016/wiki/API-Couverture-Service
    https://pypi.org/project/isbnlib/
    Parameters
    ----------
    isbn : int
        ISBN to search

    Returns
    -------
    BookCreate or None
        Book if found
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN%20all%20%22{isbn}%22&recordSchema=dublincore&maximumRecords=100&startRecord=1"
        )
        print(r.text)

        root = ET.fromstring(r.text)
        print(root.tag)

        namespaces = {
            "srw": "http://www.loc.gov/zing/srw/",
            "mxc": "info:lc/xmlns/marcxchange-v2",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

        nb = root.find("srw:numberOfRecords", namespaces).text
        print(f"found {nb} records")
        if nb == 0:
            return None

        # idArk, l'identifiant ARK du document numérique
        recordIdentifier = root.find(
            "srw:records/srw:record/srw:recordIdentifier", namespaces
        ).text
        print(recordIdentifier)

        couv = await client.get(
            f"http://catalogue.bnf.fr/couverture?&appName=NE&idArk={recordIdentifier}&couverture=1",
            follow_redirects=True,
        )

        print(f"Couverture status {couv.status_code}, url {couv.url}")

        im = Image.open(BytesIO(couv.content))
        print(im.format, im.size, im.mode)

        # recordData contain standart record format : unimarcXchange,dublincore
        for recordData in root.findall(
            "srw:records/srw:record/srw:recordData", namespaces
        ):
            # dublincore format
            title = recordData.findtext(".//dc:title", "", namespaces)
            print(title)

            source = recordData.findtext(".//dc:identifier", "", namespaces)
            print(source)

            author = recordData.findtext(".//dc:creator", "", namespaces)
            print(author)

            publisher = recordData.findtext(".//dc:publisher", "", namespaces)
            print(publisher)

            format = recordData.findtext(".//dc:format", "", namespaces)
            print(format)

        return None

    return book


async def isbn2book_googlebooks(isbn) -> BookCreate | None:
    """Query Google book api to find a book notice

    Parameters
    ----------
    isbn : int
        ISBN to search

    Returns
    -------
    BookCreate or None
        Book if found
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        )
        # print(r.text)

        if r.json()["totalItems"] == 0:
            print("GoogleBooks: not found")
            return None

        volume_info = r.json()["items"][0]["volumeInfo"]
        if volume_info is None:
            print("GoogleBooks: no volume info")
            return None

        # debug(volume_info)

        try:
            img = volume_info["imageLinks"]["thumbnail"]
        except KeyError:
            img = ""

        book = BookCreate(
            title=volume_info.get("title", "") + " " + volume_info.get("subtitle", ""),
            abstract=volume_info.get("description", ""),
            publication_date=volume_info.get("publishedDate", ""),
            publisher=volume_info.get("publisher", ""),
            author=volume_info.get("authors", "")[0],
            format=f"{volume_info.get('pageCount', '')}p.",
            language=volume_info.get("language", ""),
            isbn=isbn,
            cover_url=img,
        )

    return book


async def isbn2book(in_isbn: str) -> BookCreate | None:
    isbn = clean_isbn(in_isbn)  # "978-2013944762"
    if isbn == "" or not isbn.isdecimal():
        print("Invalid ISBN format")
        return None

    book = await isbn2book_bnf(isbn)

    # if book is None:
    #     book = await isbn2book_googlebooks(isbn)
    #
    #     if book is None:
    #         book = await isbn2book_sudoc(isbn)

    return book
