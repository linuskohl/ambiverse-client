# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Dict
from marshmallow import Schema, fields, post_load


class ErrorMessage(object):
    def __init__(self, message: str = None):
        self.message = message

    def __repr__(self):
        return '<ErrorMessage(message={self.message!r})>'.format(self=self)


class ErrorMessageSchema(Schema):
    message = fields.Str()

    @post_load
    def make_object(self, data):
        return ErrorMessage(**data)


class Meta(object):
    def __init__(self, dumpVersion: str = None, languages: List[str] = list(), creationDate: datetime = None,
                 collectionSize: int = None):
        # The dumpVersion
        self.dumpVersion = dumpVersion
        # The languages
        self.languages = languages
        # The creationDate
        self.creationDate = creationDate
        # The collectionSize
        self.collectionSize = collectionSize

    def __repr__(self):
        return '<Meta(dumpVersion={self.dumpVersion!r}, languages={self.languages!r}, ' \
               'creationDate={self.creationDate!r})>'.format(self=self)


class MetaSchema(Schema):
    dumpVersion = fields.Str()
    languages = fields.List(fields.Str())
    creationDate = fields.DateTime()
    collectionSize = fields.Int()

    @post_load
    def make_object(self, data):
        return Meta(**data)


class Category(object):
    def __init__(self, id: str = None, name: str = None, descriptions: List[str] = list()):
        self.id = id
        self.name = name
        self.descriptions = descriptions

    def __repr__(self):
        return '<Category(id={self.id!r}, name={self.name!r}, ' \
               'descriptions={self.descriptions!r})>'.format(self=self)


class CategorySchema(Schema):
    # The ID
    id = fields.Str()
    # The name
    name = fields.Str()

    # descriptions = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        return Category(**data)


class CategoriesSchema(Schema):
    categories = fields.Mapping(keys=fields.Str(), values=fields.Nested(CategorySchema))


class Author(object):
    def __init__(self, name: str = None, url: str = None):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Author(name={self.name!r}, url={self.url!r})>'.format(self=self)


class AuthorSchema(Schema):
    name = fields.Str()
    url = fields.Url()

    @post_load
    def make_object(self, data):
        return Author(**data)


class Image(object):
    def __init__(self, url: str = None):
        self.url = url

    def __repr__(self):
        return '<Image(url={self.url!r})>'.format(self=self)


class ImageSchema(Schema):
    url = fields.Url()
    licenses = fields.List(fields.Str())
    author = AuthorSchema

    @post_load
    def make_object(self, data):
        return Image(**data)


class Label(object):
    def __init__(self, language: str = None, value: str = None):
        self.language = language
        self.value = value

    def __repr__(self):
        return '<Label(language={self.language!r}, value={self.value!r})>'.format(self=self)


class LabelSchema(Schema):
    language = fields.Str()
    value = fields.Str()

    @post_load
    def make_object(self, data):
        return Label(**data)


class Entity(object):
    def __init__(self, id: str = None, type: str = None, names: Dict = list(), descriptions: List[str] = list(),
                 detailedDescriptions: List[str] = list(),
                 image: Image = None, links: List[str] = list(), categories: List[str] = list()):
        self.id = id
        # The most salient entity type.
        self.type = type
        self.names = names
        self.descriptions = descriptions
        self.detailedDescriptions = detailedDescriptions
        self.image = image
        self.links = links
        self.categories = categories

    def __repr__(self):
        return '<Entity(id={self.id!r}, type={self.type!r}, names={self.names!r})>'.format(self=self)


class EntitySchema(Schema):
    id = fields.Str()
    type = fields.Str()
    names = fields.Mapping(keys=fields.Str(), values=fields.Nested(LabelSchema))
    descriptions = fields.List(fields.Str())
    detailedDescriptions = fields.List(fields.Str())
    image = fields.Nested(ImageSchema)
    links = fields.List(fields.Url())
    categories = fields.List(fields.Str())
    #categories = fields.Nested(CategoriesSchema)

    @post_load
    def make_object(self, data):
        return Entity(**data)


class OutputEntity(object):

    def __init__(self, id: str = None, url: str = None, salience: float = None, name: str = None, type: str = None):
        self.id = id
        self.url = url
        self.salience = salience
        self.name = name
        self.type = type

    def __repr__(self):
        return '<OutputEntity(id={self.id!r}, salience={self.salience!r}, type={self.type!r}, name={self.name!r})>'.format(self=self)


class OutputEntitySchema(Schema):
    id = fields.Str()
    url = fields.Url()
    salience = fields.Float()
    name = fields.Str()
    type = fields.Str()

    @post_load
    def make_object(self, data):
        return OutputEntity(**data)


class EntitiesSchema(Schema):
    entities = fields.Mapping(keys=fields.Str(), values=fields.Nested(EntitySchema))


class Licence(object):
    def __init__(self, name: str = None, url: str = None):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Licence(name={self.name!r}, url={self.url!r})>'.format(self=self)


class LicenceSchema(Schema):
    name = fields.Str()
    url = fields.Url()

    @post_load
    def make_object(self, data):
        return Licence(**data)


