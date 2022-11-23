from . import parser_2_0, parser_3_0_0


def parse(yaml_buffer):
    if 'openapi' in yaml_buffer:
        version = yaml_buffer['openapi']
        return parser_3_0_0.parse(yaml_buffer)

    if 'swagger' in yaml_buffer:
        version = yaml_buffer['swagger']
        return parser_2_0.parse(yaml_buffer)

    return parser_3_0_0.parse(yaml_buffer)
