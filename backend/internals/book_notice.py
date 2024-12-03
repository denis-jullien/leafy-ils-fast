from xml.etree.ElementTree import Element

from backend.models import BookCreate
from backend.config import Settings

import xml.etree.ElementTree as ET
from rdflib import Graph
from io import StringIO
import httpx
from PIL import Image
from io import BytesIO

import isbnlib
import babelfish
from random_header_generator import HeaderGenerator

# --- bnf saprql test
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
                language=isbn2language(isbn),
                isbn=isbn,
                record_source=row.book,
            )
            break

        # debug(book)

    return book


def unimarcxchange2book(record: Element):
    namespaces = {
        "mxc": "info:lc/xmlns/marcxchange-v2",
    }

    # dublincore format
    title = record.findtext(".//dc:title", "", namespaces)
    print(title)

    source = record.findtext(".//dc:identifier", "", namespaces)
    print(source)

    author = record.findtext(".//dc:creator", "", namespaces)
    print(author)

    publisher = record.findtext(".//dc:publisher", "", namespaces)
    print(publisher)

    format = record.findtext(".//dc:format", "", namespaces)
    print(format)

    book = BookCreate(
        title=record.findtext(".//dc:title", "", namespaces),
        publication_date=record.findtext(".//dc:date", "", namespaces),
        publisher=record.findtext(".//dc:publisher", "", namespaces),
        author=record.findtext(".//dc:creator", "", namespaces),
        format=record.findtext(".//dc:format", "", namespaces),
        language=record.findtext(".//dc:language", "", namespaces),
        record_source=record.findtext(".//dc:identifier", "", namespaces),
    )

    return book


