import sys
import textwrap
from typing import Optional
import importlib.resources

import click

from .inference import init_onnx_session, predict_language


def print_language_prediction(input_string, language, confidence):
    text_slug = textwrap.fill(
        input_string,
        initial_indent="",
        subsequent_indent=28 * " ",
        max_lines=30,
        placeholder="...",
    )
    print(
        textwrap.dedent(
            f"""\
                Input text: {text_slug}
                Language:   {language}
                Confidence: {confidence*100:.0f}%\
            """
        )
    )


@click.command(help="Predicts the language of a text")
@click.argument("input_string", required=False)
def main(input_string: Optional[str]):
    if input_string is None:
        input_string = sys.stdin.read(1024 ^ 3)

    with importlib.resources.path("langc.models", "classifier.onnx") as model_path:
        onnx_session = init_onnx_session(model_path)
    language, confidence = predict_language(onnx_session, input_string)

    print_language_prediction(input_string, language, confidence)


if __name__ == "__main__":
    main()
