import json
from aiogram.types import MessageEntity


# преобразует в строку
def proces_entities(entities):
    entities_list = []
    for entity in entities:
        entities_list.append ({
            'type': entity.type,
            'url': entity.url,
            'offset': entity.offset,
            'length': entity.length,
            'custom_emoji_id': entity.custom_emoji_id})

    return json.dumps (entities_list)


# восстанавливает entities
def restore_entities(entities_string):
    entities = []
    if entities_string:
        entities_raw = json.loads (entities_string)
        for entity_raw in entities_raw:
            entities.append (MessageEntity (
                type=entity_raw ['type'],
                offset=entity_raw ['offset'],
                length=entity_raw ['length'],
                custom_emoji_id=entity_raw ['custom_emoji_id'],
                url=entity_raw ['url']))
    return entities
