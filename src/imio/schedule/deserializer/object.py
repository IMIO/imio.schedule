from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.restapi.interfaces import IFieldDeserializer
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IObject
from z3c.form.interfaces import IObjectFactory
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

@implementer(IFieldDeserializer)
@adapter(IObject, IDexterityContent, IBrowserRequest)
class ObjectFieldDeserializer(DefaultFieldDeserializer):
    def __call__(self, value):
        if not (
            "condition" in self.field.schema
            and "display_status" in self.field.schema
            and "operator" in self.field.schema
        ):
            super(ObjectFieldDeserializer, self).__call__(value)

        deserializer = queryMultiAdapter(
            (self.context, self.request, None, None),
            IObjectFactory,
            name="{}.{}".format(
                self.field.schema.__module__,
                self.field.schema.__name__
            )
        )
        arg = {}
        
        if "condition" in value:
            arg["condition"] = value["condition"]
        if "operator" in value:
            arg["operator"] = value["operator"]
        if "display_status" in value:
            arg["display_status"] = value["display_status"]

        condition = deserializer.factory(**arg)
        
        self.field.schema["condition"].vocabulary = getUtility(
            IVocabularyFactory,
            name=self.field.schema["condition"].vocabulary_name
        )(self.context)

        self.field.validate(condition)
        return condition
