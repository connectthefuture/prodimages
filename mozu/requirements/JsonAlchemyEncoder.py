# coding: utf-8
#
"""
    http://github.com:kolypto/py-flask-jsontools/flask_jsontools/formatting.py

    Copyright (c) 2014, Mark Vartanyan <kolypto@gmail.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES,  INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE  FOR  ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY, OR
    CONSEQUENTIAL   DAMAGES  (INCLUDING,  BUT NOT LIMITED TO,  PROCUREMENT  OF
    SUBSTITUTE GOODS OR SERVICES;  LOSS OF USE, DATA, OR PROFITS;  OR BUSINESS
    INTERRUPTION)  HOWEVER CAUSED AND ON ANY  THEORY OF LIABILITY,  WHETHER IN
    CONTRACT,  STRICT LIABILITY,  OR TORT   (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,  EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.


"""
from json import JSONEncoder


class DynamicJSONEncoder(JSONEncoder):
    """ JSON encoder for custom classes:

        Uses __json__() method if available to prepare the object.
        Especially useful for SQLAlchemy models
    """

    def default(self, o):
        # Custom JSON-encodeable objects
        if hasattr(o, '__json__'):
            return o.__json__()

        # Default
        return super(DynamicJSONEncoder, self).default(o)


#region SqlAlchemy Tools

try:
    from sqlalchemy import inspect
    from sqlalchemy.orm.state import InstanceState
except ImportError as e:
    def __nomodule(*args, **kwargs): raise e
    inspect = __nomodule
    InstanceState = __nomodule


def get_entity_propnames(entity):
    """ Get entity property names

        :param entity: Entity
        :type entity: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :returns: Set of entity property names
        :rtype: set
    """
    ins = entity if isinstance(entity, InstanceState) else inspect(entity)
    return set(
        ins.mapper.column_attrs.keys() +  # Columns
        ins.mapper.relationships.keys()  # Relationships
    )


def get_entity_loaded_propnames(entity):
    """ Get entity property names that are loaded (e.g. won't produce new queries)

        :param entity: Entity
        :type entity: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :returns: Set of entity property names
        :rtype: set
    """
    ins = inspect(entity)
    keynames = get_entity_propnames(ins)

    # If the entity is not transient -- exclude unloaded keys
    # Transient entities won't load these anyway, so it's safe to include all columns and get defaults
    if not ins.transient:
        keynames -= ins.unloaded

    # If the entity is expired -- reload expired attributes as well
    # Expired attributes are usually unloaded as well!
    if ins.expired:
        keynames |= ins.expired_attributes

    # Finish
    return keynames


class JsonSerializableBase(object):
    """ Declarative Base mixin to allow objects serialization

        Defines interfaces utilized by :cls:ApiJSONEncoder
    """

    def __json__(self, exluded_keys=set()):
        return {name: getattr(self, name)
                for name in get_entity_loaded_propnames(self) - exluded_keys}

#endregion