class MatchEntity(object):
    def __init__(self, id: str = None, confidence: float = None):
        self.id = id
        self.confidence = confidence

    def __repr__(self):
        return '<MatchEntity(id={self.id!r}, confidence={self.confidence!r})>'.format(self=self)


class MatchEntitySchema(Schema):
    id = fields.Str()
    confidence = fields.Float()
    matches = fields.Nested(EntitySchema)

    @post_load
    def make_object(self, data):
        return MatchEntity(**data)


class Match(object):
    def __init__(self, charLength: int = None, charOffset: int = None, text: str = None, entity: MatchEntity = None):
        # The character length of the match in the text.
        self.charLength = charLength
        # The character offset of the match in the text, starting at 0.
        self.charOffset = charOffset
        # The entity
        self.entity = entity
        # The full text of the match (equivalent to the substring of the text defined by charOffset and charLength).
        self.text = text

    def __repr__(self):
        return '<Match(charLength={self.charLength!r}, charOffset={self.charOffset!r}, text={self.text!r})>'.format(
            self=self)


class MatchSchema(Schema):
    charLength = fields.Int()
    charOffset = fields.Int()
    text = fields.Str()
    entity = fields.Nested(MatchEntitySchema)

    @post_load
    def make_object(self, data):
        return Match(**data)


class AnnotatedMention(object):
    def __init__(self, charLength: int = None, charOffset: int = None):
        # The character length of the match in the text.
        self.charLength = charLength
        # The character offset of the match in the text, starting at 0.
        self.charOffset = charOffset

    def __repr__(self):
        return '<AnnotatedMention(charLength={self.charLength!r}, charOffset={self.charOffset!r})>'.format(self=self)


class AnnotatedMentionSchema(Schema):
    charLength = fields.Int()
    charOffset = fields.Int()

    @post_load
    def make_object(self, data):
        return AnnotatedMention(**data)


class AnalyzeInput(object):
    def __init__(self, docId: str = None, language: str = None, text: str = None, confidenceThreshold: float = None,
                 coherentDocument: bool = None,
                 annotatedMentions: List[AnnotatedMention] = list()):
        # Will be part of the response so that you can identify your documents.
        self.docId = docId
        # Language of the input text.
        self.language = language
        # The natural-language text to analyze.
        self.text = text
        # Filters every entity with a confidence score lower than the threshold (in [0.0,1.0]).
        self.conficendeThreshold = confidenceThreshold
        # Our method by default assumes that the document is coherent, i.e. the entities in it are related to each other.
        # Set this to false if the document contains very different types of entities that are not related to each other.
        self.coherentDocument = coherentDocument
        # Mentions provided by the user
        self.annotatedMentions = annotatedMentions

    def __repr__(self):
        return '<AnalyzeInput(docId={self.docId!r}, language={self.language!r}, text={self.text!r}, ' \
               'confidenceThreshold={self.confidenceThreshold}, coherentDocument={self.coherentDocument!r}, ' \
               'annotatedMentions={self.annotatedMentions!r})>'.format(self=self)


class AnalyzeInputSchema(Schema):
    docId = fields.Str()
    language = fields.Str()
    text = fields.Str()
    confidenceThreshold = fields.Float()
    coherentDocument = fields.Boolean()
    annotatedMentions = fields.Nested(AnnotatedMentionSchema, many=True)

    @post_load
    def make_object(self, data):
        return AnalyzeInput(**data)


class AnalyzeOutput(object):
    def __init__(self, docId: str = None, language: str = None, matches: List[Match] = list(),
                 entities: List[Entity] = list()):
        # Document ID from the input.
        self.docId = docId
        # Language of the text. In case the language is not provided on input, the language is
        # detected automatically, otherwise its the same as the input.
        self.language = language
        # Matches found in the text.
        self.matches = matches
        # All entities found in the text.
        self.entities = entities

    def get_by_type(self, type: str):
        result = []
        for entity in self.entities:
            if entity.type == type:
                result.append(entity)
        return result

    def __repr__(self):
        return '<AnalyzeOutput(docId={self.docId!r}, language={self.language!r}, ' \
               'matches={self.matches}, entities={self.entities!r})>'.format(self=self)


class AnalyzeOutputSchema(Schema):
    docId = fields.Str()
    language = fields.Str()
    matches = fields.Nested(MatchSchema, many=True)
    entities = fields.Nested(OutputEntitySchema, many=True)

    @post_load
    def make_object(self, data):
        return AnalyzeOutput(**data)


class MessageResponse(object):
    def __init__(self, message: str = None, additionalProperties: Dict = {}):
        # The message
        self.message = message
        self.additionalProperties = additionalProperties

    def __repr__(self):
        return '<MessageResponse(message={self.message!r}, additionalProperties={self.additionalProperties!r})>'.format(
            self=self)


class MessageResponseSchema(Schema):
    message = fields.Str()
    additionalProperties = fields.Dict()

    @post_load
    def make_object(self, data):
        return MessageResponse(**data)
