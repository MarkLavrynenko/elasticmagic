import datetime

import dateutil

from elasticmagic.types import Type, String, Integer, Float, Date, Object, List
from elasticmagic.compat import string_types
from elasticmagic.document import Document, DynamicDocument
from elasticmagic.attribute import AttributedField, DynamicAttributedField
from elasticmagic.expression import Field

from .base import BaseTestCase


class GroupDocument(Document):
    id = Field(Integer)
    name = Field('test_name', String, fields={'raw': Field(String)})

class TagDocument(Document):
    id = Field(Integer)
    name = Field(String)
    group = Field(Object(GroupDocument))

class TestDocument(Document):
    name = Field('test_name', String(), fields={'raw': Field(String)})
    status = Field(Integer)
    group = Field(Object(GroupDocument))
    price = Field(Float)
    tags = Field(List(Object(TagDocument)))
    date_created = Field(Date)
    unused = Field(String)

    __dynamic_fields__ = [
        Field('attr_*', Integer),
    ]


class DocumentTestCase(BaseTestCase):
    def test_document(self):
        self.assertEqual(
            list(TestDocument.fields),
            [
                TestDocument._uid,
                TestDocument._id,
                TestDocument._type,
                TestDocument._source,
                TestDocument._all,
                TestDocument._analyzer,
                TestDocument._parent,
                TestDocument._routing,
                TestDocument._index,
                TestDocument._size,
                TestDocument._timestamp,
                TestDocument._ttl,
                TestDocument._score,
                TestDocument.name,
                TestDocument.status,
                TestDocument.group,
                TestDocument.price,
                TestDocument.tags,
                TestDocument.date_created,
                TestDocument.unused,
            ]
        )
        self.assertIsInstance(TestDocument._id, AttributedField)
        self.assertIsInstance(TestDocument._id.get_field().get_type(), String)
        self.assertEqual(TestDocument._id.get_field().get_name(), '_id')
        self.assert_expression(TestDocument._id, '_id')
        self.assertIsInstance(TestDocument._score, AttributedField)
        self.assertIsInstance(TestDocument._score.get_field().get_type(), Float)
        self.assertEqual(TestDocument._score.get_field().get_name(), '_score')
        self.assert_expression(TestDocument._score, '_score')
        self.assertIsInstance(TestDocument.name, AttributedField)
        self.assertIsInstance(TestDocument.name.get_field().get_type(), String)
        self.assertEqual(TestDocument.name.get_field().get_name(), 'test_name')
        self.assert_expression(TestDocument.name, 'test_name')
        self.assertEqual(list(TestDocument.name.fields), [TestDocument.name.raw])
        self.assertEqual(TestDocument.name._collect_doc_classes(), [TestDocument])
        self.assertIsInstance(TestDocument.name.raw, AttributedField)
        self.assertIsInstance(TestDocument.name.raw.get_field().get_type(), String)
        self.assert_expression(TestDocument.name.raw, 'test_name.raw')
        self.assertEqual(TestDocument.name.raw.get_field().get_name(), 'test_name.raw')
        self.assertEqual(TestDocument.name.raw._collect_doc_classes(), [TestDocument])
        self.assertIsInstance(TestDocument.status, AttributedField)
        self.assertIsInstance(TestDocument.status.get_field().get_type(), Integer)
        self.assertIsInstance(TestDocument.price, AttributedField)
        self.assertIsInstance(TestDocument.price.get_field().get_type(), Float)
        self.assertIsInstance(TestDocument.group, AttributedField)
        self.assertIsInstance(TestDocument.group.get_field().get_type(), Object)
        self.assertEqual(list(TestDocument.group.fields), [TestDocument.group.id, TestDocument.group.name])
        self.assertIsInstance(TestDocument.group.name, AttributedField)
        self.assertEqual(list(TestDocument.group.name.fields), [TestDocument.group.name.raw])
        self.assertEqual(TestDocument.group.name.get_field().get_name(), 'group.test_name')
        self.assertIsInstance(TestDocument.group.name.get_field().get_type(), String)
        self.assertEqual(TestDocument.group.name._collect_doc_classes(), [TestDocument])
        self.assertEqual(TestDocument.group.name.raw.get_field().get_name(), 'group.test_name.raw')
        self.assertIsInstance(TestDocument.group.name.raw.get_field().get_type(), String)
        self.assertEqual(TestDocument.group.name.raw._collect_doc_classes(), [TestDocument])
        self.assertIsInstance(TestDocument.tags, AttributedField)
        self.assertIsInstance(TestDocument.tags.get_field().get_type(), List)
        self.assertEqual(list(TestDocument.tags.fields), [TestDocument.tags.id, TestDocument.tags.name, TestDocument.tags.group])
        self.assertEqual(TestDocument.tags.get_field().get_name(), 'tags')
        self.assert_expression(TestDocument.tags, 'tags')
        self.assertIsInstance(TestDocument.tags.group, AttributedField)
        self.assertIsInstance(TestDocument.tags.group.get_field().get_type(), Object)
        self.assertEqual(list(TestDocument.tags.group.fields), [TestDocument.tags.group.id, TestDocument.tags.group.name])
        self.assertEqual(TestDocument.tags.group.get_field().get_name(), 'tags.group')
        self.assert_expression(TestDocument.tags.group, 'tags.group')
        self.assertIsInstance(TestDocument.tags.group.name, AttributedField)
        self.assertIsInstance(TestDocument.tags.group.name.get_field().get_type(), String)
        self.assertEqual(list(TestDocument.tags.group.name.fields), [TestDocument.tags.group.name.raw])
        self.assertEqual(TestDocument.tags.group.name.get_field().get_name(), 'tags.group.test_name')
        self.assert_expression(TestDocument.tags.group.name, 'tags.group.test_name')
        self.assertIsInstance(TestDocument.tags.group.name.raw, AttributedField)
        self.assertIsInstance(TestDocument.tags.group.name.raw.get_field().get_type(), String)
        self.assertEqual(list(TestDocument.tags.group.name.raw.fields), [])
        self.assertEqual(TestDocument.tags.group.name.raw.get_field().get_name(), 'tags.group.test_name.raw')
        self.assert_expression(TestDocument.tags.group.name.raw, 'tags.group.test_name.raw')
        self.assertRaises(AttributeError, lambda: TestDocument.group._id)
        self.assertRaises(KeyError, lambda: TestDocument.group.fields['_id'])
        self.assertRaises(AttributeError, lambda: TestDocument.group.missing_field)
        self.assertRaises(KeyError, lambda: TestDocument.group.fields['missing_field'])
        self.assertIsInstance(TestDocument.attr_2, AttributedField)
        self.assertIsInstance(TestDocument.attr_2.get_field().get_type(), Integer)
        self.assertEqual(TestDocument.attr_2._collect_doc_classes(), [TestDocument])
        self.assertRaises(AttributeError, lambda: TestDocument.fake_attr_1)
        self.assertIsInstance(TestDocument.wildcard('date_*'), AttributedField)
        self.assertIsInstance(TestDocument.wildcard('date_*').get_field().get_type(), Type)
        self.assert_expression(TestDocument.wildcard('date_*'), 'date_*')
        self.assertEqual(TestDocument.wildcard('date_*').get_field().get_name(), 'date_*')
        self.assertEqual(TestDocument.wildcard('date_*')._collect_doc_classes(), [TestDocument])
        self.assertIsInstance(TestDocument.group.wildcard('date_*'), AttributedField)
        self.assertIsInstance(TestDocument.group.wildcard('date_*').get_field().get_type(), Type)
        self.assert_expression(TestDocument.group.wildcard('date_*'), 'group.date_*')
        self.assertEqual(TestDocument.group.wildcard('date_*').get_field().get_name(), 'group.date_*')
        self.assertEqual(TestDocument.group.wildcard('date_*')._collect_doc_classes(), [TestDocument])
        self.assertIsInstance(TestDocument.wildcard('group_*').id, AttributedField)
        self.assertIsInstance(TestDocument.wildcard('group_*').id.get_field().get_type(), Type)
        self.assert_expression(TestDocument.wildcard('group_*').id, 'group_*.id')
        self.assertEqual(TestDocument.wildcard('group_*').id.get_field().get_name(), 'group_*.id')
        self.assertEqual(TestDocument.wildcard('group_*').id._collect_doc_classes(), [TestDocument])

        self.assertIs(TestDocument._id, TestDocument._id)
        self.assertIs(TestDocument.name, TestDocument.name)
        self.assertIs(TestDocument.group.name, TestDocument.group.name)
        self.assertIs(TestDocument.tags.group.name, TestDocument.tags.group.name)
        self.assertIs(TestDocument.tags.group.name.raw, TestDocument.tags.group.name.raw)
        # TODO: May be we should cache dynamic fields?
        self.assertIsNot(TestDocument.attr_2, TestDocument.attr_2)
        self.assertIsNot(TestDocument._id, GroupDocument._id)
        self.assertIsNot(GroupDocument.name, TestDocument.group.name)
        self.assertIsNot(GroupDocument.name, TestDocument.tags.group.name)
        self.assertIsNot(TestDocument.group.name, TestDocument.tags.group.name)
        self.assertIsNot(TagDocument.name, TestDocument.tags.name)

        doc = TestDocument()
        self.assertIs(doc._id, None)
        self.assertIs(doc.name, None)
        self.assertIs(doc.status, None)
        doc._id = 123
        self.assertIsInstance(doc._id, int)
        self.assertEqual(doc._id, 123)

        doc = TestDocument(_id=123)
        self.assertIsInstance(doc._id, int)
        self.assertEqual(doc._id, 123)
        self.assertIs(doc.name, None)
        self.assertIs(doc.status, None)

        doc = TestDocument(_id=123, name='Test name', status=0,
                           group=GroupDocument(name='Test group'),
                           price=99.99,
                           tags=[TagDocument(id=1, name='Test tag'),
                                 TagDocument(id=2, name='Just tag')])
        self.assertIsInstance(doc._id, int)
        self.assertEqual(doc._id, 123)
        self.assertIsInstance(doc.name, string_types)
        self.assertEqual(doc.name, 'Test name')
        self.assertIsInstance(doc.status, int)
        self.assertEqual(doc.status, 0)
        self.assertIsInstance(doc.group, GroupDocument)
        self.assertIsInstance(doc.group.name, string_types)
        self.assertIsInstance(doc.price, float)
        self.assertAlmostEqual(doc.price, 99.99)
        self.assertEqual(doc.group.name, 'Test group')
        self.assertIsInstance(doc.tags, list)
        self.assertIsInstance(doc.tags[0].name, string_types)
        self.assertEqual(doc.tags[0].name, 'Test tag')

        hit_doc = TestDocument(
            _hit={
                '_id':'123',
                '_score': 1.23,
                '_source': {
                    'test_name': 'Test name',
                    'status': 0,
                    'group': {'name': 'Test group'},
                    'price': 101.5,
                    'tags': [{'id': 1, 'name': 'Test tag'},
                             {'id': 2, 'name': 'Just tag'}],
                    'date_created': '2014-08-14T14:05:28.789Z',
                }
            }
        )
        self.assertEqual(hit_doc._id, '123')
        self.assertAlmostEqual(hit_doc._score, 1.23)
        self.assertEqual(hit_doc.name, 'Test name')
        self.assertEqual(hit_doc.status, 0)
        self.assertIsInstance(hit_doc.group, GroupDocument)
        self.assertEqual(hit_doc.group.name, 'Test group')
        self.assertAlmostEqual(hit_doc.price, 101.5)
        self.assertIsInstance(hit_doc.tags, list)
        self.assertIsInstance(hit_doc.tags[0], TagDocument)
        self.assertEqual(hit_doc.tags[0].id, 1)
        self.assertEqual(hit_doc.tags[0].name, 'Test tag')
        self.assertEqual(hit_doc.tags[1].id, 2)
        self.assertEqual(hit_doc.tags[1].name, 'Just tag')
        self.assertEqual(hit_doc.date_created,
                         datetime.datetime(2014, 8, 14, 14, 5, 28, 789000, dateutil.tz.tzutc()))
        self.assertIs(hit_doc.unused, None)

        hit_doc = TestDocument(
            _hit={
                '_id':'123'
            }
        )
        self.assertEqual(hit_doc._id, '123')
        self.assertIs(hit_doc.name, None)

        doc = TestDocument(_id=123, name='Test name', status=0,
                           group=GroupDocument(name='Test group'),
                           price=101.5,
                           tags=[TagDocument(id=1, name='Test tag'),
                                 TagDocument(id=2, name='Just tag')],
                           attr_3=45)
        self.assertEqual(
            doc.to_source(),
            {
                'name': 'Test name',
                'status': 0,
                'group': {
                    'name': 'Test group'
                },
                'price': 101.5,
                'tags': [
                    {'id': 1, 'name': 'Test tag'},
                    {'id': 2, 'name': 'Just tag'},
                ],
                'attr_3': 45
            }
        )

    def test_inheritance(self):
        class InheritedDocument(TestDocument):
            description = Field(String)

        self.assertEqual(
            list(InheritedDocument.fields),
            [
                InheritedDocument._uid,
                InheritedDocument._id,
                InheritedDocument._type,
                InheritedDocument._source,
                InheritedDocument._all,
                InheritedDocument._analyzer,
                InheritedDocument._parent,
                InheritedDocument._routing,
                InheritedDocument._index,
                InheritedDocument._size,
                InheritedDocument._timestamp,
                InheritedDocument._ttl,
                InheritedDocument._score,
                InheritedDocument.name,
                InheritedDocument.status,
                InheritedDocument.group,
                InheritedDocument.price,
                InheritedDocument.tags,
                InheritedDocument.date_created,
                InheritedDocument.unused,
                InheritedDocument.description,
            ]
        )
        self.assertIsInstance(InheritedDocument.name, AttributedField)
        self.assertIsInstance(InheritedDocument.name.get_field().get_type(), String)
        self.assertEqual(InheritedDocument.name._collect_doc_classes(), [InheritedDocument])
        self.assertIsInstance(InheritedDocument.name.raw, AttributedField)
        self.assertIsInstance(InheritedDocument.name.raw.get_field().get_type(), String)
        self.assertEqual(InheritedDocument.name.raw._collect_doc_classes(), [InheritedDocument])
        self.assertIsInstance(InheritedDocument.description, AttributedField)
        self.assertEqual(InheritedDocument.description._collect_doc_classes(), [InheritedDocument])

        doc = InheritedDocument(_id=123)
        self.assertIsInstance(doc._id, int)
        self.assertEqual(doc._id, 123)
        self.assertIs(doc.name, None)
        self.assertIs(doc.status, None)
        self.assertIs(doc.description, None)
        self.assertEqual(
            doc.to_source(),
            {}
        )

        doc = InheritedDocument(_id=123, status=0, name='Test', attr_1=1, attr_2=2, face_attr_3=3)
        self.assertEqual(
            doc.to_source(),
            {
                'status': 0,
                'name': 'Test',
                'attr_1': 1,
                'attr_2': 2,
            }
        )

    def test_dynamic_document(self):
        self.assertIsInstance(DynamicDocument._id, AttributedField)
        self.assertNotIsInstance(DynamicDocument._id, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument._id.get_field().get_type(), String)
        self.assertEqual(DynamicDocument._id._collect_doc_classes(), [DynamicDocument])
        self.assertIsInstance(DynamicDocument.name, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument.name.get_field().get_type(), Type)
        self.assert_expression(DynamicDocument.name, 'name')
        self.assertEqual(DynamicDocument.name._collect_doc_classes(), [DynamicDocument])
        self.assertIsInstance(DynamicDocument.status, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument.status.get_field().get_type(), Type)
        self.assert_expression(DynamicDocument.status, 'status')
        self.assertEqual(DynamicDocument.status._collect_doc_classes(), [DynamicDocument])
        self.assertIsInstance(DynamicDocument.group, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument.group.get_field().get_type(), Type)
        self.assert_expression(DynamicDocument.group, 'group')
        self.assertEqual(DynamicDocument.group._collect_doc_classes(), [DynamicDocument])
        self.assertIsInstance(DynamicDocument.group.name, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument.group.name.get_field().get_type(), Type)
        self.assertEqual(DynamicDocument.group.name.get_field().get_name(), 'group.name')
        self.assert_expression(DynamicDocument.group.name, 'group.name')
        self.assertEqual(DynamicDocument.group.name._collect_doc_classes(), [DynamicDocument])
        self.assertIsInstance(DynamicDocument.group.name.raw, DynamicAttributedField)
        self.assertIsInstance(DynamicDocument.group.name.raw.get_field().get_type(), Type)
        self.assertEqual(DynamicDocument.group.name.raw.get_field().get_name(), 'group.name.raw')
        self.assert_expression(DynamicDocument.group.name.raw, 'group.name.raw')
        self.assertEqual(DynamicDocument.group.name.raw._collect_doc_classes(), [DynamicDocument])
