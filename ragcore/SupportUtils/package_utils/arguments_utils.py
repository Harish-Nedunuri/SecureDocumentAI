import argparse
from pydantic import BaseModel

class ArgumentsUnpacker:
    def __init__(self, model: BaseModel):
        self.model = model
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self.add_model_arguments()

    def add_model_arguments(self):
        fields = self.model.model_fields
        for name, field in fields.items():
            self.parser.add_argument(
                f"--{name}",
                dest=name,                
                type=field.annotation,
                default=field.default,
                help=field.description,
            )
    def run(self):
        args = self.parser.parse_args()
        arguments = self.model(**vars(args))
        return arguments