def dublincore2book(record: Element):
    namespaces = {
        "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    langghndf3 = (record.findtext(".//dc:language", "", namespaces),)
    print(langghndf3[0])
    language = babelfish.Language.fromalpha3b(langghndf3[0]).alpha2

    title = record.findtext(".//dc:title", "", namespaces).split(" / ")

    if len(title) > 1:
        author = title[1].split(" ; ")[0]
    else:
        author = ""

    publisher = record.findtext(".//dc:publisher", "", namespaces).split("(")[0]

    book = BookCreate(
        title=title[0],
        abstract="",
        publication_date=record.findtext(".//dc:date", "", namespaces),
        publisher=publisher,
        author=author,  # record.findtext(".//dc:creator", "", namespaces),
        format=record.findtext(".//dc:format", "", namespaces),
        language=language,
        record_source=record.findtext(".//dc:identifier", "", namespaces),
    )

    return book


async def isbn2book_bnf(isbn: int, format: str = "unimarcXchange") -> BookCreate | None:
    """Query bnf SRU api to find a book record
    https://api.bnf.fr/api-sru-catalogue-general
    https://couverture.geobib.fr/
    https://github.com/hackathonBnF/hackathon2016/wiki/API-Couverture-Service
    https://pypi.org/project/isbnlib/
    Parameters
    ----------
    isbn : int
        ISBN to search

    format : str
        either "dublincore" or "unimarcXchange"

    Returns
    -------
    BookCreate or None
        Book if found
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN%20all%20%22{isbn}%22&recordSchema={format}&maximumRecords=100&startRecord=1"
        )

        root = ET.fromstring(r.text)

        namespaces = {
            "srw": "http://www.loc.gov/zing/srw/",
            "mxc": "info:lc/xmlns/marcxchange-v2",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

        nb = int(root.find("srw:numberOfRecords", namespaces).text)
        # print(f"found {nb} records")
        if nb == 0:
            print("BnF: not found")
            return None

        # idArk, l'identifiant ARK du document numérique
        recordIdentifier = root.find(
            "srw:records/srw:record/srw:recordIdentifier", namespaces
        ).text
        print(recordIdentifier)

        couv_url = f"https://catalogue.bnf.fr/couverture?&appName=NE&idArk={recordIdentifier}&couverture=1"

        couv = await client.get(couv_url)

        print(f"Couverture status {couv.status_code}, url {couv.url}")

        im = Image.open(BytesIO(couv.content))
        print(im.format, im.size, im.mode)
        if im.size == (92, 138):
            print("default cover detected")
            couv_url = None

        # recordData contain standart record format : unimarcXchange,dublincore
        for recordData in root.findall(
            "srw:records/srw:record/srw:recordData", namespaces
        ):
            if format == "dublincore":
                book = dublincore2book(recordData)
            elif format == "unimarcXchange":
                book = unimarcxchange2book(recordData)

            if book is not None:
                book.cover = couv_url
                return book

    return None


async def isbn2book_banq(isbn: int) -> BookCreate | None:
    """Query banq.qc.ca  rss api to find a book record

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
        headers = HeaderGenerator()()

        r = await client.get(
            f"https://cap.banq.qc.ca/in/rest/api/rss?q={isbn}&locale=fr",
            headers=headers,
        )

        if r.status_code == 302:
            print("BAnQ doesn't like robots :(")
            return None

        try:
            root = ET.fromstring(r.text)
        except ET.ParseError:
            print("BAnQ XML ParseError")
            return None

        namespaces = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

        item = root.find("channel/item", namespaces)
        if item is None:
            return None

        desc = item.findtext("description", "", namespaces).split("\n")
        print(desc)

        # try:
        publication = desc[-3].split(", ")
        publication_date = publication[1].strip(" []")
        publisher = publication[0]
        # except:
        #     publication_date = None
        #     publisher = None

        book = BookCreate(
            title=item.findtext("title", "", namespaces),
            abstract="",
            publication_date=publication_date,
            publisher=publisher,
            author=item.findtext("itunes:author", "", namespaces),
            format=item.findtext("itunes:summary", "", namespaces),
            language=isbn2language(isbn),
            record_source=item.findtext("link", "", namespaces),
        )

        return book

    return None


async def isbn2book_googlebooks(isbn) -> BookCreate | None:
    """Query Google book api to find a book record

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
            img = None

        book = BookCreate(
            title=volume_info.get("title", "") + " " + volume_info.get("subtitle", ""),
            abstract=volume_info.get("description", ""),
            publication_date=volume_info.get("publishedDate", ""),
            publisher=volume_info.get("publisher", ""),
            author=volume_info.get("authors", "")[0],
            format=f"{volume_info.get('pageCount', '')}p.",
            language=volume_info.get("language", ""),
            isbn=isbn,
            cover=img,
            record_source=volume_info.get("canonicalVolumeLink", ""),
        )

    return book


def isbn2language(isbn):
    lang = isbnlib.info(isbn).split()[0]
    # print(lang)
    lang2 = [item.alpha2 for item in babelfish.LANGUAGE_MATRIX if item.name == lang]
    if len(lang2) > 0:
        return lang2[0]

    return None


async def isbn2book_openlibrary(isbn):
    """Query openlibrary api to find a book record

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
        try:
            r = await client.get(
                f"https://openlibrary.org/isbn/{isbn}.json", follow_redirects=True
            )
        except httpx.ReadTimeout:
            return None

        if r.status_code == 404:
            print("Open Library: not found")
            return None

        print(r.status_code, r.text)

        volume_info = r.json()

        if "covers" in volume_info:
            img = (
                f"https://covers.openlibrary.org/b/id/{volume_info["covers"][0]}-L.jpg"
            )
        else:
            img = None

        work_url = f'https://openlibrary.org{volume_info["works"][0]["key"]}.json'
        print(work_url)

        work_r = await client.get(work_url)
        work = work_r.json()
        print(work)

        descirption = work.get("description", "")
        if isinstance(descirption, dict):
            abstract = descirption.get("value", "")
        else:
            abstract = work.get("description", "").split("\r")[0]

        if "languages" in volume_info:
            lang = volume_info["languages"][0]["key"].split("/")[2]
            language = babelfish.Language(lang).alpha2
        else:
            language = isbn2language(isbn)

        if "authors" in work:
            author = work["authors"][0]["author"]["key"]
        else:
            author = ""

        if "publishers" in volume_info:
            publisher = volume_info["publishers"][0]
        else:
            publisher = None

        book = BookCreate(
            title=volume_info.get("title", "") + " " + volume_info.get("subtitle", ""),
            abstract=abstract,
            publication_date=volume_info.get("publish_date", ""),
            publisher=publisher,
            author=author,
            format=f"{volume_info.get('number_of_pages', '')}p.",
            language=language,
            isbn=isbn,
            cover=img,
            record_source=f"https://openlibrary.org/isbn/{isbn}",
        )

    return book


async def openlibrarycover(isbn):
    # We could also use isbn2book_openlibrary but seems lighter
    async with httpx.AsyncClient() as client:
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        try:
            r = await client.get(url, follow_redirects=True)
        except httpx.ReadTimeout:
            return None

        print(f"Open Library Covers API status {r.status_code}, url {r.url}")

        if len(r.content) > 50:
            return url

        print("Default Open Library Cover detected")

    return None


# Get cover from google images?
# https://www.googleapis.com/customsearch/v1?key={googleapikey}&cx={customsearchengineid}&searchType=image&q={isbn}
# https://www.reddit.com/r/googlecloud/comments/126efns/is_the_google_images_api_still_available/?tl=fr
# https://developers.google.com/custom-search/v1/introduction
# https://programmablesearchengine.google.com/controlpanel/create
# https://developers.google.com/custom-search/v1/using_rest
# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list


async def googleimagescover(isbn, apikey: str, seachengine: str):
    # We could also use isbn2book_openlibrary but seems lighter
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://www.googleapis.com/customsearch/v1?key={apikey}"
            f"&cx={seachengine}&searchType=image&fields=kind,items(title,link,mime,displayLink,image/height,image/width,image/byteSize)"
            f"&num=10&q={isbn}"
            f"&gl=fr"  # Geolocalisation France
        )

        print(f"Google image status {r.status_code}, url {r.url}")

        if "items" in r.json():
            imagessearch = r.json()["items"]
            print(imagessearch)

            for img in imagessearch:
                if "http" in img["link"] and "no-image" not in img["link"]:
                    # TODO : test query image ?
                    return img["link"]

    return None


async def isbn2book(in_isbn: str, settings: Settings) -> BookCreate | None:
    isbn = isbnlib.ean13(in_isbn)  # "978-2013944762"
    if isbn == "":
        print("Invalid ISBN format")
        return None

    openlibrarycovertested = False

    # TODO : use unimarcXchange for abstract
    book = await isbn2book_bnf(isbn, "dublincore")

    if book is None:
        book = await isbn2book_googlebooks(isbn)

        if book is None:
            book = await isbn2book_openlibrary(isbn)
            openlibrarycovertested = True

            if book is None:
                book = await isbn2book_sudoc(isbn)

                if book is None:
                    book = await isbn2book_banq(isbn)

    if book is not None:
        if book.isbn is None:
            book.isbn = isbn

        if (book.cover is None) and not openlibrarycovertested:
            book.cover = await openlibrarycover(isbn)

        if book.cover is None:
            book.cover = await googleimagescover(
                isbn, settings.google_api_key, settings.google_custom_search_engine
            )

    return book
